from http import HTTPStatus

from flask import jsonify, request

from . import app  # BASE_URL
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import random_string, validate_custom_id


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data or 'url' == "":
        raise InvalidAPIUsage('\"url\" является обязательным полем!', HTTPStatus.BAD_REQUEST)

    if 'custom_id' not in data or data['custom_id'] is None:
        data['custom_id'] = random_string()

    custom_id = data['custom_id']

    if not validate_custom_id(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if URLMap.get(custom_id):
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.',
                              HTTPStatus.BAD_REQUEST)

    url = URLMap()
    url.from_dict(data)
    url.save(url)
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.get(short_id)
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
