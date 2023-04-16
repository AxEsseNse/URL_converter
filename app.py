from flask import Flask, render_template, request, jsonify, make_response
from db_model import db
from service import Service
from validators import url as url_validator


# config
app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/url_converter'
db.init_app(app)


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
