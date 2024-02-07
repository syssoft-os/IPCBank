from flask import Blueprint, render_template, request, redirect, session, url_for, Response
from flask_sqlalchemy import SQLAlchemy
import auth
from datetime import datetime
import json
import threading
import time
import subprocess
import os

api_blueprint = Blueprint("api", __name__)
db = SQLAlchemy()


class JobWorker():
    active = False;
    job = None;
    execution = None

    def run_binary(self, args):
        try:
            process = subprocess.run(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=False,
                check=True,
            )
            result = process.stdout
            return result.decode("utf-8")
        except subprocess.CalledProcessError as e:
            print(e)
            return None

    def update_jobs(self, app):
        with app.app_context():
            while True:
                db.session.expire_all()
                job_list = jobs.query.filter(
                    (jobs.c_time.is_(None)) |
                    (jobs.java_time.is_(None)) |
                    (jobs.python_threads_time.is_(None)) |
                    (jobs.python_msgq_time.is_(None)) |
                    (jobs.python_pipes_time.is_(None)) |
                    (jobs.clojure_time.is_(None))
                ).all()
                if job_list:
                    self.job = job_list[0]
                    if self.job.c_time is None:
                        self.execution = "c"
                        if (not self.active):
                            continue
                        start_time = time.time()
                        output = self.run_binary(['./bin/programs/c/bank_konto_c', str(self.job.seed),
                                                  str(self.job.number_of_accounts),
                                                  str(self.job.budget_min),
                                                  str(self.job.budget_max),
                                                  str(self.job.transfer_min),
                                                  str(self.job.transfer_max),
                                                  str(self.job.number_of_clients),
                                                  str(self.job.transactions_per_client)])
                        end_time = time.time()
                        if (output):
                            self.job.c_output = json.loads(output)
                            self.job.c_time = end_time - start_time
                            db.session.add(self.job)
                            db.session.commit()

                    elif self.job.python_threads_time is None:
                        self.execution = "python_threads"
                        if (not self.active):
                            continue
                        start_time = time.time()
                        output = self.run_binary(['python', './bin/programs/python/SingleProcess.py', str(self.job.seed),
                                                  str(self.job.number_of_accounts),
                                                  str(self.job.budget_min),
                                                  str(self.job.budget_max),
                                                  str(self.job.transfer_min),
                                                  str(self.job.transfer_max),
                                                  str(self.job.number_of_clients),
                                                  str(self.job.transactions_per_client)])
                        end_time = time.time()
                        if (output):
                            self.job.python_threads_output = json.loads(output)
                            self.job.python_threads_time = end_time - start_time
                            db.session.add(self.job)
                            db.session.commit()
                    
                    elif self.job.python_msgq_time is None:
                        self.execution = "python_msgq"
                        if (not self.active):
                            continue
                        start_time = time.time()
                        output = self.run_binary(['python', './bin/programs/python/MessageQueue.py', str(self.job.seed),
                                                  str(self.job.number_of_accounts),
                                                  str(self.job.budget_min),
                                                  str(self.job.budget_max),
                                                  str(self.job.transfer_min),
                                                  str(self.job.transfer_max),
                                                  str(self.job.number_of_clients),
                                                  str(self.job.transactions_per_client)])
                        end_time = time.time()
                        if (output):
                            self.job.python_msgq_output = json.loads(output)
                            self.job.python_msgq_time = end_time - start_time
                            db.session.add(self.job)
                            db.session.commit()
                            
                    elif self.job.python_pipes_time is None:
                        self.execution = "python_pipes"
                        if (not self.active):
                            continue
                        start_time = time.time()
                        output = self.run_binary(['python', './bin/programs/python/Pipes.py', str(self.job.seed),
                                                  str(self.job.number_of_accounts),
                                                  str(self.job.budget_min),
                                                  str(self.job.budget_max),
                                                  str(self.job.transfer_min),
                                                  str(self.job.transfer_max),
                                                  str(self.job.number_of_clients),
                                                  str(self.job.transactions_per_client)])
                        end_time = time.time()
                        if (output):
                            self.job.python_pipes_output = json.loads(output)
                            self.job.python_pipes_time = end_time - start_time
                            db.session.add(self.job)
                            db.session.commit()

                    elif self.job.java_time is None:
                        self.execution = "java"
                        if (not self.active):
                            continue
                        start_time = time.time()
                        output = self.run_binary(['java', '-jar', './bin/programs/java/java_threads.jar',str(self.job.seed),
                                                  str(self.job.number_of_accounts),
                                                  str(self.job.budget_min),
                                                  str(self.job.budget_max),
                                                  str(self.job.transfer_min),
                                                  str(self.job.transfer_max),
                                                  str(self.job.number_of_clients),
                                                  str(self.job.transactions_per_client)])
                        end_time = time.time()
                        if (output):
                            self.job.java_output = json.loads(output)
                            self.job.java_time = end_time - start_time
                            db.session.add(self.job)
                            db.session.commit()

                    elif self.job.clojure_time is None:
                        self.execution = "clojure"
                        if (not self.active):
                            continue
                        start_time = time.time()
                        output = self.run_binary(['java', '-jar', './bin/programs/clojure/bank_konto.jar',str(self.job.seed),
                                                  str(self.job.number_of_accounts),
                                                  str(self.job.budget_min),
                                                  str(self.job.budget_max),
                                                  str(self.job.transfer_min),
                                                  str(self.job.transfer_max),
                                                  str(self.job.number_of_clients),
                                                  str(self.job.transactions_per_client)])
                        end_time = time.time()
                        if (output):
                            self.job.clojure_output = json.loads(output)
                            self.job.clojure_time = end_time - start_time
                            db.session.add(self.job)
                            db.session.commit()
                else:
                    self.job = None
                    self.active = False;
                    time.sleep(5)


jobWorker = JobWorker()


def initJobWorker(app):
    thread = threading.Thread(target=jobWorker.update_jobs, args=(app,))
    thread.daemon = True
    thread.start()


class jobs(db.Model):
    _id = db.Column("id", db.String(14), primary_key=True)
    seed = db.Column(db.String(64))
    number_of_accounts = db.Column(db.Integer)
    budget_min = db.Column(db.Integer)
    budget_max = db.Column(db.Integer)
    transfer_min = db.Column(db.Integer)
    transfer_max = db.Column(db.Integer)
    number_of_clients = db.Column(db.Integer)
    transactions_per_client = db.Column(db.Integer)
    c_time = db.Column(db.Float)
    java_time = db.Column(db.Float)
    python_threads_time = db.Column(db.Float)
    python_msgq_time = db.Column(db.Float)
    python_pipes_time = db.Column(db.Float)
    clojure_time = db.Column(db.Float)
    c_output = db.Column(db.JSON)
    java_output = db.Column(db.JSON)
    python_threads_output = db.Column(db.JSON)
    python_msgq_output = db.Column(db.JSON)
    python_pipes_output = db.Column(db.JSON)
    clojure_output = db.Column(db.JSON)

    def __init__(self, id):
        self._id = id


@api_blueprint.route("/job/status")
def api_job_status():
    return Response(str(jobWorker.active), content_type="text/plain")


@api_blueprint.route("/job/start")
def api_job_start():
    jobWorker.active = True
    return Response(str(jobWorker.active), content_type="text/plain")


@api_blueprint.route("/job/stop")
def api_job_end():
    jobWorker.active = False
    return Response(str(jobWorker.active), content_type="text/plain")


@api_blueprint.route("/job/add", methods=["POST"])
def api_job_add():
    auth.is_granted()
    jid = generate_timestamp()
    found_job = jobs.query.filter_by(_id=jid).first()
    if found_job:
        return Response("-1", content_type="text/plain")
    else:
        job = jobs(jid)
        job.seed = request.form.get('seed')
        job.number_of_accounts = request.form.get('number_of_accounts')
        job.budget_min = request.form.get('budget_min')
        job.budget_max = request.form.get('budget_max')
        job.transfer_min = request.form.get('transfer_min')
        job.transfer_max = request.form.get('transfer_max')
        job.number_of_clients = request.form.get('number_of_clients')
        job.transactions_per_client = request.form.get('transactions_per_client')
        db.session.add(job)
        db.session.commit()
    return Response("1", content_type="text/plain")


@api_blueprint.route("/job/list")
def api_job_list():
    auth.is_granted()
    job_list = jobs.query.filter(
        (jobs.c_time.is_(None)) |
        (jobs.java_time.is_(None)) |
        (jobs.python_threads_time.is_(None)) |
        (jobs.python_msgq_time.is_(None)) |
        (jobs.python_pipes_time.is_(None)) |
        (jobs.clojure_time.is_(None))
    ).all()

    job_list_json = [
        {
            "_id": job._id,
            "seed": job.seed,
            "number_of_accounts": job.number_of_accounts,
            "budget_min": job.budget_min,
            "budget_max": job.budget_max,
            "transfer_min": job.transfer_min,
            "transfer_max": job.transfer_max,
            "number_of_clients": job.number_of_clients,
            "transactions_per_client": job.transactions_per_client,
            "c_time": job.c_time,
            "java_time": job.java_time,
            "python_threads_time": job.python_threads_time,
            "python_msgq_time": job.python_msgq_time,
            "python_pipes_time": job.python_pipes_time,
            "clojure_time": job.clojure_time,
        } for job in job_list
    ]

    output = {}
    output["active"] = str(jobWorker.active)
    output["current_job"] = None
    if jobWorker.job:
        output["current_job"] = {
            "_id": jobWorker.job._id,
            "seed": jobWorker.job.seed,
            "number_of_accounts": jobWorker.job.number_of_accounts,
            "budget_min": jobWorker.job.budget_min,
            "budget_max": jobWorker.job.budget_max,
            "transfer_min": jobWorker.job.transfer_min,
            "transfer_max": jobWorker.job.transfer_max,
            "number_of_clients": jobWorker.job.number_of_clients,
            "transactions_per_client": jobWorker.job.transactions_per_client,
            "c_time": jobWorker.job.c_time,
            "java_time": jobWorker.job.java_time,
            "python_threads_time": jobWorker.job.python_threads_time,
            "python_msgq_time": jobWorker.job.python_msgq_time,
            "python_pipes_time": jobWorker.job.python_pipes_time,
            "clojure_time": jobWorker.job.clojure_time,
            "execution": jobWorker.execution
        }
    output["job_list"] = job_list_json
    return Response(json.dumps(output), content_type="application/json")


@api_blueprint.route("/job/finished")
def api_job_finished():
    auth.is_granted()
    job_list = jobs.query.filter(
        (jobs.c_time.isnot(None)) &
        (jobs.java_time.isnot(None)) &
        (jobs.python_threads_time.isnot(None)) &
        (jobs.python_msgq_time.isnot(None)) &
        (jobs.python_pipes_time.isnot(None)) &
        (jobs.clojure_time.isnot(None))
    ).all()

    job_list_json = [
        {
            "_id": job._id,
            "seed": job.seed,
            "number_of_accounts": job.number_of_accounts,
            "budget_min": job.budget_min,
            "budget_max": job.budget_max,
            "transfer_min": job.transfer_min,
            "transfer_max": job.transfer_max,
            "number_of_clients": job.number_of_clients,
            "transactions_per_client": job.transactions_per_client,
            "c_time": job.c_time,
            "java_time": job.java_time,
            "python_threads_time": job.python_threads_time,
            "python_msgq_time": job.python_msgq_time,
            "python_pipes_time": job.python_pipes_time,
            "clojure_time": job.clojure_time,
        } for job in job_list
    ]

    return Response(json.dumps(job_list_json), content_type="application/json")


@api_blueprint.route("/job/get", methods=["POST"])
def api_get_finished():
    auth.is_granted()

    data = request.get_json()
    requested_id = data.get("id", None)

    job = jobs.query.get(requested_id)

    if job is None:
        return Response(json.dumps("-1"), content_type="application/json")

    # Create JSON response including all fields
    job_json = {
        "_id": job._id,
        "seed": job.seed,
        "number_of_accounts": job.number_of_accounts,
        "budget_min": job.budget_min,
        "budget_max": job.budget_max,
        "transfer_min": job.transfer_min,
        "transfer_max": job.transfer_max,
        "number_of_clients": job.number_of_clients,
        "transactions_per_client": job.transactions_per_client,
        "c_time": job.c_time,
        "java_time": job.java_time,
        "python_threads_time": job.python_threads_time,
        "python_msgq_time": job.python_msgq_time,
        "python_pipes_time": job.python_pipes_time,
        "clojure_time": job.clojure_time,
        "c_output": job.c_output[2:],
        "java_output": job.java_output[2:],
        "python_threads_output": job.python_threads_output[2:],
        "python_msgq_output": job.python_msgq_output[2:],
        "python_pipes_output": job.python_pipes_output[2:],
        "clojure_output": job.clojure_output[2:],
        "c_balance": job.c_output[:2],
        "java_balance": job.java_output[:2],
        "python_threads_balance": job.python_threads_output[:2],
        "python_msgq_balance": job.python_msgq_output[:2],
        "python_pipes_balance": job.python_pipes_output[:2],
        "clojure_balance": job.clojure_output[:2]
    }

    return Response(json.dumps(job_json), content_type="application/json")


def generate_timestamp():
    current_time = datetime.now()
    timestamp = current_time.strftime("%Y%m%d%H%M%S")
    return timestamp
