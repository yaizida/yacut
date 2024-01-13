from flask import render_template, jsonify

from . import app, db


class InvalidAPIUsage(Exception):
    # Если статус-код для ответа API не указан - вернется код 400
    satus_code = 400
    # Конструктор класса InvalidAPIUsage принимает на вход
    # текст сообщения и статус код ошибки (необязательно)

    def __init__(self, message, status_code=None) -> None:
        super().__init__()
        self.message = message
        # Если статус-код передан в конструктор -
        # этот код вернется в ответе
        if status_code is not None:
            self.satus_code = status_code

    # метод для сериализации переданного сообщения об ошибк
    def to_dict(self):
        return dict(message=self.message)


# Обработчик кастомного исключения для API
@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    # Возвращает в ответе текст ошибки и статус-код
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500