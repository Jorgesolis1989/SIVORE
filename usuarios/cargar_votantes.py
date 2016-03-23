# Full path and name to your csv file
csv_filepathname="/home/sivore/votantes.csv"
# Full path to your django project directory
your_djangoproject_home="/home/martha/SIVORE/"

import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

#from zips.models import ZipCode
from usuarios.models import User

import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

for row in dataReader:
    if row[0] != 'USUARIOS': # Ignore the header row, import everything else
        usuario = User()
        usuario.username = row[0]
        usuario.first_name = row[1]
        usuario.last_name= row[2]
        usuario.email = row[3]
        usuario.save()