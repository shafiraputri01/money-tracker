import logging
from appname.models import db, Model, ModelProxy, transaction

logger = logging.getLogger(__name__)

class Record(Model):
    """
    A record is a financial records, include income and outcome.
    """

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.ForeignKey("user.id"), index=True,
                           nullable=False)

    date = db.Column(db.Date(), nullable=False)
    amount = db.Column(db.BigInteger(), nullable=False)
    notes = db.Column(db.String(255))
    is_income = db.Column(db.Boolean())

    user = db.relationship("User", foreign_keys=[user_id])

    GDPR_EXPORT_COLUMNS = {
        "id": "ID of the record",
        "hashid": "ID of User",
        "date": "When the money is used",
        "amount": "Amount of money",
        "notes": "Notes of the finacial record",
        "is_income": "Is the finacial record an income",
    }


    # @classmethod
    # @transaction
    # def create(cls, name, creator):
    #     new_team = cls(name=name, creator=creator)
    #     new_team_member = ModelProxy.teams.TeamMember(team=new_team, user=creator, role='administrator', activated=True)

    #     db.session.add(new_team)
    #     db.session.add(new_team_member)
    #     db.session.commit()
    #     return new_team
