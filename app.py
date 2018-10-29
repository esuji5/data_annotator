from urllib.parse import urljoin

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, session, render_template, url_for
# from flask_s3 import FlaskS3
from flask import redirect
from flask_cdn import CDN

from flask_compress import Compress

# from basic_auth import requires_auth
from data import get_image_data
from data import get_step1_inputer_dict
from data import get_graph_script
from data import fetch_next_rand_id
from data import update_step1

# setup flask
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('YUYU_DATA_SETTINGS')
if not app.config['DEBUG'] and not app.config['TESTING']:
    # print('use CDN')
    # app.config['CDN_DOMAIN'] = 'd1jm3kuvjv07m2.cloudfront.net'
    app.config['STATIC_URL'] = 'http://d1jm3kuvjv07m2.cloudfront.net/static'
    # CDN(app)  # for js, css
    # FlaskS3(app)  # for jpg
db = SQLAlchemy(app)
Compress(app)


def get_avatar():
    return session.get('avatar', None)


# @app.endpoint('static')
# def static(filename):
#     static_url = app.config.get('STATIC_URL')

#     if static_url:
#         return redirect(urljoin(static_url, filename))
#     print('in static', app.send_static_file(filename))
#     return app.send_static_file(filename)

@app.template_global()
def static_url(filename):
    static_url = app.config.get('STATIC_URL')

    if static_url:
        return urljoin(static_url, filename)

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
    print(url_for("static", filename=img_path))
    print(url_for("static", filename=img_path, _external=True))
    print(app.config.get('STATIC_URL'), img_path)
    return render_template('annotate.html', img_path=img_path, img_data=img_data,
                           koma_id=koma_id, next_rand_id=next_rand_id, avatar=get_avatar())


@app.route('/save_annotate', methods=['POST'])
# @requires_auth
def save_annotate():
    # request.formのMultiDictだと変なlist型になるので普通のdictにする
    val_dict = {key: val for key, val in request.form.items()}
    update_step1(db, val_dict)
    next_rand_id = fetch_next_rand_id(db)
    return redirect('/annotate/' + next_rand_id)


if __name__ == '__main__':
    app.run()
