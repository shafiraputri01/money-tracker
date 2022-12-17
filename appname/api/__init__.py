from flask import Blueprint, request, jsonify
from itertools import groupby

from flask_restful.representations.json import output_json
from flask_restful import reqparse
import flask_restful as restful

from appname.extensions import login_manager
from appname.models.user import User

api_blueprint = Blueprint('api', __name__)
api_blueprint.config = {}

api = restful.Api(api_blueprint)

API_VERSION = 'v1'
API_BASE = '/'  # API_BLUEPRINT prefix is 'api'

@api.representation('application/json')
def envelope_api(data, code, headers=None):
    """ API response envelope (for metadata/pagination).
    Optionally wraps JSON response in envelope.
    This is for successful requests only.

        data is the object returned by the API.
        code is the HTTP status code as an int
    """
    if not request.args.get('envelope'):
        return output_json(data, code, headers)
    message = 'success'
    if 'message' in data:
        message = data['message']
        del data['message']
    data = {
        'data': data,
        'code': code,
        'message': message
    }
    return output_json(data, code, headers)

@login_manager.request_loader
def load_user_from_request(request):
    # Only functional for API Endpoints
    if not request.endpoint or not request.endpoint.startswith("api."):
        return None

    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if not api_key:
        return None
    user_id, _ = api_key.split('-')
    user = User.get_by_hashid(user_id)
    if user and user.check_api_key_hash(api_key):
        return user

def custom_abort(status_code, message, data=None):
    response = jsonify({
        'code': status_code,
        'data': data,
        'message': message,
    })
    response.status_code = status_code
    return response

def handle_api_error(err):
    return custom_abort(404, str(err))

class Resource(restful.Resource):
    method_decorators = []
    required_scopes = {}
    # applies to all inherited resources

    def __repr__(self):
        return "<Resource {0}>".format(self.__class__.__name__)

    def make_response(self, data, *args, **kwargs):
        return super().make_response(data, *args, **kwargs)


class BaseAPISchema():
    """ APISchema describes the input and output formats for
    resources. The parser deals with arguments to the API.
    The API responses are marshalled to json through get_fields
    """
    get_fields = {}

    def __init__(self):
        self.parser = reqparse.RequestParser()

    def parse_args(self):
        return self.parser.parse_args()

class Wallet:
    balance = 665000

    idx = 3

    records = {
        1: {
            'id': 1,
            'date': '2022-05-02',
            'amount': 700000,
            'notes': 'Monthly Income',
            'is_income': True,
        },
        2: {
            'id': 2,
            'date': '2022-05-03',
            'amount': 20000,
            'notes': 'F&B',
            'is_income': False,
        },
        3: {
            'id': 3,
            'date': '2022-05-04',
            'amount': 15000,
            'notes': 'Transport',
            'is_income': False,
        },
    }

    def add_record(self, record_data):
        self.idx += 1

        if record_data['is_income']:
            self.balance += record_data['amount']
        else:
            self.balance -= record_data['amount']

        record_data['id'] = self.idx
        self.records[self.idx] = record_data

        return self.records[self.idx]

    def edit_record(self, record_data):
        record_id = record_data['id']
        old_record = self.records[record_id]

        if old_record['is_income']:
            self.balance -= old_record['amount']
        else:
            self.balance += old_record['amount']

        if record_data['is_income']:
            self.balance += record_data['amount']
        else:
            self.balance -= record_data['amount']

        self.records[record_id] = record_data

        return self.records[record_id]

    def delete_record(self, record_id):
        old_record = self.records[record_id]

        if old_record['is_income']:
            self.balance -= old_record['amount']
        else:
            self.balance += old_record['amount']

        del self.records[record_id]

        return old_record

    def get_record(self, record_id):
        return self.records[record_id]

    def get_records(self):
        return list(self.records.values())

    def get_statistic(self):
        result = {}

        for record in self.records.values():
            try:
                result[record['date'][0:7]]
            except KeyError:
                result[record['date'][0:7]] = {
                    'month': record['date'][0:7],
                    'income': 0,
                    'expense': 0,
                }

            if record['is_income']:
                result[record['date'][0:7]]['income'] += record['amount']
            else:
                result[record['date'][0:7]]['expense'] += record['amount']
        return list(result.values())

    def get_balance(self):
        return self.balance


wallet = Wallet()
