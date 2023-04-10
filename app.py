from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy, session
from datetime import datetime
from shorter import create_short_url


# Конфигурация
app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/url_converter'
db = SQLAlchemy(app)
BASE_URL = 'http://127.0.0.1:5000/'


# Модели таблиц БД
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


# Сервис
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
            return {'data': f'Обращение с идентичным содержимым уже зарегистрировано. Дата обращения: {datetime.fromtimestamp(db_data.date)}'}
        else:
            new_ses = session.Session(db)
            with new_ses.begin():
                new_data = ModelFeedback(msg=msg)
                db.session.add(new_data)
                db.session.commit()
            return {'data': 'Ваще обращение успешно зарегистрировано.'}


# ОБРАБОТЧИКИ СТРАНИЦ


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<short_url>')
def link(short_url):
    try:
        db_data = ModelURL.query.filter_by(short_url=short_url).first()
        if db_data is None:
            temp = {'data': None, 'code': '12', 'comment': 'There is not this short URL in DataBase'}
        else:
            temp = {'data': db_data.url, 'code': '11', 'comment': 'Short URL executed from DataBase'}
    except Exception as e:
        temp = {'data': None, 'code': '13', 'comment': 'Error on stage work with DataBase'}
        print('Ошибка соединения с БД', str(e))
    if temp['data'] is None:
        return render_template('wrong.html', data=temp)
    else:
        return render_template('redirect.html', data=temp)


# API
@app.post('/api/main')
def event():
    html_request = request.get_json()
    url = html_request['url']

    service = Service()
    #user_session = session.Session
    temp = service.add_url(url)

    content = jsonify(temp)
    response = make_response(content)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.post('/api/feedback')
def feedback():
    html_request = request.get_json()
    msg = html_request['msg']

    service = Service()
    temp = service.add_feedback(msg)

    content = jsonify(temp)
    response = make_response(content)
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == '__main__':
    app.run(debug=True)
