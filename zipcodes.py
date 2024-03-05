# Nicholas McLendon
# CNE 350
# Winter 2024.

from getpass import getpass
import numpy
import pandas
from sqlalchemy import create_engine

hostname="127.0.0.1"
uname="root"
pwd=getpass("Enter your MariaDB root user password: ")
dbname="YourDataBaseNameHere"

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
.format(host=hostname, db=dbname, user=uname, pw=pwd))

tables = pandas.read_csv(r"Your/File/Path.csv")

connection=engine.connect()
tables.to_sql('zipcodes',con = engine, if_exists = 'replace')
connection.close()

print(tables)
