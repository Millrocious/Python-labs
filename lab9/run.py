import pprint
from os import getenv

from dotenv import dotenv_values

from app import create_app

app = create_app(dotenv_values(".env")['FLASK_CONFIG'])

if __name__ == '__main__':
    app.run()
