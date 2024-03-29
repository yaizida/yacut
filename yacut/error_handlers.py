from http import HTTPStatus

from flask import render_template, jsonify

from . import app, db


class InvalidAPIUsage(Exception):

    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code if status_code else HTTPStatus.BAD_REQUEST

    def to_dict(self):
        return dict(message=self.message)

    def from_dict(self, data):
        self.short = data['custom_id']
        self.original = data['url']


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html',
                           error_message='Нет такой страницы'
                           ), HTTPStatus.NOT_FOUND


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html',
                           error_message='Ошибка сервера'
                           ), HTTPStatus.INTERNAL_SERVER_ERROR
