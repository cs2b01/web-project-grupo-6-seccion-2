from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time
import datetime
import random
from operator import  itemgetter,attrgetter



db = connector.Manager()
engine = db.createEngine()
cache = {} # Users cache
application=app = Flask(__name__)
app.secret_key = ".."


##############################################
#                                            #
#                   RENDER                   #
#                                            #
##############################################
@app.route('/')
def index():
    session['logged']=None
    session['category']=None
    session['category_question']=None
    return render_template('dologin.html')

@app.route('/dologin')
def dologin():
    return render_template('dologin.html')

@app.route('/gracias')
def gracias():
    return render_template('gracias.html')


@app.route('/juego')
def juego():
    return render_template('juego.html')


@app.route('/main_menu')
def main_menu():
    return render_template('main_menu.html')


@app.route('/rankings')
def rankings():
    return render_template('rankings.html')

@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/subir_contenido')
def subir_contenido():
    return render_template('subir_contenido.html')
@app.route('/subir_pregunta')
def subir_pregunta():
    return render_template('subir_pregunta.html')


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

##############################################
#                                            #
#                 Rankings                   #
#                                            #
##############################################

@app.route('/rankings_uploads', methods = ['GET'])
def rankings_uploads():
    session = db.getSession(engine)
    users = session.query(entities.User)
    data = []
    for user in users:
        data.append(user)
    data=sorted(data,key=attrgetter('uploads'),reverse=True)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/rankings_record', methods = ['GET'])
def rankings_record():
    session = db.getSession(engine)
    users = session.query(entities.User)
    data = []
    for user in users:
        data.append(user)
    data=sorted(data,key=attrgetter('record'),reverse=True)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

##############################################
#                                            #
#             Get Users w/Cache              #
#                                            #
##############################################

@app.route('/users', methods = ['GET'])
def get_users():
    key = 'getUsers'
    if key not in cache.keys():
        session = db.getSession(engine)
        dbResponse = session.query(entities.User)
        cache[key] = dbResponse
    users = cache[key]
    response = []
    for user in users:
        response.append(user)
    return json.dumps(response, cls=connector.AlchemyEncoder)


##############################################
#                                            #
#                    Game                    #
#                                            #
##############################################


@app.route('/set_category_and_random_question', methods = ['POST'])
def set_category_question():
    message = json.loads(request.data)
    id = message['id']
    db_session = db.getSession(engine)
    try:
        category = db_session.query(entities.Category
            ).filter(entities.Category.id == id
            ).one()
        category_id = category.id
        data = []
        categoryX=db_session.query(entities.Question).filter(entities.Question.category_id==category_id)
        for category in categoryX:
            data.append(category)
        randomx=random.choice(data)
        return Response(json.dumps(randomx, cls=connector.AlchemyEncoder), mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')


##############################################
#                                            #
#                   Run                      #
#                                            #
##############################################

if __name__ == '__main__':
    app.run()

