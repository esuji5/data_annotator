from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, session, render_template, url_for
from flask_s3 import FlaskS3

from basic_auth import requires_auth
from data import get_image_data
from data import get_step1_inputer_dict
from data import fetch_next_rand_id
from data import update_step1

# setup flask
app = Flask(__name__)
app.config.from_object(__name__)  # load config from this file , flaskr.py
app.config.from_envvar('YUYU_DATA_SETTINGS')
if not app.config['DEBUG'] and not app.config['TESTING']:
    s3 = FlaskS3(app)
db = SQLAlchemy(app)


def get_avatar():
    return session.get('avatar', None)


@app.route('/')
@requires_auth
def top():
    step1_inputer_dict = get_step1_inputer_dict(db)
    next_rand_id = fetch_next_rand_id(db)
    return render_template('index.html', step1_inputer_dict=step1_inputer_dict,
                           next_rand_id=next_rand_id, avatar=get_avatar())


@app.route('/set_avatar/<avatar>')
@requires_auth
def set_avatar(avatar):
    if avatar == 'none':
        session['avatar'] = None
    else:
        session['avatar'] = avatar
    return redirect(url_for('top'))


@app.route('/annotate/<koma_id>')
@requires_auth
def annotate(koma_id):
    img_data = get_image_data(db, koma_id)
    img_path = img_data['img_path'].split('yuyu_data/')[-1]
    next_rand_id = fetch_next_rand_id(db)
    return render_template('annotate.html', img_path=img_path, img_data=img_data,
                           koma_id=koma_id, next_rand_id=next_rand_id, avatar=get_avatar())


@app.route('/save_annotate', methods=['POST'])
@requires_auth
def save_annotate():
    # request.formのMultiDictだと変なlist型になるので普通のdictにする
    val_dict = {key: val for key, val in request.form.items()}
    update_step1(db, val_dict)
    next_rand_id = fetch_next_rand_id(db)
    return redirect('/annotate/' + next_rand_id)


if __name__ == '__main__':
    app.run()

# @app.before_request
# def before_request():
#     g.db = db


# @app.after_request
# def after_request(response):
#     g.db.close()
#     return response

# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()
# from bokeh.charts import Histogram
# from bokeh.embed import components
# from bokeh.plotting import figure
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
