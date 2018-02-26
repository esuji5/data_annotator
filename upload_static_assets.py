import flask_s3
from app import app

app.config['AWS_ACCESS_KEY_ID'] = 'AKIAIHGYOSPAJA4TQM5A'
app.config['AWS_SECRET_ACCESS_KEY'] = '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'
app.config['FLASKS3_BUCKET_NAME'] = 'yuyudata'

flask_s3.create_all(app, filepath_filter_regex=r'(style.css|index.js)')
