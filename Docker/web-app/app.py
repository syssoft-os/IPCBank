from flask import Flask, render_template, session, request, Response
from flask_sqlalchemy import SQLAlchemy
global system_info
import auth
import stream
import api
import time
import threading
from waitress import serve

app = Flask(__name__)

app.secret_key = "swhDNyX7p04HKTooIJbcBWMbqnrk5Ymy"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint( auth.auth_blueprint)
app.register_blueprint( stream.stream_blueprint, url_prefix="/stream")
app.register_blueprint( api.api_blueprint, url_prefix="/api")


api.db.init_app(app)

@app.route("/home/")
@app.route("/")
def home():
    auth.is_granted()
    return render_template("index.html", active="home", system_info=system_info)

@app.route("/logs/<id>")
@app.route("/logs/")
def logs(id=-1):
    auth.is_granted()
    return render_template("logs.html", active="logs", id=id)


@app.route("/generate/")
def generate():
    auth.is_granted()
    return render_template("generate.html", active="generate", system_info=system_info)


if __name__ == "__main__":
    system_info = stream.get_system_info()
    with app.app_context():
        api.db.create_all()
    app.config.update(
    SESSION_COOKIE_SAMESITE="Strict",
    #SESSION_COOKIE_SECURE=True
          )
        
    api.initJobWorker(app)
#    app.run(host="0.0.0.0", port=8080, threaded=False,debug=True)
    print("http://localhost:8080")
    serve(app, host='0.0.0.0', port=8080, _quiet=True)
    

