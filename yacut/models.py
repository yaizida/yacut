from datetime import datetime
from http import HTTPStatus
import re
import random

from . import db, BASE_URL
from .error_handlers import InvalidAPIUsage
from . import CHARACTERS, CHEK_PATTERN, RANDOM_LENGTH


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
    def random_string(length=RANDOM_LENGTH):
        existing_ids = {url for url in URLMap.query.all()}
        while True:
            new_short_id = ''.join(random.choices(CHARACTERS, k=length))
            if new_short_id not in existing_ids:
                return new_short_id

    @staticmethod
    def validate_custom_id(custom_id):
        return bool(re.search(CHEK_PATTERN, custom_id))

    def save(self):
        if self.short:
            if not self.validate_custom_id(self.short):
                # Если кидаю дпугую то ругаюатся тесты
                raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        else:
            self.short = self.random_string()
        if URLMap.get(self.short):
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.',
                                  HTTPStatus.BAD_REQUEST)
        db.session.add(self)
        db.session.commit()
        return self
