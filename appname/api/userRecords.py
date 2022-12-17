from flask_restful import marshal_with
from flask_restful import fields

from appname.api import Resource, BaseAPISchema, wallet

class UserRecordsSchema(BaseAPISchema):
    get_fields = {
        'id': fields.Integer,
        'date': fields.String,
        'amount': fields.Integer,
        'notes': fields.String,
        'is_income': fields.Boolean,
    }

class UserRecords(Resource):
    schema = UserRecordsSchema()

    @marshal_with(schema.get_fields)
    def get(self):
        return wallet.get_records()
