import logging
import xml
import sys
from .dao import SimpleDao
from .handler import CollectionContentHandler


class MovieHandler(CollectionContentHandler):

    def __init__(self, dao):
        CollectionContentHandler.__init__(self)
        self.dao = dao

    def handle_movie(self, obj):
        movie_id = self.dao.insert_movie(obj)
        for g in obj['genres']:
            genre_id = self.dao.select_value_id('genres', g)
            if not genre_id:
                genre_id = self.dao.insert_value('genres', g)
            self.dao.map_value_id('genres', 'genre_id', movie_id, genre_id)
        for s in obj['studios']:
            studio_id = self.dao.select_value_id('studios', s)
            if not studio_id:
                studio_id = self.dao.insert_value('studios', s)
            self.dao.map_value_id('studios', 'studio_id', movie_id, studio_id)
        for c in obj['companies']:
            company_id = self.dao.select_value_id('companies', c)
            if not company_id:
                company_id = self.dao.insert_value('companies', c)
            self.dao.map_value_id('companies', 'company_id', movie_id, company_id)
        for a in obj['actors']:
            person_id = self.dao.select_person(a)
            if not person_id:
                person_id = self.dao.insert_person(a)
            self.dao.map_role(movie_id, person_id, a['role'])
        for c in obj['credits']:
            person_id = self.dao.select_person(c)
            if not person_id:
                person_id = self.dao.insert_person(c)
            self.dao.map_credit(movie_id, person_id, c['credit_type'], c['credit_subtype'])


class CollectionLoader(object):
    @staticmethod
    def load_collection(file, database):
        dao = SimpleDao(database)
        handler = MovieHandler(dao)
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        with open(file, 'rb') as source:
            parser.parse(source)
        dao.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    CollectionLoader.load_collection(sys.argv[1], sys.argv[2])


