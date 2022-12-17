from flask_restful import marshal_with
from flask_restful import fields

from appname.api import Resource, BaseAPISchema, wallet

class WalletSchema(BaseAPISchema):
    get_fields = {
        'balance': fields.Integer,
    }

class Wallet(Resource):
    schema = WalletSchema()

    @marshal_with(schema.get_fields)
    def get(self):
        balance = wallet.get_balance()
        result = {'balance': balance}
        return result
