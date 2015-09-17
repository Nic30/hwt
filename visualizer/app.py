from flask import Flask, render_template
from flask.helpers import send_from_directory


app = Flask(__name__)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/gantt/')
def gantt():
    return render_template('hls/gantt_chart.html', ganttTasks=[], ganttTaskNames=[])


if __name__ == '__main__':
    app.debug = True
    app.run()
