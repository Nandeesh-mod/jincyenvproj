import os 
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.environ.get('MYSQL_USER', 'jincy')}:{os.environ.get('MYSQL_PASSWORD', '')}@{os.environ.get('MYSQL_HOST', 'localhost')}/{os.environ.get('MYSQL_DATABASE', 'wastemanage')}"

print(SQLALCHEMY_DATABASE_URI)