import logging
from scanner.scan import CollectionScanner

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    scanner = CollectionScanner("data/collection.db", "temp")
    scanner.scan_covers()