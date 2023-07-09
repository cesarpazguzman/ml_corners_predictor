# ml_corners_predictor


1- sudo apt-get install python-pytest <br/>
2- pip install mysql-connector-python <br/>
3- pip install pandas <br/>
4- pip install SQLAlchemy <br/>
5- pip install selenium <br/>
6- pip install bs4 <br/>
7- pip install webdriver-manager <br/>
8- pip install unidecode <br/>
9- Chromedriver for selenium: <br/>
    - sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add <br/>
    - sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" <br/>
    - sudo apt -y update <br/>
    - sudo apt -y install google-chrome-stable <br/>
    - wget https://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip <br/>
    - sudo apt-get install unzip <br/>
    - unzip chromedriver_linux64.zip <br/>
    - sudo mv chromedriver /usr/bin/chromedriver <br/>
    - sudo chown root:root /usr/bin/chromedriver <br/>
    - sudo chmod +x /usr/bin/chromedriver <br/>
10- pip install pymysql <br/>
11- Database MySQL <br/>
    - sudo apt-get install mysql-server <br/>
    - sudo service mysql stop <br/>
    - sudo usermod -d /var/lib/mysql/ mysql <br/>
    - sudo service mysql start <br/>
    - sudo mysql_secure_installation <br/>
    - Configure mysql users: 
        - ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'password'; <br/>
        - FLUSH PRIVILEGES; <br/>
        - CREATE USER 'cesar'@'%' IDENTIFIED BY '***password***'; <br/>
        - GRANT ALL PRIVILEGES ON *.* TO 'cesar'@'%'; <br/>
        - FLUSH PRIVILEGES; <br/>
        - CREATE DATABASE football_data <br/>
12- Install jupyter <br/>
    - cd ~ <br/>
    - wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh <br/>
    - chmod +x Miniconda3-latest-Linux-x86_64.sh <br/>
    - sh Miniconda3-latest-Linux-x86_64.sh <br/>
    - rm Miniconda3-latest-Linux-x86_64.sh <br/>
