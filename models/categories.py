from datetime import datetime
from dbc import db 


# Alias common DB names
Column = db.Column
Model = db.Model
relationship = db.relationship

class Categories(Model):
    """ User model for storing user related data """

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(64))
    description = Column(db.Text)
    link = Column(db.String(250))
    created_date = Column(db.DateTime, default=datetime.utcnow)
    parent_id = Column(db.Integer, default=0)
    status = Column(db.Boolean, default=False, index=True)
    
    def __init__(self, name, description,link, parent_id, status):
        self.name = name
        self.description = description
        self.link = link
        self.parent_id = parent_id
        self.status = status

    def _asdict(self):
        return self.__dict__
