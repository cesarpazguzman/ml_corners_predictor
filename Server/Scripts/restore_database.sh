#!/bin/bash

mysql -u root -p"secret" -e "DELETE FROM football_data.matches"
mysql -u root -p"secret" -e "DELETE FROM football_data.finished_matches"
mysql -u root -p"secret" -e "DELETE FROM football_data.active_matches"
mysql -u root -p"secret" -e "DELETE FROM football_data.stats_matches"

mysql -u root -p"secret" football_data < Backups_MySQL/backup_database_20211030_155600.sql