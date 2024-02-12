from flask import render_template, flash, redirect, abort

from . import app, BASE_URL
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if URLMap.get(short):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('url_cut.html', form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=short,
        )
        url_maping = URLMap.save(url_map)
        return render_template('url_cut.html', form=form,
                               short=BASE_URL + url_maping.short)
    return render_template('url_cut.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_url(short):
    if URLMap.get(short) is None:
        abort(404)
    return redirect(URLMap.get(short).original)
