command = '/home/dev/env/bin/gunicorn'
pythonpath = '/home/dev/env/bin'
bind = '127.0.0.1:8001'
workers = 3
user = 'dev'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=medical_site.settings'
