from flask import render_template, flash, redirect, abort

from . import app, BASE_URL
from .forms import URLMapForm
from .models import URLMap
from .utils import random_string, validate_custom_id


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if not short:
            short = random_string()
        if short and not validate_custom_id(short):
            flash('Допустимые символы: A-z, 0-9')
        if URLMap.get(short):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('url_cut.html', form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=short,
        )
        URLMap.save(url_map)
        return render_template('url_cut.html', form=form,
                               short=BASE_URL + short)
    return render_template('url_cut.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_url(short):
    if URLMap.get(short) is None:
        abort(404)
    return redirect(URLMap.get(short).original)
