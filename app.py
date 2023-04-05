from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from random import choice


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
        return f"Short_URL: {self.short_url}\nURL: {self.url}\nCreate date: {datetime.fromtimestamp(self.date)}\n<dop: primary_id = {self.id}>>"
'''
Создание таблиц по указанным моделям
'''
# >>> from ToDoList.app import app, db, TopMenuModel, BotInfoModel
# >>> with app.app_context():
# >>>   db.create_all()




database_imitation = {}
variable_symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z',
                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z',
                    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def create_short_url():
    result = ''
    for _ in range(10):
        result += choice(variable_symbols)
    return result

def event(URL):
    for _ in range(2):
        short_url = create_short_url()
        temp = database_imitation.get('short_url')
        if temp is not None:
            continue
        database_imitation[short_url] = URL
        return short_url




# ОБРАБОТЧИКИ СТРАНИЦ




@app.route('/main')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

