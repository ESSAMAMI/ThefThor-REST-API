from flask import Flask, render_template, redirect, url_for, request, session, Response
import socket
import os
from random import shuffle
import shutil
from pymongo import MongoClient
import json
from datetime import datetime
from EDPwd import EncryptDecryptPwd
import pandas as pd
import uu

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route( '/', methods=['GET'] )
def home() :
	return render_template('landing.html')
	#return "<body style='font-family: sans-serif;background-color:#524876; color:#fff'><center><div style='height:32%'></div><h1 style='font-size:100px;'>SERVER <span style='color:#179482'>POSTER</span></h1></center></body>"

@app.route( '/app/forget_password', methods=['GET'] )
def forget_password() :
	return "OK"


@app.route( '/app/console/stop_run_camera/<userid>', methods=['GET'] )
def stop_run_camera(userid) :
    pass
    try:

        print("USER ID===============>", userid)
        # Creating a pymongo client
        client = MongoClient('mongodb://mymongodbusername:qzdihgvolihgseoihfoqzdhaqzoiuufhaqozzfhgao@mongo:27017/')
        #Getting the database instance
        db = client['db_project']
        conf = db.configuration.find({'user_id': int(userid)})[0]
        if conf['system_on']:
            db.configuration.update({'user_id': int(userid)},{'$set': {'system_on': False}}, upsert=False, multi=False)
        else:
            db.configuration.update({'user_id': int(userid)},{'$set': {'system_on': True}}, upsert=False, multi=False)

        df = pd.DataFrame([db.configuration.find({'user_id': 2})[0]])
        df['_id'] = df['_id'].astype('str')
        response = json.dumps(json.loads(df.to_json(orient="records")))
        return Response( response , status=200 , mimetype='text/html' )

    except Exception as e:
        print('===========>', e)
        response = json.dumps(json.loads(pd.DataFrame().to_json(orient="records")))
        return Response( response , status=500 , mimetype='text/html' )
	

@app.route( '/app/connection/<login>.<pwd>', methods=['GET'])
def connection(login, pwd) :

    # Creating a pymongo client
    client = MongoClient('mongodb://mymongodbusername:qzdihgvolihgseoihfoqzdhaqzoiuufhaqozzfhgao@mongo:27017/')
    #Getting the database instance
    db = client['db_project']
    try:

        user = db.user.find({ "login": login})[0]
        pwd_crypted = user['pwd']
        edp = EncryptDecryptPwd()
        pwd_decrypted = edp.decrypt_pwd(pwd_crypted).decode("utf-8")
        assert pwd == pwd_decrypted
        df = pd.DataFrame([user])
	############################################
        db.user.update({'login': 'h.essamami@admin.com'},{'$set': {'last_connection': str(datetime.today().strftime('%Y-%m-%d'))}}, upsert=False, multi=False)
        ############################################
    except Exception as e:
        print(e)
        user = {}
    if bool(user) == True:
        response = json.dumps(json.loads(df.to_json(orient="records")))
    else:
        response = json.dumps(json.loads(pd.DataFrame().to_json(orient="records")))
    return Response( response , status=200 , mimetype='text/html' )


################################### ALERTS ##################################

@app.route( '/app/alerts/<int:id>', methods=['GET'])
def get_alerts(id) :
    # Creating a pymongo client
    #client = MongoClient('localhost', 27017)
    client = MongoClient('mongodb://mymongodbusername:qzdihgvolihgseoihfoqzdhaqzoiuufhaqozzfhgao@mongo:27017/')

    #Getting the database instance
    db = client['db_project']
    alerts = {}
    try:
        df_alerts = pd.DataFrame(db.notifications.find({'user_id':int(id)}))
        print(df_alerts)
    except Exception as e:
        print(e)
        return e

    if bool(df_alerts.empty) != True:
        response = json.dumps(json.loads(df_alerts.to_json(orient="records")))
    else:
        response = json.dumps(json.loads(pd.DataFrame().to_json(orient="records")))
    return Response( response , status=200 , mimetype='text/html' )

#####################################################################################
@app.route( '/notifications/more_info/<notification_id>.token_id=<token>', methods=['GET'])
def more_info(notification_id, token):
    try:
        # Creating a pymongo client
        client = MongoClient('mongodb://mymongodbusername:qzdihgvolihgseoihfoqzdhaqzoiuufhaqozzfhgao@mongo:27017/')
        #Getting the database instance
        db = client['db_project']

        user = db.user.find({ "pwd": token.encode()})[0]
        
        notifications = db.notifications.find({ "_id":int(notification_id)})[0]
        # TODO: Create folder if not exists for user to put the video which asked to show...
        datetime_requested = str(datetime.now()).replace(' ','_').split('.')[0].replace(':','_').replace('-','_')
        path = 'static/videos/'+str(user['_id'])+'/'
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)
            
        url_video = 'static/videos/%s/video_%s%s' % (user['_id'],datetime_requested,'.mp4')
        url_file = 'static/videos/%s/video_%s%s' % (user['_id'],datetime_requested,'.txt')
        if not os.path.isdir(path):
            os.mkdir(path)
        videos_bytes = notifications['contents']['frames']
        #convert str bytes to txt file, then in video
        if len(videos_bytes) > 500:
            out_file = open(url_file, "w") # open for [w]riting as [b]inary
            out_file.write(videos_bytes)
            out_file.close()
            #save video using uu to decode data
            uu.decode(url_file, url_video)
            #delete txt file
            os.remove(url_file)
        else:
            url_video = ""
        return render_template('more_info.html', name=user['name'], notifications=notifications, url=url_video)
    except Exception as e:
        print("===============>",e)
        return render_template('landing.html')

if __name__ == '__main__':

    #hostname = socket.gethostname()
    app.run(debug=True, host="0.0.0.0", port=8000)
