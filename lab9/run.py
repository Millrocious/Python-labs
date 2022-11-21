from dotenv import dotenv_values
from app import create_app

if __name__ == '__main__':
    create_app(dotenv_values(".env")['FLASK_CONFIG']).run()
