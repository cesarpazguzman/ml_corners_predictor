# ml_corners_predictor


1- sudo apt-get install python-pytest 
2- pip install mysql-connector-python
3- pip install pandas
4- pip install SQLAlchemy
5- pip install selenium
6- pip install bs4
7- pip install webdriver-manager
8- pip install unidecode
9- Chromedriver for selenium:
    - sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add 
    - sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" 
    - sudo apt -y update 
    - sudo apt -y install google-chrome-stable 
    - wget https://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip
    - sudo apt-get install unzip
    - unzip chromedriver_linux64.zip 
    - sudo mv chromedriver /usr/bin/chromedriver 
    - sudo chown root:root /usr/bin/chromedriver 
    - sudo chmod +x /usr/bin/chromedriver
10- pip install pymysql
11- Database MySQL
    - sudo apt-get install mysql-server
    - sudo service mysql stop
    - sudo usermod -d /var/lib/mysql/ mysql
    - sudo service mysql start    
    - sudo mysql_secure_installation
    - Configure mysql users:
        - ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'password';
        - FLUSH PRIVILEGES;
        - CREATE USER 'cesar'@'%' IDENTIFIED BY '***password***';
        - GRANT ALL PRIVILEGES ON *.* TO 'cesar'@'%';
        - FLUSH PRIVILEGES;
        - CREATE DATABASE football_data