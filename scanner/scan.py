import logging
import urllib2
from PIL import Image
import os
from dao import SimpleDao

class CollectionScanner(object):

    def __init__(self, database, target_dir):
        self.database = database
        self.target_dir = target_dir

    def download_image(self, img, dest):
        url = "http://www.invelos.com/mpimages/{0}/{1}".format(img[:2], img)
        res = urllib2.urlopen(url)
        sc = res.code
        ct = res.headers['Content-Type']
        logging.debug("[{}] code: {}, type: {}".format(img, sc, ct))
        b = 0
        with open(dest, 'wb') as fp:
            while True:
                chunk = res.read(1024)
                b += len(chunk)
                if not chunk:
                    break
                fp.write(chunk)
        logging.debug("[{}] downloaded {} bytes".format(img, b))

    def retrieve_image(self, res):
        img = os.path.basename(res)
        if not os.path.isfile(res):
            try:
                self.download_image(img, res)
                logging.debug("Successfully retrieved '{0}'".format(img))
            except Exception, e:
                logging.exception(e)
                #logging.error("Failed to retrieve '{0}': {1}".format(img), e)
        else:
            logging.debug("Skipping existent {0}".format(img))

    @staticmethod
    def resize_image(res):
        img = os.path.basename(res)
        if os.path.isfile(res):
            im = Image.open(res)
            logging.info("[{}] format: {}, size: {}, mode: {}".format(img, im.format, im.size, im.mode))
            w, h = im.size
            if 150 != w or 210 != h:
                im = im.resize((150, 210), Image.ANTIALIAS)
                im.save(res)
                logging.debug("[{}] resized".format(img))

    def process_cover(self, uid):
        img = "{0}f.jpg".format(uid)
        res = os.path.join(self.target_dir, img)
        self.retrieve_image(res)
        self.resize_image(res)

    def scan_covers(self):
        if not os.path.isdir(self.target_dir):
            os.mkdir(self.target_dir)
        dao = SimpleDao(self.database)
        dao.process_all_uids(self.process_cover)