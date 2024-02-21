from datetime import datetime
import re
import random

from . import db, BASE_URL
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
        new_short_id = ''.join(random.choices(CHARACTERS, k=length))
        if URLMap.get(new_short_id):
            raise ValueError('Сгенерированная ссылка уже сущетвует' +
                             '\n Порпробуйте снова')
        return new_short_id

    @staticmethod
    def validate_custom_id(custom_id):
        return bool(re.search(CHEK_PATTERN, custom_id))

    def save(self):
        if self.short:
            if not self.validate_custom_id(self.short):
                raise ValueError('Указано недопустимое имя для короткой ссылки')
        else:
            self.short = self.random_string()
        if URLMap.get(self.short):
            raise ValueError('Предложенный вариант короткой ссылки уже существует.')
        db.session.add(self)
        db.session.commit()
        return self
