from flask import Flask, render_template
from flask.helpers import send_from_directory
import json


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


@app.route('/connections/')
def connections():
    return render_template('hls/connections.html')
@app.route('/connections-tests/')
def connections_test():
    return render_template('hls/connections_test.html')


@app.route('/test/')
def test():
    class Component:
        def __init__(self, name, file):
            self.name = name
            self.file = file
        def to_json(self):
            return {"id": id(self), "name" : self.name, "file": self.file}
                             
    class Connection:
        def __init__(self, compA, compA_portName, compB, compB_portName):
            self.compA = compA
            self.compA_portName = compA_portName
            self.compB = compB
            self.compB_portName = compB_portName
        def to_json(self):
            return {"compA_id":id(self.compA), "compA_portName": self.compA_portName, "compB_id":  id(self.compB), "compB_portName": self.compB_portName }
    c0 = Component("compA", "./compA.vhd")
    c1 = Component("compB", "./compB.vhd")
    a = {"components" : [c0, c1], 'connections': [Connection(c0, "portA", c1, "portA"), Connection(c1, "portB", c0, "portB")]}
    
    def _default(obj):
        if hasattr(obj, "to_json"):
            return obj.to_json()
        
        return obj.__dict__

    
    return json.dumps(a, default=_default)

if __name__ == '__main__':
    app.debug = True
    app.run()
