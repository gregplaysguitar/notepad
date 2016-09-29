#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask import Flask, render_template, redirect, url_for, request, abort, \
    jsonify, make_response
from flask_assets import Environment, Bundle
import shortuuid

PROJECT_ROOT = os.path.dirname(__file__)

app = Flask(__name__)
assets = Environment(app)

app.config.update(dict(
    # default settings here
    DATA_DIR=os.path.join(PROJECT_ROOT, 'data'),
    KEY_LENGTH=6
))
# load env-specific settings (i.e. dev)
app.config.from_envvar('FLASK_SETTINGS', silent=True)

# any asset bundles requiring pre-processing are declared here
assets.register('style_css', Bundle('c/style.scss', filters='pyscss',
                                    output='gen/style.css'))


def file_path(key):
    return os.path.join(app.config['DATA_DIR'], '%s.txt' % key)


def new_key():
    key = shortuuid.uuid()[-app.config['KEY_LENGTH']:]

    # recurse until we get an unused one, just in case
    if os.path.exists(file_path(key)):
        return new_key

    return key


def save_note(text, key=None):
    if not key:
        key = new_key()

    f = open(file_path(key), 'w')
    f.write(text)
    f.close()

    return key


def delete_note(key):
    path = file_path(key)
    os.remove(path)


def get_note(key):
    path = file_path(key)

    if not os.path.exists(path):
        return None

    f = open(path, 'r')
    text = f.read()
    f.close()
    return text


@app.route('/')
@app.route('/<key>')
def index(key=None):
    if key:
        text = get_note(key)

        if text is None:
            abort(404)
    else:
        text = ''

    return render_template('index.html', text=text, key=key)


@app.route('/', methods=['POST'])
@app.route('/<key>', methods=['POST'])
def save(key=None):
    key = save_note(request.form.get('t', ''), key=key)

    if request.form.get('a'):
        panel = app.jinja_env.get_template('panel.html').render(key=key)
        return jsonify(url=url_for('index', key=key), panel=panel)
    else:
        return redirect(url_for('index', key=key))


@app.route('/d/<key>', methods=['POST'])
def delete(key):
    key = delete_note(key=key)

    return redirect(url_for('index'))


@app.route('/<key>.txt')
def download(key):
    text = get_note(key)

    if text is None:
        abort(404)

    response = make_response(text)
    response.headers["Content-Disposition"] = \
        "attachment; filename=%s.txt" % key
    return response


@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist<br><a href="/">Home</a>', 404


if __name__ == '__main__':
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))
