import awsgi
from server.app import app


def lambda_handler(event, context):
    print(event)
    return awsgi.response(app, event, context)
