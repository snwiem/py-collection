import logging
import sys
from loader.loader import CollectionLoader

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    CollectionLoader.load_collection("C:\Users\Sebastian\Documents\DVD Profiler\Collection.xml", "data/collection.db")