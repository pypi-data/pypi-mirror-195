from __future__ import annotations
import asyncio
import json
import struct
from uuid import UUID

import attr
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms

from ..config import CONFIG
from .frame import Frame, InvalidFrame
from ..proto.common_pb2 import ListenerID
from ..proto.location_pb2 import (IBeaconSummary, TempBeaconSummary,
                                  LABeaconSummary, RawAdvert)
from ..proto.secbeacon_pb2 import SecureSmartRelay
from .sensors import SensorReport
from .sensors.mopeka import Mopeka
import c3loc.stats as stats


ALERTWET_PREFIX = b'\x00\x86\x00\x03\x96\x06\x15\x00\x00\x00\x00\x11\x00\x00'
ALERTWET_THRESHOLD = 2**16 / 2


class PacketType:
    """Enum emulation class."""

    ID = 0
    DATA = 1
    SECURE = 2
    RESPONSE = 3
    REQUEST = 4
    ID_REQUEST = 5
    HEALTH_CHECK = 6
    TEMPBEACON = 7
    LABEACON = 8
    SSR = 9
    RAW = 10


class ADSubType:
    SmartRelay = 0
    SecureSmartRelay = 2
    SensorData = 3


def valid_ssr(ssr):
    key = CONFIG['SSR_KEY']
    c = cmac.CMAC(algorithms.AES(key))
    c.update(ssr.payload)
    calculated = c.finalize()
    if calculated[:4] == ssr.mac:
        stats.increment('Valid MAC')
        return True
    # print(calculated, ssr.payload.hex(), ssr.mac.hex())
    stats.increment('Failed MAC')
    return False


def start_packet_tasks():
    async def packet_task(t_id):
        print(f'Started packet task #{t_id}')
        while True:
            qd_pkt = await ListenerProtocol.packet_queue.get()
            try:
                await qd_pkt.protocol.process_packet(qd_pkt.msg)
            except Exception as e:
                stats.increment('Packet Processing Failure')
                print(f"Exception during packet_task: {e}")
                continue
            stats.increment('Packets Processed')
    for i in range(CONFIG['MAX_DB_CONNECTIONS']):
        asyncio.ensure_future(packet_task(i))


class ListenerProtocol(object):
    callback = None
    db_pool = None
    max_depth = int(CONFIG['MAX_QUEUED_PACKETS'])
    packet_queue: asyncio.Queue[QueuedPacket] = \
        asyncio.Queue(max_depth)
    packet_queue_reg_flag = False

    def __init__(self, verbose=False):
        self._rx_buf = bytearray()
        self.transport = None
        self._frame = Frame()
        self.verbose = verbose
        if not self.db_pool:
            raise NotImplementedError(
                "ListenerProtocol.db_pool must be set before instantiation")
        self.router = {
            PacketType.DATA: self.process_ibeacon,
            PacketType.LABEACON: self.process_relay_beacon,
            PacketType.SSR: self.process_ssr,
            PacketType.RAW: self.process_raw,
        }
        self.ignored_types = {
            PacketType.HEALTH_CHECK, PacketType.SECURE, PacketType.TEMPBEACON}
        self._l_id = None
        self.listener_id = None
        self.peer_name = None
        if not self.packet_queue_reg_flag:
            stats.register_cb(
                'Current Packet Queue Depth', self.packet_queue.qsize)
            self.packet_queue_reg_flag = True

    def connection_made(self, transport) -> None:
        self.transport = transport
        self.peer_name = transport.get_extra_info('peername')[0]
        print("Connection from {}".format(self.peer_name))
        stats.increment('Listener Connections')

    def eof_received(self):
        pass

    def data_received(self, data: bytes) -> None:
        try:
            self._frame.add_bytes(data)
        except InvalidFrame as e:
            print(f'Error: {self.peer_name} sent an InvalidFrame: '
                  f'{e.args[0]}. Disconnecting')
            stats.increment(f'Invalid Frame ({e.args[0]})')
            self.transport.close()
            return
        for msg in self._frame.get_messages():
            stats.increment("Packet Received")
            qd = QueuedPacket(msg, self)
            if self.packet_queue.full():
                stats.increment('Packet Dropped (Queue Full)')
                return
            self.packet_queue.put_nowait(qd)

    def _print_reason(self, report):
        print("\t\tReason: {}".format(self._reason(report)))

    def _reason(self, report):
        reason = ""
        if report.reason in [
                IBeaconSummary.IBeaconReport.EventReason.ENTRY,
                TempBeaconSummary.TempBeaconReport.EventReason.ENTRY,
                LABeaconSummary.LABeaconReport.EventReason.ENTRY]:
            reason = "ENTRY"
        if report.reason in [
                IBeaconSummary.IBeaconReport.EventReason.MOVE,
                TempBeaconSummary.TempBeaconReport.EventReason.MOVE,
                LABeaconSummary.LABeaconReport.EventReason.MOVE]:
            reason = "MOVE"
        if report.reason in [
                IBeaconSummary.IBeaconReport.EventReason.STATUS,
                TempBeaconSummary.TempBeaconReport.EventReason.STATUS,
                LABeaconSummary.LABeaconReport.EventReason.STATUS]:
            reason = "STATUS"
        if report.reason in [
                IBeaconSummary.IBeaconReport.EventReason.EXIT,
                TempBeaconSummary.TempBeaconReport.EventReason.EXIT,
                LABeaconSummary.LABeaconReport.EventReason.EXIT]:
            reason = "EXIT"
        return reason

    async def _upsert_listener(self, conn):
        await conn.execute(
            'INSERT into listeners (id) VALUES ($1) '
            'ON CONFLICT ON CONSTRAINT listeners_pkey '
            'DO UPDATE SET last_seen = (now() at time zone \'utc\') '
            'WHERE listeners.last_seen < now() - interval \'5sec\'',
            self.listener_id)
        # Add a default zone for listeners
        zone_id = await self._select_zone_id(conn)
        if not zone_id:
            r = await conn.fetchrow(
                'INSERT INTO zones (name) VALUES ($1) RETURNING id',
                f'Near Listener {self.listener_id}')
            zone_id = r[0]
            await conn.execute(
                'UPDATE listeners SET zone_id = $1 WHERE id = $2',
                zone_id, self.listener_id)

    async def _select_zone_id(self, conn):
        listener = await conn.fetchrow(
            'SELECT zone_id FROM listeners WHERE id = $1', self.listener_id)
        if not listener:
            return None
        return listener[0]

    async def process_packet(self, msg):
        if msg.type == PacketType.ID:
            self.process_id(msg)
            stats.increment(f'Packets Received ({self.listener_id})')
            return

        stats.increment(f'Packets Received ({self.listener_id})')

        if not self.listener_id:
            print(f'Error: {self.peer_name} non-ID packet before ID. '
                  f'Dropping connection')
            self.transport.close()
            return

        if msg.type in self.ignored_types:
            stats.increment('Ignored Packets')
            return

        conn = await self.db_pool.acquire()
        await self._upsert_listener(conn)
        if msg.type not in self.router:
            stats.increment('Unknown Packets')
            print(f"Warning: No implementation for packet type: {msg.type}")
        else:
            await self.router[msg.type](msg, conn)
        await self.db_pool.release(conn)

    def process_id(self, msg):
        l_id = ListenerID()
        l_id.ParseFromString(msg.data)
        self._l_id = l_id.listener_id
        self.listener_id = self._l_id.hex()
        print("{} identified as {} (version {})".format(
            self.peer_name, self._l_id.hex(), l_id.version))

    async def process_sensor(self, mac_addr, payload, conn):
        ts = payload[:4]
        ts = int.from_bytes(payload[:4], 'little', signed=False)
        payload = payload[4:]
        sensor = SensorReport.parse(payload)
        existing_tag_id = await conn.fetchval(
            "SELECT id from tags WHERE mac = $1 "
            "ORDER BY last_seen DESC LIMIT 1", mac_addr)
        if not existing_tag_id:
            stats.increment("Orphaned sensor packets")
            return
        insert_sensor = await conn.prepare(
            "INSERT INTO sensors (tag_id, type, value, device_ts) "
            "VALUES ($1, $2, $3, $4)")
        for field in sensor.fields:
            await insert_sensor.fetch(
                existing_tag_id, field.tag, field.value, ts)

    async def process_mopeka(self, data, conn):
        mac_addr = bytes(reversed(data.mac)).hex()
        # Parse fields
        m = Mopeka.from_bytes(data.payload)
        # Generate tag, if needed
        listener_zone = await self._select_zone_id(conn)
        (db_id,) = await conn.fetchrow(
            'INSERT into tags (bid, type, mac, zone_id) '
            'VALUES ($1, \'MacBeacon\', $2, $3) '
            'ON CONFLICT ON CONSTRAINT tags_bid_key '
            'DO UPDATE SET last_seen = (now() at time zone \'utc\'), '
            'zone_id = $3 RETURNING id', m.sensor_id, mac_addr,
            listener_zone)

        # Insert fields into sensors table
        insert_sensor = await conn.prepare(
            'INSERT INTO sensors (tag_id, type, value) '
            'VALUES ($1, $2, $3)')
        for sensor in m.to_sensor():
            await insert_sensor.fetch(
                db_id, *sensor)
        stats.increment("Mopeka packets")

    async def process_raw(self, msg, conn):
        data = RawAdvert()
        data.ParseFromString(msg.data)

        if data.payload.find(b'\xff\x59\x00') != -1:
            await self.process_mopeka(data, conn)
            return

        needle = b'\xff\x8d\x09'
        ad_start = data.payload.find(needle)
        payload = data.payload[ad_start+len(needle):]
        subtype = payload[0]

        if subtype == ADSubType.SensorData:
            stats.increment("Sensor Packets")
            mac_addr = bytes(reversed(data.mac)).hex()
            await self.process_sensor(mac_addr, payload[1:], conn)

    async def process_alertwet(self, b, conn):
        stats.increment('AlertWet Reports')

        (b_id,) = struct.unpack(">H", b.uuid[-2:])
        sensor = b.major_num
        batt = b.minor_num
        uuid = UUID(bytes=b.uuid)
        alarm_active = sensor > ALERTWET_THRESHOLD
        raw = json.dumps({'raw': f"{uuid}:{sensor}:{batt}",
                          'wetness': f"{sensor}",
                          'battery': f"{batt}"})
        listener_zone = await self._select_zone_id(conn)
        row = await conn.fetchrow(
            'INSERT into tags '
            '(bid, type, battery_pct, alarm_active, '
            'attrs, last_seen, zone_id, distance) '
            'VALUES ($1, \'AlertWet\', $2, $3, '
            '$4, (now() at time zone \'utc\'), $5, $6) '
            'ON CONFLICT ON CONSTRAINT tags_bid_key DO '
            'UPDATE SET battery_pct = excluded.battery_pct, '
            'alarm_active = excluded.alarm_active, '
            'attrs = excluded.attrs, '
            'last_seen = excluded.last_seen, '
            'zone_id = excluded.zone_id, '
            'distance = excluded.distance '
            'RETURNING tags.id',
            b_id, batt, alarm_active, raw, listener_zone, b.distance_cm / 100)
        (t_id,) = row

        await conn.fetch(
            'INSERT into log (tag_id, zone_id, listener_id, '
            'distance, variance, reason)'
            'VALUES ($1, $2, $3, $4, $5, $6)',
            t_id, listener_zone, self.listener_id, b.distance_cm / 100,
            round(b.variance / 2000, 1), self._reason(b))

        # Record sensor separately
        await conn.fetch(
            "INSERT into sensors (tag_id, type, value) "
            "VALUES  ($1, $2, $3)",
            t_id, 0x4, sensor.to_bytes(2, "little"))

    async def process_ibeacon(self, msg, conn):
        data = IBeaconSummary()
        data.ParseFromString(msg.data)

        # Convert to upsert when last_seen field is added?
        tag_insert = await conn.prepare(
            'INSERT into tags (uuid, major, minor, type)'
            'VALUES ($1, $2, $3, $4) '
            'RETURNING id, last_seen, (now() at time zone \'utc\')')
        tag_select = await conn.prepare(
            'SELECT id, last_seen, (now() at time zone \'utc\') FROM tags '
            'WHERE uuid = $1 AND major = $2 AND minor = $3')
        ibeacon_log = await conn.prepare(
            'INSERT into log '
            '(tag_id, zone_id, listener_id, distance, variance, reason)'
            'VALUES ($1, $2, $3, $4, $5, $6)')
        listener_zone = await self._select_zone_id(conn)
        for b in data.reports:

            if b.uuid.startswith(ALERTWET_PREFIX):
                await self.process_alertwet(b, conn)
                continue

            stats.increment('iBeacon Reports')
            uuid = UUID(bytes=b.uuid)
            tag_type = ''
            if uuid == CONFIG['LA_UUID']:
                tag_type = 'LocationAnchor'
            else:
                tag_type = 'iBeacon'
            t = await tag_select.fetchrow(uuid, b.major_num, b.minor_num)
            if not t:
                t = await tag_insert.fetchrow(uuid, b.major_num, b.minor_num,
                                              tag_type)
            t_id, t_lastseen, db_now = t[0], t[1], t[2]
            diff = (db_now - t_lastseen).seconds
            if diff > CONFIG['LAST_SEEN_RESOLUTION_SECS']:
                await conn.fetch(
                    'UPDATE tags SET last_seen = $1 WHERE id = $2',
                    db_now, t_id)
            await ibeacon_log.fetch(
                t_id, listener_zone, self.listener_id, b.distance_cm / 100,
                round(b.variance / 2000, 1), self._reason(b))

    async def process_ssr(self, msg, conn):
        data = SecureSmartRelay()
        data.ParseFromString(msg.data)
        if not valid_ssr(data):
            print("Invalid SSR, MAC check failed")
            return

        if len(data.payload) < 12:
            print("Ignoring short (but valid MAC?) SSR packet")
            return

        stats.increment("SSR Reports")
        (rssi1m, b_id, ts, status) = struct.unpack("<bIIB", data.payload[2:12])
        batt = status >> 1
        button = bool(status & 0x1)
        mac_addr = bytes(reversed(data.mac_addr)).hex()

        row = await conn.fetchrow(
            'INSERT into tags '
            '(bid, type, battery_pct, alarm_active, last_clock, mac) '
            'VALUES ($1, \'SecureSmartRelay\', $2, $3, $4, $5) '
            'ON CONFLICT ON CONSTRAINT tags_bid_key DO '
            'UPDATE SET battery_pct = excluded.battery_pct, '
            'alarm_active = excluded.alarm_active, '
            'last_clock = excluded.last_clock, '
            'mac = excluded.mac '
            'WHERE tags.last_clock < excluded.last_clock RETURNING tags.id',
            b_id, batt, button, ts, mac_addr)

        if not row:
            # print(f"Skipping duplicate or replayed packet for SSR {b_id}")
            return
        (t_id,) = row

        # Service the alarm state
        if button:
            row = await conn.fetchrow(
                'SELECT id from alarms '
                'WHERE tag_id = $1 and acknowledged = FALSE', t_id)
            if not row:
                await conn.fetchrow(
                    'INSERT INTO alarms (tag_id) VALUES ($1)', t_id)
            else:
                row = await conn.fetchrow(
                    'UPDATE alarms SET last_ts = now() '
                    'WHERE id = $1 AND acknowledged = FALSE', row[0])

        (anchor_id, anchor_delta, anchor_dist) = (None, None, None)
        azone_id = a_db_id = None
        if len(data.payload) == 18 and data.payload[1] in (0x0, 0x1):  # SSRv0
            (anchor_id, anchor_delta, anchor_dist) = struct.unpack(
                "<IBB", data.payload[12:])
            anchor_dist = anchor_dist / 10
        elif len(data.payload) == 19 and data.payload[1] == 0x2:  # SSRv1
            (anchor_id, anchor_delta, anchor_rssi, anchor_cal) = struct.unpack(
                "<IBBB", data.payload[12:])
            anchor_dist = 10 ** ((anchor_cal - anchor_rssi) / (10 * 3.2))

        if anchor_id:
            # Anchor upsert
            (a_db_id, azone_id) = await conn.fetchrow(
                'INSERT into tags (bid, type) '
                'VALUES ($1, \'SecureLocationAnchor\') '
                'ON CONFLICT ON CONSTRAINT tags_bid_key '
                'DO UPDATE SET last_seen = (now() at time zone \'utc\') '
                'RETURNING id, zone_id',
                anchor_id)
            if not azone_id:
                # Create default zone for anchor if nonexistant
                (azone_id,) = await conn.fetchrow(
                    'INSERT INTO zones (name) VALUES ($1) RETURNING id',
                    f'Near SLA {b_id}')
                await conn.execute(
                    'UPDATE tags SET zone_id = $1 WHERE id = $2',
                    azone_id, a_db_id)

        await conn.fetch(
            'INSERT into log (tag_id, zone_id, listener_id, distance,'
            'variance, anchor_id, anchor_dist, anchor_ts_delta, reason)'
            'VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)',
            t_id, azone_id, self.listener_id, data.distance_cm / 100,
            round(data.variance / 2000, 1), a_db_id, anchor_dist, anchor_delta,
            None)

    async def process_relay_beacon(self, msg, conn):
        data = LABeaconSummary()
        data.ParseFromString(msg.data)
        # Convert to upsert when last_seen field is added?
        tag_insert = await conn.prepare(
            'INSERT into tags (mac, type, battery_pct) '
            'VALUES ($1, \'SmartRelay\', $2) RETURNING '
            'id, last_seen, (now() at time zone \'utc\'), alarm_active')
        tag_select = await conn.prepare(
            'SELECT id, last_seen, (now() at time zone \'utc\'), alarm_active '
            'FROM tags WHERE mac = $1 AND type = \'SmartRelay\'')
        tag_update = await conn.prepare(
            'UPDATE tags SET last_seen = $1, battery_pct = $3 WHERE id = $2')
        anchor_insert = await conn.prepare(
            'INSERT into tags (uuid, major, minor, type) '
            'VALUES ($1, $2, $3, \'LocationAnchor\') RETURNING id, zone_id')
        anchor_select = await conn.prepare(
            'SELECT id, zone_id FROM tags '
            'WHERE uuid = $1 AND major = $2 AND minor = $3')
        labeacon_log = await conn.prepare(
            'INSERT into log (tag_id, zone_id, listener_id, distance, '
            'variance, anchor_id, anchor_dist, anchor_ts_delta, reason)'
            'VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)')
        alarm_update = await conn.prepare(
            'UPDATE alarms SET last_ts = now() '
            'WHERE tag_id = $1 AND acknowledged = FALSE RETURNING id')
        listener_zone = await self._select_zone_id(conn)
        for b in data.reports:
            stats.increment("SR Reports")
            b_id = bytes(reversed(b.beacon_id)).hex()

            t = await tag_select.fetchrow(b_id)
            if not t:
                stats.increment('New SR')
                t = await tag_insert.fetchrow(b_id, b.battery_pct)
            t_id, t_lastseen, db_now, t_alarm = t[0], t[1], t[2], t[3]
            diff = (db_now - t_lastseen).seconds
            if diff > CONFIG['LAST_SEEN_RESOLUTION_SECS']:
                await tag_update.fetch(db_now, t_id, b.battery_pct)

            # Service alarm
            alarm_active = b.status == \
                           LABeaconSummary.LABeaconReport.ButtonStatus.PRESSED
            if alarm_active:
                alarm = await alarm_update.fetchrow(t['id'])
                if not alarm:
                    stats.increment('New Alarm')
                    await conn.fetch(
                        'INSERT INTO alarms (tag_id) VALUES ($1)', t['id'])
            if t_alarm != alarm_active:
                stats.increment('Alarm State Updated')
                await conn.fetch(
                    'UPDATE tags SET alarm_active = $1 WHERE id = $2',
                    alarm_active, t_id)

            if b.nearest == 0 and b.nearest_delta == 0 and b.nearest_dist == 0:
                # No current anchor
                stats.increment('Unanchored SR Packet')
                await labeacon_log.fetch(
                    t['id'], listener_zone, self.listener_id,
                    b.distance_cm / 100, round(b.variance / 2000, 1), None,
                    None, None, self._reason(b))
                continue
            # Reconstruct the iBeacon from the LA data
            major = b.nearest >> 16
            minor = b.nearest & 0xffff
            r = await anchor_select.fetchrow(CONFIG['LA_UUID'], major, minor)
            if not r:
                stats.increment('New LA')
                r = await anchor_insert.fetchrow(
                    CONFIG['LA_UUID'], major, minor)
            (a_id, azone_id) = r[0], r[1]
            if not azone_id:
                stats.increment('Autocreated Zone (LA)')
                s = await conn.fetchrow(
                    'INSERT INTO zones (name) VALUES ($1) RETURNING id',
                    f'Near LA {major}:{minor}')
                azone_id = s[0]
                await conn.execute(
                    'UPDATE tags SET zone_id = $1 WHERE id = $2',
                    azone_id, a_id)
            await labeacon_log.fetch(
                t['id'], azone_id, self.listener_id, b.distance_cm / 100,
                round(b.variance / 2000, 1), a_id, b.nearest_dist / 10,
                b.nearest_delta, self._reason(b))

    async def process_health_check(self, msg, conn):
        pass

    def error_received(self, exc: Exception) -> None:
        stats.increment("Connection Errors")
        print(f'Error received: {exc}')

    def connection_lost(self, exc: Exception) -> None:
        stats.decrement("Listener Connections")
        print("{} has disconnected".format(self.peer_name))


@attr.s
class QueuedPacket:
    msg: bytes = attr.ib()
    protocol: ListenerProtocol = attr.ib()
