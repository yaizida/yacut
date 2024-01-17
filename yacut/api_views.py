from http import HTTPStatus

from flask import jsonify, request

from . import app, db  # BASE_URL
from .error_handlers import InvalidAPIUsage, check_inique_short_url
from .models import URLMap
from .utils import random_string, check_custom


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data or 'url' == "":
        raise InvalidAPIUsage('\"url\" является обязательным полем!', HTTPStatus.BAD_REQUEST)

    if 'custom_id' not in data or data['custom_id'] is None:
        print('А как же я?')
        data['custom_id'] = random_string()

    custom_id = data['custom_id']
    if len(custom_id) > 16 or not check_custom(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    if check_inique_short_url(custom_id):
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.', HTTPStatus.BAD_REQUEST)

    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
