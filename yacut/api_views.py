import re
from http import HTTPStatus
from urllib.parse import urljoin

from flask import jsonify, request

from . import app, db
from .models import URLMap
from .utils import random_string
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/<string:id>/', methods=['GET'])
def get_original_link(id):
    db_object = URLMap.query.filter_by(short=id).first()
    if db_object is None:
        raise InvalidAPIUsage(
            'Указанный id не найден',
            HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': db_object.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    base_url = request.url_root
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    elif 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    elif (
        'custom_id' in data and data['custom_id'] is not None and
        len(data['custom_id']) > 0
    ):
        if (
            len(data['custom_id']) > 15 or not
            re.match(r'^[a-zA-Z0-9]+$', data['custom_id'])
        ):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        elif (URLMap.query.filter_by(short=data['custom_id']).first()
              is not None):
            raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
        else:
            short = data['custom_id']
    else:
        short = random_string()
    url = URLMap(
        original=data['url'],
        short=short,
    )
    db.session.add(url)
    db.session.commit()
    return jsonify(
        {
            'short_link': urljoin(base_url, short),
            'url': data['url']
        }
    ), HTTPStatus.CREATED
