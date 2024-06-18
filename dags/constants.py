import configparser
import os

parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), 'config/config.conf'))

# [database]
DATABASE_HOST =  parser.get('database', 'database_host')
DATABASE_NAME =  parser.get('database', 'database_name')
DATABASE_PORT =  parser.get('database', 'database_port')
DATABASE_USER =  parser.get('database', 'database_username')
DATABASE_PASSWORD =  parser.get('database', 'database_password')

# [env]
URL =  parser.get('env', 'url')

# [email]
EMAIL_TO = parser.get('email', 'email_to')
SMTP_USER = parser.get('email', 'smtp_user')
SMTP_PASSWORD = parser.get('email', 'smtp_password')
SMTP_MAIL_FROM = parser.get('email', 'smtp_mail_from')
