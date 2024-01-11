from flask import render_template, flash, redirect, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import random_string


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    """!!!ТРЕБУЕТ ДОРАБОТКИ!!!"""
    """Скорее всего редирект не нужен"""
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if URLMap.query.filter_by(short=short).first():
            flash('Такая ссылка уже существует')
            return render_template('url_cut.html')
        if short is None:
            short = random_string()
        url_map = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data,
        )
        db.session.add(url_map)
        db.session.commit()
        # return redirect(url_for('url_redirect'), short=short)
    return render_template('url_cut.html', form=form)

"""ДОРАБОТАЙ СНАЧАЛА ШАБЛОН ЧТО БЫ МОЖНО БЫЛО ОТСЛЕЖИВАТЬ"""
