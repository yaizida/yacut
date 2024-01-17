from flask import render_template, flash, redirect, abort

from . import app, db, BASE_URL
from .forms import URLMapForm
from .models import URLMap
from .utils import random_string, check_custom


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if not short:
            short = random_string()
        if short and not check_custom(short):
            flash('Допустимые символы: A-z, 0-9')
        if URLMap.query.filter_by(short=short).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('url_cut.html', form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=short,
        )
        db.session.add(url_map)
        db.session.commit()
        return render_template('url_cut.html', form=form,
                               short=BASE_URL + short)
    return render_template('url_cut.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_url(short):
    link = URLMap.query.filter_by(short=short).first()
    if link is None:
        abort(404)
    return redirect(link.original)
