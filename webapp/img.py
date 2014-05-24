import logging
import urllib
from PIL import Image
from flask import send_file, make_response
from webapp import app
import os, tempfile

def get_remote_image(category, resource, target):
    src = "http://www.invelos.com/mpimages/"+category+"/"+resource
    fi, path = tempfile.mkstemp(prefix='ic-')
    try:
        urllib.urlretrieve(src, path)
        img = Image.open(path)
        img.resize((160, 200), Image.ANTIALIAS)
        img.save(target)
        return target
    finally:
        os.close(fi)

@app.route('/img/<string:resource>')
def send_image(resource):
    #logging.debug("Root_Path: {}, Static: {}".format(app.root_path, app.static_folder))
    filename = os.path.join(app.config['IMAGE_TEMP'], resource)
    if not os.path.isfile(filename):
        filename = os.path.join(app.static_folder, 'img', 'no_cover.jpg')
    #    # get it from remote
    #    filename = get_remote_image(category, resource, filename)
    return send_file(filename, mimetype='application/jpg')
