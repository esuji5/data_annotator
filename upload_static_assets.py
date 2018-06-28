import flask_s3
from app import app

app.config['AWS_ACCESS_KEY_ID'] = '{AWS_ACCESS_KEY_ID}'
app.config['AWS_SECRET_ACCESS_KEY'] = '{AWS_SECRET_ACCESS_KEY}'
app.config['FLASKS3_BUCKET_NAME'] = 'yuyudata'

flask_s3.create_all(app, filepath_filter_regex=r'(style.css|index.js)')
