from flask import Flask
import os

instance = os.getenv('PY_COLLECTION_ENV', 'development')

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('webapp.config')
app.config.from_pyfile('{0}.cfg'.format(instance), silent=False)

import routes