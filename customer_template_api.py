import flask
from flask import request
from customer_template_api_dao import CustomerTemplateApiDao
from api_constants import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/te/customer/<customer_id>/templates', methods=['GET'])
def get_customer_template(customer_id):
    request_config = transform_input_param_to_request_config(GET_CUSTOMER_TEMPLATE)
    request_config[REQUEST_PARAMS][CUSTOMER_ID] = customer_id
    response = CustomerTemplateApiDao().get_customer_template(request_config)
    return response


@app.route('/te/customer/<customer_id>/templates', methods=['POST'])
def generate_customer_template(customer_id):
    request_config = transform_input_param_to_request_config(GET_CUSTOMER_TEMPLATE)
    request_config[REQUEST_PARAMS][CUSTOMER_ID] = customer_id
    response = CustomerTemplateApiDao().generate_customer_template(request_config)
    return response


def transform_input_param_to_request_config(endpoint):
    request_config = {}
    environ = request.environ
    request_config[END_POINT] = endpoint
    request_config[SOURCE_IP] = environ.get('HTTP_SOURCE_IP', environ.get(REMOTE_ADDR))
    request_config[REQUEST_PATH] = environ.get(PATH_INFO)
    request_config[QUERY_STRING] = environ.get(QUERY_STRING)
    request_config[REQUEST_METHOD] = environ.get(REQUEST_METHOD)

    headers = {ACCEPT: request.headers.get(ACCEPT)}
    request_config[HEADERS] = headers
    request_config[REQUEST_PARAMS] = request.args.copy()
    return request_config


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
