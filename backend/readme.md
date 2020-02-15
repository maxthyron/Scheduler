# Backend setup

1.  **Install Postgresql:**

    1.  **Arch-linux:**
        1.  `sudo pacman -S postgresql`
        2.  Change user to `postgres` with  `su -l postgres` or `sudo -iu postgres`
        3.  Initialize Postgres database cluster: `initdb -E UTF8 -D /var/lib/postgres/data`
        4.  Start Postgres service: `pg_ctl -D /var/lib/postgres/ -l logfile start`
    2.  **Mac OS:**
        1.  `brew install postgresql`
        2.  Start Postgres service: `brew services start postgresql`
        3.  Initialize Postgres database (not sure if this is required): `initdb /usr/local/var/postgres -E utf8`

2.  **Install system dependencies:**

    1.  **Usual install** (still needs to be determined):
        -   `python3-dev` (?)
        -   `openssl-dev libffi-dev` (bcrypt dependencies)
        -   `gcc` (?)
    2.  In case of **CI (Alpine OS)** and **Deployment**(presumably):
        *   `musl-dev`
        *   `postgresql-dev`
        *   `libxml2-dev libxslt-dev` (lxml dependencies)
        *   `libc-dev`
        *   `py3-lxml`- needed to speed up the build time, do not install directly with `pip install lxml`, because it will start to build the library and will stuck for a long time(no guarantee that it will actually build it)

3.  Install **Python requirements**: `pip install -r requirements.txt ` or `pip3 install -r requirements.txt`

    In case of **Mac OS**, for some reason, `psycopg2` ***won't*** install without additional environment variables passed:

    `export LDFLAGS="-L/usr/local/opt/openssl/lib" export CPPFLAGS="-I/usr/local/opt/openssl/include"`

4.  Initialize project database with script (may still be buggy): `./create_env.sh`

5.  Migrate database from Django: `python manage.py migrate` or `python3 manage.py migrate`

6.  Run python script to fill the database with occupied auditoriums: `python run.py` or `python3 run.py`. 

    App can be launched at the same time, the database will gradually fill up. There seems to be a bug: for some reason table won't show up until the whole database is filled (this wasn't present in the past).

7.  Start the app with either `python3 manage.py runserver` or `gunicorn dbproject.wsgi`

## Additional:

**Nginx** is working, but it messes up the user experience with caching and not updating data on user actions. Needs to be fixed. Also, for now, it works only for backend, this may change in the future.

### Nginx(currently works only for Mac OS, other OSs have to deal with stuff by their own):

1.  `./configure_nginx.sh nginx.conf` - updates nginx version, adds additional features(http2, status, additional headers?)
2.  Starts with `nginx -c nginx.conf`. Check for the right config file: `nginx -t -c nginx.conf`

