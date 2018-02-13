#/bin/bash

#postgres -c "exec /usr/lib/postgresql/9.5/bin/postgres -D /etc/postgresql/9.5/main"



# This script is run by Supervisor to start PostgreSQL 9.1 in foreground mode

function shutdown()
{
    echo "Shutting down PostgreSQL"
    pkill postgres
}

if [ -d /var/run/postgresql ]; then
    chmod 2775 /var/run/postgresql
else
    install -d -m 2775 -o postgres -g postgres /var/run/postgresql
fi

# Allow any signal which would kill a process to stop PostgreSQL
trap shutdown HUP INT QUIT ABRT KILL ALRM TERM TSTP

runuser -l postgres -c "exec /usr/lib/postgresql/9.5/bin/postgres -D /etc/postgresql/9.5/main"

