import random

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, session, g, render_template, flash, url_for
from flask_s3 import FlaskS3
# from bokeh.charts import Histogram
# from bokeh.embed import components
# from bokeh.plotting import figure

# from utils import connect_db
from utils import get_image_data
from utils import get_step1_inputer_dict

# setup flask
app = Flask(__name__)
app.config.from_object(__name__)  # load config from this file , flaskr.py
app.config.from_envvar('YUYU_DATA_SETTINGS')
if not app.config['DEBUG'] and not app.config['TESTING']:
    s3 = FlaskS3(app)
db = SQLAlchemy(app)


# @app.before_request
# def before_request():
#     g.db = db


# @app.after_request
# def after_request(response):
#     g.db.close()
#     return response


def get_avatar():
    return session.get('avatar', None)


def fetch_next_rand_id():
    # db = get_db(app)
    step1_ids_sql = 'SELECT koma_id FROM yuyu_data WHERE step = 1'
    step1_ids = db.engine.execute(step1_ids_sql).fetchall()
    next_rand_id = random.choice(step1_ids)['koma_id']
    return next_rand_id


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def top():
    step1_inputer_dict = get_step1_inputer_dict(app)
    next_rand_id = fetch_next_rand_id()
    return render_template('index.html', step1_inputer_dict=step1_inputer_dict,
                           next_rand_id=next_rand_id, avatar=get_avatar(),
                           )


@app.route('/set_avatar/<avatar>')
def set_avatar(avatar):
    if avatar == 'none':
        session['avatar'] = None
    else:
        session['avatar'] = avatar
    return redirect(url_for('top'))


@app.route('/annotate/<koma_id>')
def annotate(koma_id):
    img_data = get_image_data(db, koma_id)
    img_path = url_for('static', filename=img_data['img_path'].split('yuyu_data/')[-1])
    img_path = img_data['img_path'].split('yuyu_data/')[-1]
    print(img_path)
    print(url_for('static', filename='style.css'))
    next_rand_id = fetch_next_rand_id()
    return render_template('annotate.html', img_path=img_path, img_data=img_data,
                           koma_id=koma_id, next_rand_id=next_rand_id, avatar=get_avatar())


@app.route('/save_annotate', methods=['POST'])
def save_annotate():
    # request.formのMultiDictだと変なlist型になるので普通のdictにする
    val_dict = {key: val for key, val in request.form.items()}

    update_sql = '''
    UPDATE yuyu_data SET
    chara_num = {chara_num},
    whos = "{whos}",
    face_direction = "{face_direction}",
    eyes = "{eyes}",
    step1_inputer = "{step1_inputer}",
    step = 2
    where koma_id = "{koma_id}"
    '''.format(**val_dict)

    # db = get_db(app)
    db.engine.execute(update_sql)
    # db.engine.commit()
    flash('update was successfully posted')
    next_rand_id = fetch_next_rand_id()
    return redirect('/annotate/' + next_rand_id)


if __name__ == '__main__':
    app.run()


# データを集めるカラム
columns = ['koma_id', 'img_path', 'kanji', 'page', 'position', 'koma', 'size_x', 'size_y',
           'chara_num', 'whos', 'eyes', 'face_direction',  # 1次入力
           'place', 'background', 'serif_num', 'whos_s',  # 2次入力
           'serifs', 'onomatope',  # 3次入力
           'step', 'step1_inputer', 'step2_inputer', 'step3_inputer', ]  # 入力ステップ管理

# import math
# from collections import namedtuple

# p = figure(
#     title="Hoge",
#     x_axis_label='x',
#     y_axis_label='y',
# )
#  # x_range=xdr, y_range=ydr, plot_width=width,plot_height=height,
# # Data = namedtuple('Data', ('name', 'value', 'color'))
# # rates = [Data("A", 0.6, "#7FC97F"), Data("B", 0.4, "#DD1C77")]

# # start_angle = 0
# # for rate in rates:
# #     p.annular_wedge(
# #         x=0,
# #         y=0,
# #         inner_radius=0.2,
# #         outer_radius=0.5,
# #         start_angle=math.pi * 2 * start_angle,
# #         end_angle=math.pi * 2 * (start_angle + rate.value),
# #         color=rate.color,
# #         legend=rate.name
# #     )
# #     start_angle += rate.value
# x = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
# p.vbar(x, top=x, width=0.2, bottom=0, color="#CAB2D6")


# p = figure(title='title',
#            h_symmetry=False, v_symmetry=False,
#            # min_border=0, toolbar_location="above",
#            # esponsive=False,
#            outline_line_color="#666666")
# plot = p
# # Embed plot into HTML via Flask Render
# script, div = components(plot)
# print(script)
# print(step1_inputer_dict)
# the_script=script, the_div=div,
