from flask import jsonify, request, abort
from webapp import app
import webapp.dao as dao


@app.route('/api/genres')
def get_genres():
    genres = dao.select_all_genres()
    return jsonify(genres=genres)


@app.route('/api/ratings')
def get_ratings():
    ratings = dao.select_all_ratings()
    return jsonify(ratings=ratings)


@app.route('/api/movies', methods=['GET', 'POST'])
def get_movies():
    s = request.args.get('s', 0)
    n = request.args.get('n', -1)
    # the list of default fields to retrieve (used by GET by default)
    fields = ['id', 'uid', 'title', 'original_title', 'overview', 'rating', 'length', 'year']
    if request.method == 'POST':
        if request.json:
            data = request.get_json()
            if 'fields' in data:
                fields = data['fields']
    result = dao.select_movies(s, n, fields=fields)
    return jsonify(result), 200


@app.route('/api/movie/<uid>', methods=['GET'])
def get_details(uid):
    movie = dao.select_movie_details(uid)
    return jsonify(movie)
