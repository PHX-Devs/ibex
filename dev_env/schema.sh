# install ibex schema
runuser -l postgres -c "psql -f /var/ibex/dev_env/create_database.sql"
runuser -l postgres -c "psql -U ibex -f /var/ibex/dev_env/ibex_schema.sql"