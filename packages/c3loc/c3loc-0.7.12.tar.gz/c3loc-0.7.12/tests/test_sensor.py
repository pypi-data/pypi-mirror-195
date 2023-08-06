from c3loc.ingest.sensors import SensorReport


def test_field_count():
    assert len(SensorReport.parse(b'').fields) == 0
    assert len(SensorReport.parse(b'\x01\x02\x00\x00').fields) == 1
    assert len(SensorReport.parse(b'\x02\x01\x00\x01\x01\x00').fields) == 2


def test_sensor_field():
    batt = SensorReport.parse(b'\x00\x01\x00').fields[0]
    assert batt.tag == 0
    assert batt.length == 1
    assert batt.value == b'\x00'
    temp = SensorReport.parse(b'\x01\x02\x00\x00').fields[0]
    assert temp.tag == 1
    assert temp.length == 2
    assert temp.value == b'\x00\x00'
