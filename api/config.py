import os

if 'DATABASE_URL' in os.environ:
    DATA_SOURCE = os.environ['DATABASE_URL']
else:
    DATA_SOURCE = 'postgresql://admin:admin@localhost/db'
