from http import HTTPStatus

from flask import jsonify, request

from . import app  # BASE_URL
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!', HTTPStatus.BAD_REQUEST)

    url_map = URLMap.from_dict(data)
    try:
        url_map.save()
    except ValueError as error:
        raise InvalidAPIUsage(error.args[0], HTTPStatus.BAD_REQUEST)
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.get(short_id)
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
