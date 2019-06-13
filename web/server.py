from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time
import datetime
from operator import  itemgetter,attrgetter

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)


##############################################
#                                            #
#                   RENDER                   #
#                                            #
##############################################
@app.route('/')
def index():
    return render_template('dologin.html')


@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

##############################################
#                                            #
#                   LOGIN                    #
#                                            #
##############################################


@app.route('/authenticate', methods = ['POST'])
def authenticate():
    message = json.loads(request.data)
    email = message['email']
    password = message['password']
    db_session = db.getSession(engine)
    try:
        user = db_session.query(entities.User
            ).filter(entities.User.email == email
            ).filter(entities.User.password == password
            ).one()
        message = {'message': 'Authorized'}
        session['logged'] = user.id
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')

##############################################
#                                            #
#                  REGISTER                  #
#                                            #
##############################################
@app.route('/users', methods = ['POST'])
def create_user():
    sessiondb = db.getSession(engine)
    c =  json.loads(request.data)
    data = []
    users=sessiondb.query(entities.User).filter(entities.User.email== c['email'])
    for user in users:
        data.append(user)
    if(len(data)==0):
        user = entities.User(
        username=c['username'],
        email=c['email'],
        name=c['name'],
        lastname=c['lastname'],
        password=c['password'])
        sessiondb.add(user)
        sessiondb.commit()
        message = {'message': 'Authorized'}
        return Response(message, status=200, mimetype='application/json')
    else:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')












@app.route('/users', methods = ['GET'])
def get_users():
    session = db.getSession(engine)
    dbResponse = session.query(entities.User)
    data = []
    for user in dbResponse:
        data.append(user)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')

@app.route('/create_test_users', methods = ['GET'])
def create_test_users():
    db_session = db.getSession(engine)
    user = entities.User(name="David", lastname="Lazo", password="1234", username="qwerty", email="davidlazo@gmail.com")
    db_session.add(user)
    db_session.commit()
    return "Test user created!"


@app.route('/users', methods = ['PUT'])
def update_user():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated User'

@app.route('/users', methods = ['DELETE'])
def delete_user():
    id = request.form['key']
    session = db.getSession(engine)
    users = session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        session.delete(user)
    session.commit()
    return "Deleted User"



@app.route('/current', methods = ['GET'])
def current():
    sessiondb = db.getSession(engine)
    user = sessiondb.query(entities.User).filter(entities.User.id == session['logged']).first()
    js = json.dumps(user, cls=connector.AlchemyEncoder)
    return Response(js, status=200, mimetype='application/json')

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
