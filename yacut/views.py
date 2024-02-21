from flask import render_template, flash, redirect, abort

from . import app, BASE_URL
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        url_map = URLMap.from_dict(
            {'custom_id': short,
             'url': form.original_link.data
             }
        )
        try:
            url_map.save()
        except ValueError as error:
            flash(error.args[0])
        return render_template('url_cut.html', form=form,
                               short=BASE_URL + url_map.short)
    return render_template('url_cut.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_url(short):
    url_map = URLMap.get(short)
    if not url_map:
        abort(404)
    return redirect(url_map.original)
