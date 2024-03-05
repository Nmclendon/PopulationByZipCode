# Nicholas McLendon
# CNE 350
# Winter 2024.
# Restful interface that has search and update options for navigating a Zip code database on Phpmyadmin.

# Special thanks to Justin Ellis for providing the foundation for this code. This is mostly just a repurposed version of
# his rest_web.py States project found here: https://github.com/ellisju37073/States/tree/main/states/rest_web

#https://stackoverflow.com/questions/8211128/multiple-distinct-pages-in-one-html-file
#https://stackoverflow.com/questions/902408/how-to-use-variables-in-sql-statement-in-python
#https://stackoverflow.com/questions/1081750/python-update-multiple-columns-with-python-variables
#https://stackoverflow.com/questions/7478366/create-dynamic-urls-in-flask-with-url-for
#https://github.com/vimalloc/flask-jwt-extended/issues/175


from getpass import getpass
from mysql import connector
from flask import Flask, redirect, url_for, request, render_template
import mysql.connector

app = Flask(__name__, static_url_path='')
# Set the SERVER_NAME directly in app config
app.config['SERVER_NAME'] = 'YourPiIPaddressHere:5000'

#connect to database
conn = mysql.connector.connect(user='root', password=getpass("Enter your MariaDB root user password: "),
                                  host='127.0.0.1',
                                  database='YourDataBaseNameHere',
                               buffered = True)
cursor = conn.cursor()

#Search state database
@app.route('/searchZip/<searchZip>')
def searchZip(searchZip):
    # Get data from database
    cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s", [searchZip])
    test = cursor.rowcount
    if test != 1:
        return searchZip + " was not found"
    else:
        searched = cursor.fetchall()
        return 'Success! Here you go: %s' % searched

#update state database population for a specified state
@app.route('/updateZipPop/<updateZip> <updatePop>')
def updateZipPop(updateZip, updatePop):
    cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s", [updateZip])
    test = cursor.rowcount
    if test != 1:
        return updateSTATE + " was not found"
    else:
        cursor.execute("UPDATE `zipcodes` SET Population = %s WHERE zip= %s;", [updatePop,updateZip])
        cursor.execute("SELECT * FROM `zipcodes` WHERE zip= %s and Population=%s", [updateZip,updatePop])
        test1 = cursor.rowcount
        if test1 != 1:
            return updateZip + "  failed to update"
        else:
            return 'Population has been updated successfully for State: %s' % updateZip

#update webpage
@app.route('/update',methods = ['POST'])
def update():
       user = request.form['uzip']
       user2 = request.form['upop']
       return redirect(url_for('updateZipPop', updateZip=user, updatePop=user2, _external=True))

#search page
@app.route('/search', methods=['GET'])
def search():
       user = request.args.get('sZip')
       return redirect(url_for('searchZip', searchZip=user, _external=True))


#root of web server and gots to template (login.html)
@app.route('/')
def root():
   return render_template('login.html')

#main
if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True)


