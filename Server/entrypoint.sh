#!/bin/bash

service mysql stop
usermod -d /var/lib/mysql/ mysql
service mysql start 


mysql -u root -p"secret" -e "CREATE DATABASE IF NOT EXISTS football_data"
mysql -u root -p"secret" -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'secret'"
mysql -u root -p"secret" -e "FLUSH PRIVILEGES"

bash /home/root/ml_corners_predictor/Server/Scripts/update_liquibase_changes.sh

exec tail -f /dev/null


#jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
#liquibase update --url=jdbc:mysql://localhost:3306/football_data --username=root --password=secret --changelog-file=/home/root/ml_corners_predictor/DatabaseCreation/src/main/resources/db/changelog-master.yaml --driver=com.mysql.cj.jdbc.Driver