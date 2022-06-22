from os import environ

TOKEN = environ.get("TOKEN")
OWNER = environ.get("OWNER")
PARSE_MODE = environ.get("PARSE_MODE")
SECRET_WORD = environ.get("SECRET_WORD")
CHROME_LOCATION = environ.get("GOOGLE_CHROME_SHIM", None)
