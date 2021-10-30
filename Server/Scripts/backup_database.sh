#!/bin/bash

mysqldump -v --opt --no-create-info --skip-triggers --default-character-set=utf8 -u root -p"secret" football_data --ignore-table=football_data.DATABASECHANGELOG --ignore-table=football_data.DATABASECHANGELOGLOCK --ignore_table=football_data.season_leagues_url --ignore_table=football_data.stadiums > Server/Backups_MySQL/backup_database_`date +%Y%m%d_%H%M%S`.sql