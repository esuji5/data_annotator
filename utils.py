def get_image_data(db, koma_id):
    select_sql = 'SELECT img_path FROM yuyu_data WHERE koma_id = "{}"'.format(koma_id)
    cur = db.engine.execute(select_sql)
    data = cur.fetchone()
    return data


def get_step1_inputer_dict(db):
    select_sql = 'SELECT step1_inputer, COUNT(step1_inputer) FROM yuyu_data GROUP BY step1_inputer'
    cur = db.engine.execute(select_sql)
    data = cur.fetchall()
    step1_inputer_dict = {r['step1_inputer']: r['count(step1_inputer)'] for r in data}
    return step1_inputer_dict

# select step, count(step) from yuyu_data
# group by step
# select step1_inputer, count(step1_inputer) from yuyu_data
# group by step1_inputer
