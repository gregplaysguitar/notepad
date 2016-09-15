import os

FLASK_DEBUG = True
ASSETS_DEBUG = FLASK_DEBUG

HOST = os.environ.get('HOST')
PORT = int(os.environ.get('PORT')) if os.environ.get('PORT') else None
