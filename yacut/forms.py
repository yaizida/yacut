from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import DataRequired, Optional


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Optional()]
    )
    submit = SubmitField('Создать')
