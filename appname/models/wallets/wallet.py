import logging
from appname.models import db, Model, ModelProxy, transaction

logger = logging.getLogger(__name__)

class Wallet(Model):
    """
    A record is a financial records, include income and outcome.
    """

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.ForeignKey("user.id"), index=True, nullable=False)

    amount = db.Column(db.BigInteger(), nullable=False)

    user = db.relationship("User", foreign_keys=[user_id])

    GDPR_EXPORT_COLUMNS = {
        "id": "ID of the record",
        "hashid": "ID of User",
        "amount": "Amount of money",
    }
