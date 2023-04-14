from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy, session
from datetime import datetime
from shorter import create_short_url
from validators import url as url_validator
#from api import Service


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
                    db.session.flush()
                    new_data.date_last_use = new_data.date_creating
                    # Показать как работает вывод в консоль
                    #print([new_data])
                    #print(new_data)
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
                # Показать как работает вывод в консоль
                #db.session.flush()
                #print([new_data])
                #print(new_data)
                db.session.commit()
            date = f"Дата Вашего обращения: {datetime.fromtimestamp(ModelFeedback.query.filter_by(msg=msg).first().date).strftime('%d.%m.%Y')}"
            return {'data': 'Ваще обращение успешно зарегистрировано.', 'date': date, 'code': True}

    def link_url(self, short_url):
        if self.is_correct(short_url):
            new_ses = session.Session(db)
            with new_ses.begin():
                self.db_data.count_use += 1
                self.db_data.date_last_use = datetime.timestamp(datetime.utcnow())
                db.session.commit()
            return {'data': self.db_data.url, 'comment': 'URL executed from DataBase'}
        else:
            raise Exception('short url incorrect')

    def is_correct(self, short_url):
        self.db_data = ModelURL.query.filter_by(short_url=short_url).first()
        return False if self.db_data is None else True


# ОБРАБОТЧИКИ СТРАНИЦ


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<short_url>')
def link(short_url):
    service = Service() ### Жека, этот экземпляр надо как-то удалять? Типо они сами удаляются или мы так и будем хранить миллион экземпляров?
    try:
        data = service.link_url(short_url)
        return render_template('redirect.html', data=data)
    except Exception as e:
        print(e)
        data = {'data': None, 'comment': 'There is not this short URL in DataBase'}
        return render_template('wrong.html', data=data)


# API
@app.post('/api/main')
def event():
    html_request = request.get_json()
    url = html_request['url']

    if url_validator(url):
        service = Service()
        temp = service.add_url(url)
    else:
        temp = {'data': 'incorrect url', 'comment': 'URL incorrect'}

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
