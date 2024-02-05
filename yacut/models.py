from datetime import datetime
from http import HTTPStatus

from . import db, BASE_URL
from .error_handlers import InvalidAPIUsage
from .utils import validate_custom_id, random_string


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=BASE_URL + self.short,
        )

    @staticmethod
    def from_dict(data):
        instance = URLMap()
        if 'custom_id' not in data:
            data['custom_id'] = ''
        instance.short = data['custom_id']
        instance.original = data['url']
        return instance

    @staticmethod
    def get(custom_id):
        return URLMap.query.filter_by(short=custom_id).first()

    @staticmethod
    def save(data):
        if not data.short:
            data.short = random_string()
        if not validate_custom_id(data.short):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.get(data.short):
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.',
                                  HTTPStatus.BAD_REQUEST)
        db.session.add(data)
        db.session.commit()
        return data
