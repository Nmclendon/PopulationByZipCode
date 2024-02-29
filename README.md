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
- There are a few ways to accomplish this task. I will be using a python script that imports the data from the .csv file on my Pi into a MariaDB database.

  # Project to continue from here.
