import logging
import sqlite3
from flask import g
from webapp import app


def make_dict(cursor, row):
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))


def connect_db():
    logging.debug('opening database connection')
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = make_dict  # sqlite3.Row
    return db


def get_db():
    if not hasattr(g, 'collection_database'):
        g.collection_database = connect_db()
    return g.collection_database


@app.teardown_appcontext
def close_db(ex):
    if hasattr(g, 'collection_database'):
        logging.debug('closing database')
        g.collection_database.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return (rows[0] if rows else None) if one else rows


def select_all_genres():
    return query_db("SELECT id, name FROM genres ORDER BY name ASC")


def select_all_ratings():
    ratings = [r['rating'] for r in query_db("SELECT DISTINCT rating FROM movies ORDER BY rating ASC ")]
    return ratings


def select_all_movies():
    movies = query_db("SELECT id, uid, title, original_title, rating, length, year FROM movies ORDER BY sort_title ASC")
    return movies


def select_movies(s=0, n=-1, fields=['id', 'uid', 'title', 'original_title', 'overview', 'rating', 'length', 'year']):
    qry = "SELECT {2} FROM movies ORDER BY sort_title LIMIT {0} OFFSET {1}".format(n, s, ','.join(fields))
    movies = query_db(qry)
    total = query_db("SELECT COUNT(id) AS cnt FROM movies", one=True)['cnt']
    return {
        'movies': movies,
        'total': total
    }


def select_movie_by_id(movie_id):
    query = "SELECT id, uid, title, original_title, overview, rating, length, year FROM movies WHERE id = ?"
    movie = query_db(query, one=True)
    return movie


def select_movie_by_uid(movie_uid):
    query = "SELECT id, uid, title, original_title, overview, rating, length, year FROM movies WHERE uid = ?"
    movie = query_db(query, args=(movie_uid,), one=True)
    return movie

def select_movie_details(movie_uid):
    movie = select_movie_by_uid(movie_uid)
    if movie:
        movie['genres'] = query_db("SELECT g.id, g.name FROM genres g, movie_genres mg WHERE mg.movie_id = ? AND mg.genre_id = g.id", args=(movie['id'],))
        movie['roles'] = query_db("SELECT p.id AS person_id, r.role, p.first_name, p.middle_name, p.last_name, p.birth_year FROM roles r, persons p WHERE r.movie_id = ? AND r.person_id = p.id", args=(movie['id'],))
        movie['credits'] = query_db("SELECT p.id AS person_id, c.credit_type, c.credit_subtype, p.first_name, p.middle_name, p.last_name, p.birth_year FROM credits c, persons p WHERE c.movie_id = ? AND c.person_id = p.id", args=(movie['id'],))
        movie['studios'] = query_db("SELECT s.id, s.name FROM studios s, movie_studios ms WHERE ms.movie_id = ? AND ms.studio_id = s.id", args=(movie['id'],))
        movie['companies'] = query_db("SELECT c.id, c.name FROM companies c, movie_companies mc WHERE mc.movie_id = ? AND mc.company_id = c.id", args=(movie['id'],))
    return movie
