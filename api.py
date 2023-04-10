from flask import Flask
from flask_sqlalchemy import SQLAlchemy, session
from datetime import datetime
from shorter import create_short_url


app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/url_converter'
db = SQLAlchemy(app)
BASE_URL = 'http://127.0.0.1:5000/'


class ModelURL(db.Model):
    __tablename__ = 'url'
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.Text, unique=True)
    url = db.Column(db.Text)
    date = db.Column(db.Float, default=datetime.timestamp(datetime.utcnow()))

    def __repr__(self):
        return f"Short_URL: {self.short_url}\nURL: {self.url}\nCreate date: {datetime.fromtimestamp(self.date)}\n<dop: primary_id = {self.id}>"

class ModelFeedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.Text)
    date = db.Column(db.Float, default=datetime.timestamp(datetime.utcnow()))

    def __repr__(self):
        return f"Обращение № {self.id}\nПолучено: {datetime.fromtimestamp(self.date)}\nСообщение: {self.msg}"

class Service:
    @staticmethod
    def add_url(url):
        db_data = ModelURL.query.filter_by(url=url).first()
        if db_data is not None:
            return {'data': f'{BASE_URL}{db_data.short_url}', 'comment': 'There is this URL in DataBase already. Returned corresponding short URL from DataBase.'}
        else:
            short_url = create_short_url()
            db_data = ModelURL.query.filter_by(short_url=short_url).first()
            if db_data is None:
                new_ses = session.Session(db)
                with new_ses.begin():
                    new_data = ModelURL(short_url=short_url, url=url)
                    db.session.add(new_data)
                    db.session.commit()
                return {'data': f'{BASE_URL}{short_url}', 'comment': 'Your URL added to DataBase. Short URL returned.'}
            else:
                return {'data': None, 'comment': 'There is created short URL in DataBase already.'}

    @staticmethod
    def add_feedback(msg):
        db_data = ModelFeedback.query.filter_by(msg=msg).first()
        if db_data is not None:
            date = f"Дата обращения: {datetime.fromtimestamp(db_data.date).strftime('%d.%m.%Y')}"
            return {'data': 'Обращение с идентичным содержимым уже зарегистрировано.', 'date': date, 'code': False}
        else:
            new_ses = session.Session(db)
            with new_ses.begin():
                new_data = ModelFeedback(msg=msg)
                db.session.add(new_data)
                db.session.commit()
            date = f"Дата Вашего обращения: {datetime.fromtimestamp(ModelFeedback.query.filter_by(msg=msg).first().date).strftime('%d.%m.%Y')}"
            return {'data': 'Ваще обращение успешно зарегистрировано.', 'date': date, 'code': True}

    def is_correct(self, short_url):
        self.db_data = ModelURL.query.filter_by(short_url=short_url).first()
        return False if self.db_data is None else True