var component = {
		id : 0,
		name : "component name",
		inputs : [ "clk", "rst" ],
		outputs : [ "outA", "outB" ]
}
var component2 = {
		id:1,
		name : "component name2",
		inputs : [ "clk2", "rst2" ],
		outputs : [ "outA2", "outB2" ]	
}
var clk = {
		id: 2,
		name : "clk",
		inputs : [],
		outputs : ["clk"]	
}
var nodes = [component, component2, clk];
var links = [ {"source": component, "sourceIndex": 0, "target": component2, "targetIndex": 0}, 
              {"source": component, "sourceIndex": 1, "target": component2, "targetIndex": 1}, 
              {"source": clk, "sourceIndex": 0, "target": component, "targetIndex": 0}   ]
var columnWidth = 120;
var portHeight = 10;

function trim(a , boundry){
	if(a > boundry)
		return boundry;
	if (a <  0)
		return 0;
	return a;
}

function ReDiscoveredErr(message) {
	this.name = 'ReDiscoveredErr';
	this.message = message ;
	this.stack = (new Error()).stack;
}
ReDiscoveredErr.prototype = Object.create(Error.prototype);
ReDiscoveredErr.prototype.constructor = ReDiscoveredErr;

function ColumnContainer(){
	var self = {};
	self.left = [];
	self.midleRight = [];
	self.push = function(indx, elm){
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
		
	}
	self.accessFromLeft = function (indx){
		var leftLen = self.left.length;
		if(indx < leftLen){
			return self.left[indx];
		}else{
			return self.midleRight[indx - leftLen];
		}
	}
	self.length = function() {
		return self.left.length + self.midleRight.length;
	}
	return self;
}

function components2columns(nodes, links){ // discover component with most ports (bigger) then go on both sides and assign components to columns
	function findBiggestComponent(nodes){
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
	function constructTriplets(nodes, links){
		var triplets = [];
		function Triplet(){
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
	
	for(var x = 0; x< columns.length(); x++){
		var c = columns.accessFromLeft(x);	
		for(var y =0; y < c.length; y++ ){
			var component = c[y]; 
			component.x = columnWidth * x;
			component.y = 20;
			component.width = columnWidth;
			component.height = portHeight*3 + portHeight * Math.max(component.inputs.length, component.outputs.length);
		}
	}
}

function doRectangleIntersect( a,  b) {
	  return (Math.abs(a.x - b.x) * 2 < (a.width + b.width)) &&
	         (Math.abs(a.y - b.y) * 2 < (a.height + b.height));
}

// used for collision detection
function collide(node) {
	 //var  nx1 = node.x,
	 //     nx2 = node.x + node.width,
	 //     ny1 = node.y,
	 //     ny2 = node.y + node.height;
	  return function(quad, x1, y1, x2, y2) {
		 // var doesColide = doRectangleIntersect(node, quad.point)  //x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
		// 
		// if (doesColide && quad.point && (quad.point !== node)) {
		//	  
		//	  var dx0 = node.x - quad.point.x,
		//	      dy0 = node.y - quad.point.y,
		//		  l = (l - node.width) / l * .5;
		//		  node.x -= dx *= l;
		//		  node.y -= dy *= l;
		//		  quad.point.x += dx;
		//		  quad.point.y += dy;
		//	  }
		// }
		  return false; // doesColide;
	  };
}

components2columns(nodes, links);

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


	var portsOffset = 3*portHeight - portHeight/2;
	var wrap = svg.selectAll("g")
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
	
	// port icon
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
	
    var link = svg.selectAll(".link")
    	.data(links)
    	.enter()
    	.append("path")
    	.classed({"link": true});
	
    force.on("tick", function () {
    	var q = d3.geom.quadtree(nodes),
            i = 0,
            n = nodes.length;

    	while (++i < n) 
    		q.visit(collide(nodes[i]));
    	
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
        
    });
    
}
redraw();

