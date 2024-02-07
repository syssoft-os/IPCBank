from flask import Blueprint, render_template, request, redirect, session, url_for, Response
import json
import time
import psutil
import cpuinfo
import platform
import auth
import subprocess
import os

stream_blueprint = Blueprint("stream", __name__)


def get_system_info():
    system_info = {
        'os': platform.system(),
        'arch': platform.architecture(),
        'freq': psutil.cpu_freq().max,
        'model': cpuinfo.get_cpu_info()['brand_raw'],
        'cores': psutil.cpu_count(logical=True),
        'threads': psutil.cpu_count(logical=False),
        'cpu_percent': psutil.cpu_percent(percpu=True),
        'cpu_percent_mean': psutil.cpu_percent(),
        'r_t': round(psutil.virtual_memory().total / (1024 ** 3),2),
        'r_u': round(psutil.virtual_memory().used / (1024 ** 3),2),
        'r_f': round(psutil.virtual_memory().available / (1024 ** 3),2),
        'r_p': round(psutil.virtual_memory().percent,2),
    }
    return system_info




@stream_blueprint.route("/system_monitor")
def stream_system_monitor():
    auth.is_granted()
    return Response(stream_system_monitor_loop(), content_type="text/event-stream")


@stream_blueprint.route("/seed")
def stream_test_seed():
    auth.is_granted()
    seed = request.args.get('seed')
    return Response(stream_test_seed_loop(seed), content_type="text/event-stream")



def stream_system_monitor_loop():
    client_connected = True
    try:
        while client_connected:
            system_info = get_system_info()
            yield f"data: {json.dumps(system_info)}\n\n"
            time.sleep(1)
    except GeneratorExit:
        print("Client disconnected")
        client_connected = False
    
    
def run_binary(args,tout=None):
    try:
        process = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=False,
            check=True,
            timeout=tout
        )
        result = process.stdout
        return result.decode("utf-8")
    except subprocess.CalledProcessError as e:
        error_message = f'Error: {e.returncode}\n{e.output}'
        return error_message
    
    


def stream_test_seed_loop(seed):
    [x[0] for x in os.walk(".")]
    client_connected = True
    output = {}
    def send_output(output):
        nonlocal client_connected
        if client_connected:
            yield f"data: {json.dumps(output)}\n\n"
    try:
        output["random_c_value"] = run_binary(['./bin/test_seed/random_c', seed],5)
        yield from send_output(output)

        output["random_python_value"] = run_binary(['python', './bin/test_seed/random_py.py', seed],5)
        yield from send_output(output)

        output["random_java_value"] = run_binary(['java', '-jar', './bin/test_seed/random_java.jar', seed],5)
        yield from send_output(output)

        output["random_clojure_value"] = run_binary(['java', '-jar', './bin/test_seed/random_clojure.jar', seed],5)
        yield from send_output(output)
        yield f"data:-1\n\n"


    except GeneratorExit:
        print("Client disconnected")
        client_connected = False
    
