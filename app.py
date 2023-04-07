from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from shorter import create_short_url


app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/url_converter'
db = SQLAlchemy(app)


class ModelURL(db.Model):
    __tablename__ = 'url'
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.Text, unique=True)
    url = db.Column(db.Text)
    date = db.Column(db.Float, default=datetime.timestamp(datetime.utcnow()))

    def __repr__(self):
        return f"Short_URL: {self.short_url}\nURL: {self.url}\nCreate date: {datetime.fromtimestamp(self.date)}\n<dop: primary_id = {self.id}>"
'''
Создание таблиц по указанным моделям
'''
# >>> from ToDoList.app import app, db, TopMenuModel, BotInfoModel
# >>> with app.app_context():
# >>>   db.create_all()


# ОБРАБОТЧИКИ СТРАНИЦ


@app.route('/main')
def index():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def event():
    if request.method == 'POST':
        html_request = request.get_json()
        url = html_request['url']
        try:
            short_url = create_short_url()
            db_data = ModelURL.query.filter_by(short_url=short_url).first()
            if db_data is not None:
                temp = {'data': None, 'code': '3', 'comment': 'Created short url already using in DataBase'}
            new_data = ModelURL(short_url=short_url, url=url)
            db.session.add(new_data)
            db.session.commit()
            print('Данные в БД добавлены')
            temp = {'data': f'http://127.0.0.1:5000/{short_url}', 'code': '1', 'comment': 'Short URL created. Added to DataBase'}
        except Exception as e:
            db.session.rollback()
            temp = {'data': None, 'code': '2', 'comment': 'Error on stage work with DataBase'}
            print('Ошибка добавления в БД', str(e))
        content = jsonify(temp)
        response = make_response(content)
        response.headers['Content-Type'] = 'application/json'
        return response
    #return redirect('/main')

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

if __name__ == '__main__':
    app.run(debug=True)
