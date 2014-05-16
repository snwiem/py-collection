import abc
from xml import sax
import collections


class CollectionContentHandler(sax.ContentHandler):

    FIELDS = {
        'ID': 'id',
        'UPC': 'upc',
        'Title': 'title',
        'OriginalTitle': 'original_title',
        'SortTitle': 'sort_title',
        'Overview': 'overview',
        'Rating': 'rating',
        'RunningTime': 'length',
        'ProductionYear': 'year'
    }

    def __init__(self):
        sax.ContentHandler.__init__(self)
        self.level = 0
        self.buffer = ''
        self.stack = collections.deque()

    @abc.abstractmethod
    def handle_movie(self, obj):
        pass

    @staticmethod
    def create_structure():
        return {
            'genres': [],
            'studios': [],
            'companies': [],
            'actors': [],
            'credits': []
        }

    def startElement(self, name, attrs):
        self.level += 1
        if 2 == self.level and name == 'DVD':
            self.stack.clear()
            self.stack.append(self.create_structure())
        elif 4 == self.level and name == 'Actor':
            self.stack[-1]['actors'].append({
                'firstname': attrs.getValue('FirstName'),
                'middlename': attrs.getValue('MiddleName'),
                'lastname': attrs.getValue('LastName'),
                'birthyear': attrs.getValue('BirthYear'),
                'role': attrs.getValue('Role')
            })
        elif 4 == self.level and name == 'Credit':
            self.stack[-1]['credits'].append({
                'firstname': attrs.getValue('FirstName'),
                'middlename': attrs.getValue('MiddleName'),
                'lastname': attrs.getValue('LastName'),
                'birthyear': attrs.getValue('BirthYear'),
                'credit_type': attrs.getValue('CreditType'),
                'credit_subtype': attrs.getValue('CreditSubtype')
            })
        # always reset the interal character buffer on new tag
        self.buffer = ''

    def endElement(self, name):
        if 2 == self.level and name == 'DVD':
            obj = self.stack.pop()
            #logging.debug(obj)
            self.handle_movie(obj)
        elif 3 == self.level and name in CollectionContentHandler.FIELDS:
            self.stack[-1][CollectionContentHandler.FIELDS[name]] = self.buffer.strip()
        elif 4 == self.level and name == 'Genre':
            self.stack[-1]['genres'].append(self.buffer.strip())
        elif 4 == self.level and name == 'Studio':
            self.stack[-1]['studios'].append(self.buffer.strip())
        elif 4 == self.level and name == 'MediaCompany':
            self.stack[-1]['companies'].append(self.buffer.strip())
        self.level -= 1

    def characters(self, content):
        self.buffer += content


