from flask_sqlalchemy import session
from db_model import db, ModelURL, ModelFeedback
from shorter import create_short_url
from datetime import datetime


BASE_URL = 'http://127.0.0.1:5000/'


# Service
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
