#!/bin/bash
# entrypoint.sh

# Check if migrations and superuser creation have already been done
if [ -f /tmp/initialized.flag ]; then
    echo "Migrations and superuser creation have already been done. Skipping."
else
    function check_mysql {
        python - <<END
import os
import MySQLdb
import time

db_host = 'mysql'
db_port = 3306

while True:
    try:
        conn = MySQLdb.connect(
            db=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            passwd=os.environ["DB_PASSWORD"],
            host=db_host,
            port=db_port,
        )
        conn.close()
        print("MySQL is ready.")
        break
    except MySQLdb.OperationalError as e:
        print(f"Waiting for MySQL to be ready... {e}")
        time.sleep(2)
END
    }

    # Wait for the MySQL container to be ready
    check_mysql

    # Apply migrations
    python manage.py migrate

    # Set environment variables for superuser creation
    export DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-password}
    export DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-athul}
    export DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-athul@example.com}

    # Create the superuser non-interactively
    python manage.py createsuperuser --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL --noinput

    # Mark that migrations and superuser creation have been done
    touch /tmp/initialized.flag
fi

# Start the development server
python manage.py runserver 0.0.0.0:8000
