#!/bin/bash

cd /home/root/ml_corners_predictor/DatabaseCreation

mvn liquibase:update -Dliquibase.url=jdbc:mysql://localhost:3306/football_data -Dliquibase.username=root -Dliquibase.password=secret -Dliquibase.changeLogFile=src/main/resources/db/changelog-master.yaml -Dliquibase.driver=com.mysql.cj.jdbc.Driver