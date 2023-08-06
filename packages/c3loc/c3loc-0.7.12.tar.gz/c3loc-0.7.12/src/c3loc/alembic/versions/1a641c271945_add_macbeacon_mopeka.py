"""add macbeacon mopeka

Revision ID: 1a641c271945
Revises: 1100e9db1a0d
Create Date: 2023-02-16 19:32:28.088031

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '1a641c271945'
down_revision = '1100e9db1a0d'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
CREATE OR REPLACE FUNCTION def_tag_name() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.name IS NOT NULL OR NEW.name != ''
       THEN RETURN NEW;
    ELSIF NEW.type = 'iBeacon' THEN
        NEW.name := 'iBeacon ' || NEW.uuid || ':' || NEW.major || ':' || NEW.minor;
    ELSIF NEW.type = 'LocationAnchor' THEN
            NEW.name := 'Location Anchor ' || NEW.major || ':' || NEW.minor;
    ELSIF NEW.type = 'SmartRelay' THEN
            NEW.name := 'SmartRelay ' || NEW.mac;
    ELSIF New.type = 'SecureSmartRelay' THEN
            NEW.name := 'SecureSmartRelay ' || NEW.bid;
    ELSIF New.type = 'SecureLocationAnchor' THEN
            NEW.name := 'SecureLocationAnchor ' || NEW.bid;
    ELSIF New.type = 'AlertWet' THEN
            NEW.name := 'AlertWet ' || NEW.bid;
    ELSIF New.Type = 'MacBeacon' THEN
            NEW.name := 'MacBeacon ' || NEW.bid;
    END IF;
    return NEW;
END
$$;""")  # noqa: E501
    op.execute("""
DO $$ BEGIN
    ALTER TYPE tag_type ADD VALUE 'MacBeacon';
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;""")  # noqa: E501


def downgrade():
    op.execute("""
CREATE OR REPLACE FUNCTION def_tag_name() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.name IS NOT NULL OR NEW.name != ''
       THEN RETURN NEW;
    ELSIF NEW.type = 'iBeacon' THEN
        NEW.name := 'iBeacon ' || NEW.uuid || ':' || NEW.major || ':' || NEW.minor;
    ELSIF NEW.type = 'LocationAnchor' THEN
            NEW.name := 'Location Anchor ' || NEW.major || ':' || NEW.minor;
    ELSIF NEW.type = 'SmartRelay' THEN
            NEW.name := 'SmartRelay ' || NEW.mac;
    ELSIF New.type = 'SecureSmartRelay' THEN
            NEW.name := 'SecureSmartRelay ' || NEW.bid;
    ELSIF New.type = 'SecureLocationAnchor' THEN
            NEW.name := 'SecureLocationAnchor ' || NEW.bid;
    ELSIF New.type = 'AlertWet' THEN
            NEW.name := 'AlertWet ' || NEW.bid;
    END IF;
    return NEW;
END
$$;""")  # noqa: E501
