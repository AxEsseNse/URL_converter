from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


# Table Models
class ModelURL(db.Model):
    __tablename__ = 'url'
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.Text, unique=True)
    url = db.Column(db.Text, unique=True)
    date_creating = db.Column(db.Float, default=datetime.timestamp(datetime.utcnow()))
    count_use = db.Column(db.Integer, default=1)
    date_last_use = db.Column(db.Float)


    def __repr__(self):
        return f'ModelURL PK:{self.id}'

    def __str__(self):
        return f"\
Short_URL: {self.short_url}\n\
URL: {self.url}\n\
Create date: {datetime.fromtimestamp(self.date_creating)}\n\
Count use: {self.count_use}\n\
Last use: {datetime.fromtimestamp(self.date_last_use)}\n\
<dop: primary_id = {self.id}>"


class ModelFeedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.Text)
    date = db.Column(db.Float, default=datetime.timestamp(datetime.utcnow()))

    def __repr__(self):
        return f'ModelFeedback PK:{self.id}'

    def __str__(self):
        return f"\
Обращение № {self.id}\n\
Получено: {datetime.fromtimestamp(self.date)}\n\
Сообщение: {self.msg}\n"
