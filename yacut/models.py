from datetime import datetime
from http import HTTPStatus

from . import db, BASE_URL
from .error_handlers import InvalidAPIUsage
from .utils import validate_custom_id


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

    def from_dict(self, data):
        self.short = data['custom_id']
        self.original = data['url']

    @staticmethod
    def get(custom_id):
        return URLMap.query.filter_by(short=custom_id).first()

    @staticmethod
    def save(data):
        if not validate_custom_id(data.short):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.get(data.short):
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.',
                                  HTTPStatus.BAD_REQUEST)
        db.session.add(data)
        db.session.commit()
