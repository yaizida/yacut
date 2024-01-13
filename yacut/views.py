from flask import render_template, flash, redirect, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import random_string


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if not short:
            short = random_string()
        if URLMap.query.filter_by(short=short).first():
            flash('Такая ссылка уже существует')
            return render_template('url_cut.html', form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=short,
        )
        db.session.add(url_map)
        db.session.commit()
        return render_template('url_cut.html', form=form,
                               short='http://127.0.0.1:5000/' + short)
    return render_template('url_cut.html', form=form)


@app.route('/<short>')
def redirect_url(short):
    link = URLMap.query.filter_by(short=short).first()
    if link:
        return redirect(link.original)
    else:
        flash('Несуществующая ссылка. Проверьте введенную ссылку')
        return redirect(url_for('get_unique_short_id'))
