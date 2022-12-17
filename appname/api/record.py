from flask import request
from flask_restful import marshal_with
from flask_restful import fields

from appname.api import Resource, BaseAPISchema, wallet


class RecordSchema(BaseAPISchema):
    record_fields = {
        'id': fields.Integer,
        'date': fields.String,
        'amount': fields.Integer,
        'notes': fields.String,
        'is_income': fields.Boolean,
    }

class Record(Resource):
    schema = RecordSchema()

    @marshal_with(schema.record_fields)
    def get(self):
        data = request.get_json()
        result = wallet.get_record(data['id'])

        return result

    @marshal_with(schema.record_fields)
    def post(self):
        data = request.get_json()
        result = wallet.add_record(data)

        return result

    @marshal_with(schema.record_fields)
    def put(self):
        data = request.get_json()
        result = wallet.edit_record(data)

        return result

    @marshal_with(schema.record_fields)
    def delete(self):
        data = request.get_json()
        result = wallet.delete_record(data['id'])

        return result
