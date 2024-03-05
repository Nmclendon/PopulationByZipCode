# PopulationByZipCode
This project uses Flask to launch a web server on port 5000. From the web page users will be able to query the DB to get information and update the DB if needed. This project uses XML or JSON-packed messages to transport data. This project is hosted on a Raspberry Pi zero W. **All of the steps will be done using the terminal on the Raspberry Pi unless specifically stated otherwise.**

So far this documentation outlines the steps for setting up a LAMP (Linux, Apache, MariaDB, PHP) stack on a Raspberry Pi, securing the MariaDB root password, transferring a .csv file from a Windows machine to the Raspberry Pi, and importing the data into a MariaDB database.  **This project is ongoing and so this documentation is a work in progress and will be built upon as continue working.**

## Setting Up LAMP Stack on Raspberry Pi with MariaDB

This section covers the installation and configuration of the LAMP stack (Linux, Apache, MariaDB, PHP) on a Raspberry Pi. You will need to access the terminal on your Raspberry Pi to do this project, this can be done via SSH, VNC, or any other preferred method.

1. **Update the System**:
- Updates the package lists and upgrades the installed packages.

In the pi terminal:
**sudo apt update -y && sudo apt upgrade -y**

2. **Install Apache**:
- Installs the Apache web server.

In the pi terminal:
**sudo apt install apache2 -y**

3. **Install MariaDB**:
- Installs the MariaDB database server.

In the pi terminal:
**sudo apt install mariadb-server -y**

4. **Secure MariaDB Installation (optional)**:
- Runs the sql_secure_installation script to secure the MariaDB installation and set a root password.

In the pi terminal:
**sudo mariadb_secure_installation**
(Follow the prompts/installation wizard.)

5. **Install PHP, PHP SQL extension, and phpMyAdmin**:
- Installs PHP, the PHP SQL extension.

In the pi terminal:
**sudo apt install php libapache2-mod-php php-mysql -y**
**sudo apt install phpmyadmin -y** (This command will launch an install wizard and prompt you for some input)

During the installation process, you will be prompted to configure phpMyAdmin. Choose Apache as the web server that should be automatically configured to run phpMyAdmin, it may prompt you for your MariaDB root username (this will just be **root**) and then ask you to provide your MariaDB root password when prompted **(only enter a password if you did step 4: Secure MariaDB Installation (optional), otherwise leave the password blank)**

6. **Configure Apache for phpMyAdmin**:
- Modifies the Apache configuration for phpMyAdmin to allow access from other computers on the network.

In the pi terminal:
**sudo nano /etc/apache2/conf-available/phpmyadmin.conf** (this will open phpmyadmin.conf in a text editor)

In the text editor add the text **Require all granted** anywhere inside the <Directory /usr/share/phpmyadmin> section of phpmyadmin.conf. **(NOT to be confused with anywhere in the file!!! It MUST at least be in the Directory /usr/share/phpmyadmin section!)**

Afterwards you will need to enable the changes and restart Apache.

In the pi terminal:
**sudo ln -s /etc/apache2/conf-available/phpmyadmin.conf /etc/apache2/conf-enabled/phpmyadmin.conf**

(Note. You will probabaly get a message saying that this was unable to complete because the destination file already exists, in which case you should just skip this command and restart apache2 by using the command below. This was added for edge cases where the configuration file was not automatically generated.)

In the pi terminal:
**sudo systemctl restart apache2**

7.**Securing MariaDB Root Password**
- The phpMyAdmin configuration is now set not to allow users to log in without a password, this includes the root user. This step configures a a password for the root user. If you did **step 4 Secure MariaDB Installation (optional)**, then you can skip this step and will login using the same password you set in step 4.

Log into the MariaDB database server using the MariaDB command-line client.

In the pi terminal:
**sudo mariadb -u root**

Your shell prompt should change to look like this:
**MariaDB [(none)]>**

Set Root Password

In the MariaDB prompt:
**ALTER USER 'root'@'localhost' IDENTIFIED BY 'type your password here';**

From now on when logging into MariaDB you will use the sudo **mariadb -u root -p** command and enter the password when prompted.

## Transfering data to your Pi and uploading it to your database

1. **Transferring .csv File from Windows Machine to Raspberry Pi**
- This covers transferring a .csv file from a Windows machine to a Raspberry Pi using PSCP (PuTTY Secure Copy Protocol).

Open a command propmt on the Windows machine that contains the data you want to transfer.

In the command prompt:
**pscp C:\path\to\your\file.csv yourUsername@yourPisIPv4Address:/path/to/destination**

**(Be sure to replace YourUsername@YourPisIPv4Address with the proper username and ip address for your device, and \path\to\your\file.csv and /path/to/destination with the proper file paths on your respective machines.)**

2. **Importing Data into MariaDB Database**
- There are a few ways to accomplish this task. I will be using a python script named zipcodes.py that reads zip code information from a CSV file (CNE350_zip_code_database.csv) into a Pandas DataFrame called tables and writes data from tables to a table named zipcodes in my population_by_zip database.

First you will need to modify lines 13 and 18 in zipcodes.py to match the name of your database and the path on your device to your .csv file run **zipcodes.py** you should see some output once it's completed.

Something along the lines of:

Enter your MariaDB root user password:
* _ zip  Population
* 0        501         562
* 1        544           0
* 2        601           0
* 3        602           0
* 4        603           0
* ...      ...         ...
* 42627  99926        1140
* 42628  99927          48
* 42629  99928        1530
* 42630  99929        2145
* 42631  99950         262

* [42632 rows x 2 columns]


## Starting your Flask server
1. **Modify rest_web.py**
- You will need to modify lines 23 and 26-28 to match your own Raspberry Pi IP address and your own mysql.connector.connect configuration in order to properly connect to your database.

2. **Modify login.html**
- You will need to modify lines 3 and 8 in login.html to match the IP address of your Raspberry Pi or you will not be properly redirected when you use the search and update features on the web page. You should keep the port as 5000 since Flask runs on port 5000 in development mode by default.

3. **Start the Flask server** 
- Do this by running **rest_web.py** which is located in the rest_web subdirectory of this project.

You should see some output that looks like:

Enter your MariaDB root user password:
 * Serving Flask app "rest_web" (lazy loading)
 * Environment: production
 *  WARNING: This is a development server. Do not use it in a production deployment.
 *  Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
192.168.0.37 - - [05/Mar/2024 10:30:34] "GET / HTTP/1.1" 200 -

4. **Test your web application**
- Make sure everything is working properly by opening a browser on a device that's on the same network as your Pi and typing **http://YourPiIPaddressHere:5000** (replacing YourPiIPaddressHere with the IP address of your Raspberry Pi) You should be brough to a plain web page with the search and update feilds.

Try running a few searches and updates and verify that the information coming back is correct.

