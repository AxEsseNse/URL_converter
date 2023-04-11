'''
1. pip install alembic
Устанавливаем библиотеку

2. cd /project directory
Заходим в терминале в каталог с проектом

3. alembic init alembic
В этом каталоге создаются конфигурационные файлы библиотеки alembic в папке с тем же названием
+ файфл alembic.ini в папке venv

4. Edit alembic.ini
Редактируем файл alembic.ini
Вставляем  наш URL в строчку с sqlalchemy.url = ...
sqlalchemy.url = postgresql://admin:admin@localhost:5432/url_converter

5. Импортируем все наши модели
Заходим в папку alembic
Открываем env.py
Импортируем модели
from app import ModelURL, ModelFeedback

6. Создание миграции
alembic revision -m 'some message'
Создается файл миграции с заданным сообщением
Далее вручную прописываем как хотим изменить нашу базу данных
Создать таблицу\удалить таблицу\добавить столбец и другое
в функции upgrade() прописываем изменения, которые нужны для перехода в следующее состояние
в функции downgrad() прописываем как отменить эти изменения

7. Пройти по всем миграциям до последней
alembic upgrade head
От текущего состояния БД переходит в последнее (через все оставшиеся миграции - ревизии)

8. Узнать на каком этапе миграции наша БД
alembic current
Если прописано в скобках (head) - это последняя версия

9. Отображение истории миграций
alembic history --verbose

10. Даунгрейд миграции
alembic downgrade -1
Отменяет одну миграцию вниз

11. Даунгрейд до нуля
alembic downgrade base
'''

'''
Примеры миграций

def upgrade() -> None:
    op.create_table('alemurl',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('short_url', sa.Text(), unique=True),
                    sa.Column('url', sa.Text(), unique=True),
                    sa.Column('date_creating', sa.Float(), default=datetime.timestamp(datetime.utcnow())),
                    )


def downgrade() -> None:
    op.drop_table('alemurl')
    
///=====

def upgrade() -> None:
    op.add_column('alemurl', sa.Column('date_last_use', sa.Float(), default=datetime.timestamp(datetime.utcnow())))


def downgrade() -> None:
    op.drop_column('alemurl', 'date_last_use') 
'''