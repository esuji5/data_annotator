import random

from flask import flash


def get_image_data(db, koma_id):
    select_sql = "SELECT img_path, chara_num, whos, eyes, face_direction, step FROM yuyu_data WHERE koma_id = '{}'".format(koma_id)
    cur = db.engine.execute(select_sql)
    data = cur.fetchone()
    # if isinstance(data[1], float):
    #     data[1] = int(data[1])
    return data


def get_step1_inputer_dict(db):
    select_sql = 'SELECT step1_inputer, COUNT(step1_inputer) FROM yuyu_data GROUP BY step1_inputer'
    cur = db.engine.execute(select_sql)
    data = cur.fetchall()
    step1_inputer_dict = {name: count for name, count in data}
    return step1_inputer_dict


def fetch_next_rand_id(db):
    # db = get_db(app)
    step1_ids_sql = 'SELECT koma_id FROM yuyu_data WHERE step = 1'
    step1_ids = db.engine.execute(step1_ids_sql).fetchall()
    next_rand_id = random.choice(step1_ids)['koma_id']
    return next_rand_id


def update_step1(db, val_dict):
    update_sql = """
    UPDATE yuyu_data SET
    chara_num = {chara_num},
    whos = '{whos}',
    face_direction = '{face_direction}',
    eyes = '{eyes}',
    step1_inputer = '{step1_inputer}',
    step = 2
    where koma_id = '{koma_id}'
    """.format(**val_dict)

    # db = get_db(app)
    db.engine.execute(update_sql)
    # db.engine.commit()
    flash('update was successfully posted')


def get_graph_script(step1_inputer_dict):
    graph_script = """
    <script type='text/javascript'>
      var data = {{
        // A labels array that can contain any sort of values
        labels: ['yuzuko', 'yukari', 'yui', '未入力'],
        // Our series array that contains series objects or in this case series data arrays
        series: [{yuzuko},{yukari},{yui},{not_yet}]
      }};

      var options = {{
        distributeSeries: true,
        //high: 300,
        showArea: true,
        showPoint: true,
        showLabel: true,

        labelInterpolationFnc: function(value) {{
        console.log(value)
            return value
        }}
      }}

      var chart = new Chartist.Bar('.ct-chart', data, options);
    </script>
    """.format(**step1_inputer_dict)
    return graph_script


def get_pie_chart_script(step1_inputer_dict):
    graph_script = """
    <script type='text/javascript'>
      var data = {{
        labels: ['yuzuko', 'yukari', 'yui', '未入力'],
        series: [{yuzuko},{yukari},{yui},{not_yet}]
      }};
      new Chartist.Pie('.ct-chart', data)

    </script>
    """.format(**step1_inputer_dict)
    return graph_script

# データを集めるカラム
columns = ['koma_id', 'img_path', 'kanji', 'page', 'position', 'koma', 'size_x', 'size_y',
           'chara_num', 'whos', 'eyes', 'face_direction',  # 1次入力
           'place', 'background', 'serif_num', 'whos_s',  # 2次入力
           'serifs', 'onomatope',  # 3次入力
           'step', 'step1_inputer', 'step2_inputer', 'step3_inputer', ]  # 入力ステップ管理

# select step, count(step) from yuyu_data
# group by step
# select step1_inputer, count(step1_inputer) from yuyu_data
# group by step1_inputer
# CREATE INDEX step1_inputer_id ON yuyu_data (step1_inputer_id)
# DROP INDEX step1_inputer_id
# SELECT koma_id FROM yuyu_data WHERE step = 1
# SELECT img_path, chara_num, whos, eyes, face_direction, step FROM yuyu_data WHERE koma_id = '01-095-'