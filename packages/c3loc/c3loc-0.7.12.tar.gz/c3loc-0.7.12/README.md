# Location Engine

## Prerequisites

Debian / Ubuntu:

*Tested on Ubuntu 20.04.4 LTS and Debian 11*

``` sh
apt update
apt install -y \
	postgresql \
	nginx \
	python3-psycopg2 \
	python3-pip \
	python3-venv \
	liblzo2-dev \
	libpq-dev \
	build-essential
```

Redhat 8:

*Tested on Rocky Linux 8.5*

``` sh
dnf update -y
dnf module -y switch-to postgresql:12
dnf install -y postgresql-server gcc postgresql-devel python39-devel lzo-devel nginx
postgresql-setup initdb
systemctl enable postgresql
systemctl start postgresql
setenforce 0
sed -i -e 's/=enforcing/=permissive/' /etc/selinux/config

```



## Initialize Database

``` sh
sudo -u postgres -i createdb c3loc  # Create new database "c3loc"
sudo -u postgres -i createuser c3loc  # Create a new non-admin db user "c3loc"

```

## Location Engine

``` sh
useradd -m c3loc  # Create non-root user
sudo -s -u c3loc  # Switch to new user
cd  #  Go to new user home dir
python3 -m venv c3loc-env  # Create a virtual python environment, separate from system packages
. ./c3loc-env/bin/activate  # Activate environment 
pip install --upgrade pip
pip install wheel  # Enables download of binary packages
pip install c3loc  # Download and install Location engine packages
find c3loc-env/lib/python*/site-packages/c3loc -name "alembic" -type d -exec ln -s {} . \;
cp ./c3loc-env/lib/python*/site-packages/c3loc/alembic.ini .  # Copy database migration template
sed -i -e 's,^sqlalchemy\.url.*,sqlalchemy.url = postgresql://c3loc@/c3loc,' \
	alembic.ini  # Update migration template
alembic upgrade head  # Deploy db schema to empty database
exit  # Return to root user shell
```

## Nginx proxy

``` sh
if [ ! -f /etc/redhat_version ]; then
	# Debian and redhat have different default config strategies, this will
	# homogenizes non-redhat to redhat style
	mkdir -p /etc/nginx/default.d
	sed -i -e '/^[^#]*server_name.*\;/a \\tinclude default.d/*.conf\;' /etc/nginx/sites-available/default
fi

cat <<EOF > /etc/nginx/default.d/c3loc.default.conf
location /api {
     proxy_pass http://localhost:10999/api;
}

location /api2/ {
    rewrite /api2/(.*) /\$1  break;
    proxy_pass http://localhost:11999/;
}
EOF
nginx -t && systemctl enable nginx && systemctl restart nginx  # Enable and start nginx

```


## Install startup files

You may want to increase the *API\_RESULT\_LIMIT* variable below (2 locations) if
the frontend/client doesn't support pagination.


``` sh
cat <<EOF > /etc/systemd/system/c3loc_ingest.service
[Unit]
Requires=postgresql.service
Description=Ingest service for c3location [c3loc]

[Service]
User=c3loc
WorkingDirectory=/home/c3loc
Environment=DB_NAME=c3loc
Environment=PYTHONUNBUFFERED=1
Environment=MAX_DB_CONNECTIONS=8
ExecStart=/home/c3loc/c3loc-env/bin/c3loc_ingest -p 9999
Restart=always

[Install]
WantedBy=multi-user.target
EOF
systemctl enable c3loc_ingest && systemctl start c3loc_ingest

cat <<EOF > /etc/systemd/system/c3loc_api.service
[Unit]
Requires=postgresql.service
Description=API service for c3location

[Service]
User=c3loc
WorkingDirectory=/home/c3loc
Environment=DB_NAME=c3loc
Environment=PYTHONUNBUFFERED=1
Environment=API_RESULT_LIMIT=1000
ExecStart=/home/c3loc/c3loc-env/bin/c3loc_api -p 10999
Restart=always

[Install]
WantedBy=multi-user.target
EOF
systemctl enable c3loc_api && systemctl start c3loc_api

cat <<EOF > /etc/systemd/system/c3loc_api2.service
[Unit]
Requires=postgresql.service
Description=New API service for c3location [c3loc]

[Service]
User=c3loc
WorkingDirectory=/home/c3loc
Environment=DB_NAME=c3loc
Environment=PYTHONUNBUFFERED=1
Environment=API_RESULT_LIMIT=1000
ExecStart=/home/c3loc/c3loc-env/bin/uvicorn \
        --host 0.0.0.0 --port=11999 \
        --root-path="/api2" --limit-concurrency=100 c3loc.api2.main:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF
systemctl enable c3loc_api2 && systemctl start c3loc_api2
```

## Testing

At this point, you should be able to access the api servers at the following urls:

```
http://<ip addr>/api
http://<ip addr>/api2/proximity
```

If you have 200 responses, then the services are running as intended. You can
use the following commands to check the logs for each service:

``` sh
journalctl -eu c3loc_ingest
journalctl -eu c3loc_api
journalctl -eu c3loc_api2
```
