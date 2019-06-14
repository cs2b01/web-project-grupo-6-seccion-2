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
    session['logged']=None
    session['category']=None
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

@app.route('/current', methods=['GET'])
def current():
    sessiondb = db.getSession(engine)
    user = sessiondb.query(entities.User).filter(entities.User.id == session['logged']).first()
    js = json.dumps(user, cls=connector.AlchemyEncoder)
    return Response(js, status=200, mimetype='application/json')


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
        password=c['password'],
        record=0,
        uploads=0)
        sessiondb.add(user)
        sessiondb.commit()
        message = {'message': 'Authorized'}
        return Response(message, status=200, mimetype='application/json')
    else:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')


##############################################
#                                            #
#    EDIT AND DELETE ACCOUNT IN SETTINGS     #
#                                            #
##############################################

@app.route('/users', methods = ['PUT'])
def update_user():
    time.sleep(1)
    sessiondb = db.getSession(engine)
    c =  json.loads(request.data)
    try:
        user = sessiondb.query(entities.User).filter(entities.User.id == session['logged']).first()
        for key in c.keys():
            setattr(user, key, c[key])
        sessiondb.add(user)
        sessiondb.commit()
        message = {'message': 'Authorized'}
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')

@app.route('/users', methods = ['DELETE'])
def delete_user():
    session_db = db.getSession(engine)
    try:
        users = session_db.query(entities.User).filter(entities.User.id == session['logged'])
        for user in users:
            session_db.delete(user)
        session_db.commit()
        message = {'message': 'Authorized'}
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')

##############################################
#                                            #
#                 Categories                 #
#                                            #
##############################################

#Solo ejecutar /create_categories si la base de datos se borra para fines de prueba

@app.route('/create_categories', methods = ['GET'])
def create_categories():
    db_session = db.getSession(engine)
    Marvel = entities.Category(name="Marvel")
    Star_Wars = entities.Category(name="Star Wars")
    Anime = entities.Category(name="Anime")
    Deportes = entities.Category(name="Deportes")
    Memes = entities.Category(name="Memes")
    db_session.add(Marvel)
    db_session.add(Star_Wars)
    db_session.add(Anime)
    db_session.add(Deportes)
    db_session.add(Memes)
    db_session.commit()
    return "Categories created!"


@app.route('/categories', methods = ['GET'])
def get_categories():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Category)
    data = []
    for category in dbResponse:
        data.append(category)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/current_category', methods=['GET'])
def current_category():
    sessiondb = db.getSession(engine)
    category = sessiondb.query(entities.Category).filter(entities.Category.id == session['category']).first()
    js = json.dumps(category, cls=connector.AlchemyEncoder)
    return Response(js, status=200, mimetype='application/json')

@app.route('/set_category', methods = ['POST'])
def set_category():
    message = json.loads(request.data)
    id = message['id']
    db_session = db.getSession(engine)
    try:
        category = db_session.query(entities.Category
            ).filter(entities.Category.id == id
            ).one()
        message = {'message': 'Authorized'}
        session['category'] = category.id
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')

##############################################
#                                            #
#                 Questions                  #
#                                            #
##############################################

@app.route('/questions', methods = ['POST'])
def create_question():
    sessiondb = db.getSession(engine)
    c =  json.loads(request.data)
    try:
        user = entities.Question(
        statment=c['statment'],
        answer=c['answer'],
        wrong1=c['wrong1'],
        wrong2=c['wrong2'],
        wrong3=c['wrong3'],
        category_id=c['category_id'])
        sessiondb.add(user)
        sessiondb.commit()
        message = {'message': 'Authorized'}
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')

@app.route('/questions', methods = ['GET'])
def get_questions():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Question)
    data = []
    for user in dbResponse:
        data.append(user)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/users', methods = ['GET'])
def get_users():
    session = db.getSession(engine)
    dbResponse = session.query(entities.User)
    data = []
    for user in dbResponse:
        data.append(user)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')\



@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')



if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
