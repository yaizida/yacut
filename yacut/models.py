from datetime import datetime
from http import HTTPStatus
import re
import random

from flask import flash

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
        return ''.join(random.choices(CHARACTERS, k=length))

    @staticmethod
    def validate_custom_id(custom_id):
        return bool(re.search(CHEK_PATTERN, custom_id))

    def save(self):
        if not self.short:
            self.short = self.random_string()
        # А если нам прилетит в save не сгенерированая ссылка, а кастомная пользователя ?
        if not self.validate_custom_id(self.short):
            flash('Допустимые символы: A-z, 0-9')
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.get(self.short):
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.',
                                  HTTPStatus.BAD_REQUEST)
        db.session.add(self)
        db.session.commit()
        return self
