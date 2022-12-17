from flask_restful import marshal_with
from flask_restful import fields

from appname.api import Resource, BaseAPISchema, wallet

class StatisticSchema(BaseAPISchema):
    get_fields = {
        'month': fields.String,
        'income': fields.Integer,
        'expense': fields.Integer,
    }

class Statistic(Resource):
    schema = StatisticSchema()

    @marshal_with(schema.get_fields)
    def get(self):
        result = wallet.get_statistic()
        return result
