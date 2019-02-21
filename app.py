import os 

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, session, render_template, url_for
from flask_compress import Compress
import furl

# from basic_auth import requires_auth
from data import get_image_data
from data import get_page_data
from data import get_step1_inputer_dict
from data import get_graph_script
from data import fetch_next_rand_id
from data import update_step1

# setup flask
app = Flask(__name__)
# 一旦False
app.config['DEBUG'] = False
app.config['TESTING'] = False
app.config.from_object(__name__)
app.config.from_envvar('YUYU_DATA_SETTINGS', silent=True)
if not app.config['DEBUG'] and not app.config['TESTING']:
    app.config['STATIC_URL'] = 'http://d1jm3kuvjv07m2.cloudfront.net'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['FLASKS3_BUCKET_NAME'] = os.environ.get('FLASKS3_BUCKET_NAME')
    app.config['FLASKS3_FORCE_MIMETYPE'] = os.environ.get('FLASKS3_FORCE_MIMETYPE')
    os.environ.get('AURORA_USER') 
db = SQLAlchemy(app)
Compress(app)


def get_avatar():
    return session.get('avatar', None)


@app.template_global()
def static_url(filename):
    static_url = app.config.get('STATIC_URL')

    print('static_url', furl.furl(static_url).join('static/' + filename))
    if static_url:
        return furl.furl(static_url).join('static/' + filename)

    return url_for('static', filename=filename)


@app.route('/')
# @requires_auth
def top():
    step1_inputer_dict = get_step1_inputer_dict(db)
    graph_script = get_graph_script(step1_inputer_dict)
    next_rand_id = fetch_next_rand_id(db)
    return render_template('index.html', graph_script=graph_script,
                           next_rand_id=next_rand_id, avatar=get_avatar())


@app.route('/set_avatar/<avatar>')
# @requires_auth
def set_avatar(avatar):
    session['avatar'] = avatar if avatar != 'none' else None
    return redirect(url_for('top'))


@app.route('/annotate/')
def annotate_no_id():
    return redirect(url_for('top'))


@app.route('/annotate/<koma_id>')
# @requires_auth
def annotate(koma_id):
    img_data = get_image_data(db, koma_id)
    img_path = img_data['img_path'].split('yuyu_data/')[-1]
    next_rand_id = fetch_next_rand_id(db)
    return render_template('annotate.html', img_path=img_path, img_data=img_data,
                           koma_id=koma_id, next_rand_id=next_rand_id, avatar=get_avatar())


@app.route('/confirm/<page_id_idx>')
# @requires_auth
def confirm(page_id_idx):
    '''
    page_id_idx: str
    '''
    page_id_idx = int(page_id_idx)
    page_data = get_page_data(db, page_id_idx)
    kanji, page = page_data[0]['kanji'], page_data[0]['page']
    next_page_id_idx = page_id_idx + 1
    return render_template('confirm.html', page_data=page_data,
                           page_id_idx=page_id_idx, next_page_id_idx=next_page_id_idx,
                           kanji=kanji, page=page, avatar=get_avatar())


@app.route('/save_annotate', methods=['POST'])
# @requires_auth
def save_annotate():
    default_eye = request.args.get('default_eye', default=0, type=int)
    print(request.args)
    # request.formのMultiDictだと変なlist型になるので普通のdictにする
    val_dict = {key: val for key, val in request.form.items()}
    update_step1(db, val_dict)
    next_rand_id = fetch_next_rand_id(db)
    return redirect(f'/annotate/{next_rand_id}?default_eye={default_eye}')


if __name__ == '__main__':
    app.run()
