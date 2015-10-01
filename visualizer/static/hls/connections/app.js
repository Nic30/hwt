//var nodes = [{
//		id : 0,
//		name : "component name",
//		inputs : [ "clk", "rst" ],
//		outputs : [ "outA", "outB" ]
//	}, {
//		id:1,
//		name : "component name2",
//		inputs : [ "clk2", "rst2" ],
//		outputs : [ "outA2", "outB2" ]	
//	}, {
//		id: 2,
//		name : "clk",
//		inputs : [],
//		outputs : ["clk"]	
//	}];
//var links = [ {"source": 0, "sourceIndex": 0, "target": 1, "targetIndex": 0}, 
//              {"source": 0, "sourceIndex": 1, "target": 1, "targetIndex": 1}, 
//              {"source": 2, "sourceIndex": 0, "target": 0, "targetIndex": 0}];

var nodes = [{
		id : 0,
		name : "smaller one",
		inputs : [ "clk", "rst" ],
		outputs : [ "outA", "outB" ]
	}, {
		id:1,
		name : "biggest",
		inputs : [ "clk2", "rst2", "inA", "inB"],
		outputs : [ "outA2", "outB2" ]	
	}, {
		id: 2,
		name : "clk",
		inputs : [],
		outputs : ["clk"]	
	}];
var links = [ {"source": 2, "sourceIndex": 0, "target": 1, "targetIndex": 0}, 
              {"source": 0, "sourceIndex": 1, "target": 1, "targetIndex": 2}, 
              {"source": 2, "sourceIndex": 0, "target": 0, "targetIndex": 0}];



var columnWidth = 120;
var portHeight = 10;
var COMPONENT_PADDING = 40;

// replaces ID with node object
function resolveNodesInLinks(nodes, links){
	var dict = {};
	for(var i=0; i< nodes.length; i++){
		var n =nodes[i];
		dict[n.id] =n;
	}
	for(var i=0; i< links.length; i++){
		var l = links[i];
		var s = dict[l.source];
		var t = dict[l.target];
		if(s === undefined || t == undefined ){
			throw "Can not resolve link source or target";
		}
		l.source = s;
		l.target = t;
	}	
}

function trim(a , boundry){
	if(a > boundry)
		return boundry;
	if (a <  0)
		return 0;
	return a;
}


function ReDiscoveredErr(message) { //is exception
	this.name = 'ReDiscoveredErr';
	this.message = message ;
	this.stack = (new Error()).stack;
}
ReDiscoveredErr.prototype = Object.create(Error.prototype);
ReDiscoveredErr.prototype.constructor = ReDiscoveredErr;

// Column container is like an array which allow negative indexing and indexing from most left (and ColumnContainer() is its constructor)
function ColumnContainer(){
	var self = {
			left : [],
			midleRight : [],
			push : function(indx, elm){
				var arr;
				if(indx < 0){
					arr= self.left;
					indx = -indx -1;
				} else {
					arr = self.midleRight;
				}
				if(! arr[indx]){
					arr[indx] = [];
				}
				arr[indx].push(elm); 
				
			},	
			accessFromLeft : function (indx){
				var leftLen = self.left.length;
				if(indx < leftLen){
					return self.left[indx];
				}else{
					return self.midleRight[indx - leftLen];
				}
			},
			length : function() {
				return self.left.length + self.midleRight.length;
			}	
	};
	return self;
}

function components2columns(nodes, links){ // discover component with most ports (bigger) then go on both sides and assign components to columns
	function findBiggestComponent(nodes){ // find component with biggest no of ports
		var biggestComponent = null;
		for(var i =0; i<nodes.length; i++){
			var c = nodes[i];
			if(biggestComponent){
				var portCnt = biggestComponent.inputs.length + biggestComponent.outputs.length;
				var thisCompPortCnt = c.inputs.length + c.outputs.length;
				if(thisCompPortCnt > portCnt)
					biggestComponent = c;
			}else{
				biggestComponent = c;
			}
		}	
		return biggestComponent;
	}
	function constructTriplets(nodes, links){ //for each node discover what is on left and right side
		var triplets = [];
		function Triplet(){ // triplet obj constructor
			return { me: null, left: new Set(), right:new Set()};
		}
		for(var i =0; i<nodes.length; i++){
			var c = nodes[i];
			var t = new Triplet();
			t.me = c;
			for(var i2 =0; i2 < links.length; i2++){
				var l = links[i2];
				if(l.target == c && l.source != c) 
					t.left.add(l.source)
				if(l.source == c && l.target != c)
					t.right.add(l.target)
			}
			triplets.push(t);
		}
		return triplets;
	}

	
	var columns = new ColumnContainer();
	var biggestComponent = findBiggestComponent(nodes);
	var triplets = constructTriplets(nodes, links);

	// now take triplets and build columns out of them
	// go from biggest component on left and right at symetricaly,
	// use set to control if this component was discovered
	var discovered = new Set();
	function popTriplet( component){
		if(discovered.has(component))
			throw new ReDiscoveredErr();
		
		for(var index =0;index< triplets.length; index++ ){
			if(triplets[index].me == component)
				break;
		}
		if(index == triplets.length)
			throw "this component is not in triplets"
		var triplet = triplets[index];
		triplets.splice(index, 1);
		discovered.add(triplet.me);
		return triplet;
	}
	
	function makeColumns(baseIndx, triplet){
		function discoverSide(sideSet, indxShift){
			sideSet.forEach(function (c) {
				try {
					makeColumns(baseIndx+indxShift, popTriplet(c));
				} catch (e){
					if (e instanceof ReDiscoveredErr) {
					//	console.log("found same " +c.name )
					}else 
						throw e;
				}
			});	
		}
		discoverSide(triplet.left, -1);
		discoverSide(triplet.right, 1);

		columns.push(baseIndx, triplet.me);
	}
	makeColumns(0, popTriplet(biggestComponent));
	
	function heightOfPrevious(column, myIndx){
		var y =0;
		for(var i =0; i < myIndx; i++ ){
			y+= column[i].height + COMPONENT_PADDING;
		}
		return y;
	}
	
	for(var x = 0; x< columns.length(); x++){
		var column = columns.accessFromLeft(x);	
		for(var y =0; y < column.length; y++ ){
			var component = column[y]; 
			console.log(component.name + "\n");
			component.x = (columnWidth +COMPONENT_PADDING)* x;
			component.y = heightOfPrevious(column, y);
			component.width = columnWidth;
			component.height = portHeight*3 + portHeight * Math.max(component.inputs.length, component.outputs.length);
		}
	}
}

function doesRectangleOverlap(a, b) {
	  return (Math.abs(a.x - b.x) * 2 < (a.width + b.width)) &&
	         (Math.abs(a.y - b.y) * 2 < (a.height + b.height));
}

// used for collision detection, and keep out behavior of nodes
function collide(node) {
	  var nx1, nx2, ny1, ny2, padding;
	  padding = 32;
	  function x2(node){
		  return node.x + node.width; 
	  }
	  function y2(node){
		  return node.y + node.height; 
	  }
	  nx1 = node.x - padding;
	  nx2 = x2(node) + padding;
	  ny1 = node.y - padding;
	  ny2 = y2(node.y) + padding;
	  
	  
	  return function(quad, x1, y1, x2, y2) {
	    var dx, dy;
		function x2(node){
		 return node.x + node.width; 
		}
		function y2(node){
		 return node.y + node.height; 
		}
	    if (quad.point && (quad.point !== node)) {
	      if (doesRectangleOverlap(node, quad.point)) {
	        dx = Math.min(x2(node)- quad.point.x, x2(quad.point) - node.x) / 2;
	        node.x -= dx;
	        quad.point.x -= dx;
	        dy = Math.min(y2(node) - quad.point.y,y2(quad.point) - node.y) / 2;
	        node.y -= dy;
	        quad.point.y += dy;
	      }
	    }
	    return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
	  };
};

function redraw(){ //main function for renderign components layout
	var place = d3.select("#chartWraper")
		.node()
		.getBoundingClientRect();
	d3.select("#chartWraper").selectAll("svg").remove(); // delete old on redraw
	
	//force for self organizing of diagram
	var force = d3.layout.force()
		.gravity(.05)
		.distance(150)
		.charge(function(d, i) { return i ? 0 : -2000; })
		.size([place.width, place.height])
		.nodes(nodes)
		.links(links)
		.start();
	
	var svg = d3.select("#chartWraper").append("svg");
	var svgGroup= svg.append("g");;


	var portsOffset = 3*portHeight - portHeight/2;
	var wrap = svgGroup.selectAll("g")
		.data(nodes)
		.enter()
		.append("g")
	    .classed({"component": true})
	    .attr("transform", function(d) {
	    	return "translate(" + [ d.x,d.y ] + ")"; 
	    })
	    .call(force.drag); //component dragging
	
	// background
	wrap.append("rect")
	    .attr("rx", 5) // this make rounded corners
	    .attr("ry", 5)
	    .attr("width", function(d) { return d.width})
	    .attr("height", function(d) { return d.height});
	
	// component name
	wrap.append('text')
		.attr("y", 10)
		.text(function(d) {
		    return d.name;
		});

	
	// input port wraps
	var port_inputs = wrap.append("g")
		.attr("transform", function(d) { 
			return "translate(" + 0 + "," + 3*portHeight + ")"; 
		})
		.selectAll("g .port-input")
		.data(function (d){
			return d.inputs;
		})
		.enter()
		.append('g')
		.classed({"port-input": true});
	
	// input port icon
	port_inputs.append("image")
		.attr("xlink:href", function(d) { 
			return "/static/hls/connections/arrow_right.ico"; 
		})
		.attr("y", function(d, i){
			return (i-1)*portHeight;
		})
		.attr("width", 10)
		.attr("height", portHeight);
	
	// portName text
	port_inputs.append('text')
		.attr("x", 10)
		.attr("y", function(d, i){
			return i*portHeight;
		})
		.attr("height", portHeight)
		.text(function(portName) { 
			return portName; 
		});
	
	// output port wraps
	var port_out = wrap.append("g")
		.attr("transform", function(d) { 
			var componentWidth = d3.select(this).node().parentNode.getBoundingClientRect().width
			return "translate(" + componentWidth/2 + "," + 3*portHeight + ")"; 
		})
		.selectAll("g .port-group")
		.data(function (d){
			return d.outputs;
		})
		.enter()
		.append('g')
		.classed({"port-output": true});
	
	// portName text
	port_out.append('text')
		.attr("x", 10)
		.attr("y", function(d, i){
			return i*portHeight;
		})
		.attr("height", portHeight)
		.text(function(portName) { 
			return portName; 
		});
	
    var link = svgGroup.selectAll(".link")
    	.data(links)
    	.enter()
    	.append("path")
    	.classed({"link": true});
	
    function update(){
		wrap.attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    	link.attr("d", function (d) {
            var sx = d.source.x + d.source.width;
            var sy = d.source.y + portsOffset + d.sourceIndex * portHeight;
            var tx = d.target.x;
            var ty = d.target.y + portsOffset + d.targetIndex * portHeight;
            return "M" + sx + "," + sy + " L " + tx + "," + ty;
        });
	};
	
    //force.on("tick", function () {
    //	var q = d3.geom.quadtree(nodes),
    //        i = 0,
    //        n = nodes.length;
    //
    //	while (++i < n) 
    //		q.visit(collide(nodes[i]));
    //	
    //	update();
    //});
    
    update();
    
    // define the zoomListener which calls the zoom function on the "zoom" event constrained within the scaleExtents
    var zoomListener = d3.behavior.zoom().scaleExtent([0.1, 3]).on("zoom",  
    		function () {
    			svgGroup.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    		}
    );
    svg.call(zoomListener);
}

resolveNodesInLinks(nodes, links);
components2columns(nodes, links);
redraw();

