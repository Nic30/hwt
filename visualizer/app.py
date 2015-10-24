from flask import Flask, render_template, Response
from flask.helpers import send_from_directory
import json

from vhdl_toolkit.samples.superDMA_complex import superDMA_complex
from vhdl_toolkit.synthetisator.signal import PortConnection
from vhdl_toolkit.variables import PortItem
from hls_connections import connectionsBp as connectionsBp

app = Flask(__name__)

# https://leanpub.com/D3-Tips-and-Tricks/read
# http://www.d3noob.org/2013/03/d3js-force-directed-graph-examples.html
# http://blog.pixelingene.com/demos/d3_tree/
# http://bl.ocks.org/Neilos/584b9a5d44d5fe00f779
# http://www.jointjs.com/tutorial/ports
# http://gojs.net/latest/samples/dynamicPorts.html
# http://bl.ocks.org/GerHobbelt/3104394
# http://bl.ocks.org/mbostock/3681006    --zoom
# http://www.codeproject.com/Articles/709340/Implementing-a-Flowchart-with-SVG-and-AngularJS
# http://www.coppelia.io/2014/07/an-a-to-z-of-extra-features-for-the-d3-force-layout/
# http://bl.ocks.org/explunit/5603250
# http://www.ece.northwestern.edu/~haizhou/357/lec6.pdf
# http://bl.ocks.org/lgersman/5310854                 -- selection 

@app.route('/static/<path:path>') # for loading all static files (antipatent, but it is necessary because app is not deployed on webserver )
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return render_template('index.html')

# http://roberto.open-lab.com/2012/06/14/the-javascript-gantt-odyssey/
@app.route('/gantt/')
def gantt():
    return render_template('hls/gantt_chart.html', ganttTasks=[], ganttTaskNames=[])



if __name__ == '__main__':
    app.register_blueprint(connectionsBp)
    app.debug = True
    app.run()
