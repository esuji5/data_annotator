import sqlite3

from flask import g


def connect_db(app):
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db(app):
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db(app)
    return g.sqlite_db


def get_cursor():
    dbname = "yuyu_data.db"
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    return cursor, conn


# def get_image_data(app, koma_id):
    # db = get_db(app)
def get_image_data(db, koma_id):
    select_sql = 'SELECT img_path FROM yuyu_data WHERE koma_id = "{}"'.format(koma_id)
    cur = db.engine.execute(select_sql)
    data = cur.fetchone()
    return data


def get_step1_inputer_dict(app):
    db = get_db(app)
    select_sql = 'SELECT step1_inputer, COUNT(step1_inputer) FROM yuyu_data GROUP BY step1_inputer'
    cur = db.engine.execute(select_sql)
    data = cur.fetchall()
    step1_inputer_dict = {r['step1_inputer']: r['count(step1_inputer)'] for r in data}
    return step1_inputer_dict

# select step, count(step) from yuyu_data
# group by step
# select step1_inputer, count(step1_inputer) from yuyu_data
# group by step1_inputer