function doesRectangleOverlap(a, b) {
	  return (Math.abs(a.x - b.x) * 2 < (a.width + b.width)) &&
	         (Math.abs(a.y - b.y) * 2 < (a.height + b.height));
}

// used for collision detection, and keep out behavior of nodes
function nodeColisionResolver(node) {
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

function netMouseOver() {
	var net = d3.select(this)[0][0].__data__.net;
	d3.selectAll(".link")
	  .classed("link-selected", 
			  function(d){
		  			return d.net === net
	  		  });
}
function netMouseOut() {
	d3.selectAll(".link")
	  .classed("link-selected", false);
}




function redraw(nodes, links){ //main function for renderign components layout
	var place = d3.select("#chartWraper").node().getBoundingClientRect();
	d3.select("#chartWraper").selectAll("svg").remove(); // delete old on redraw
	
	//force for self organizing of diagram
	var force = d3.layout.force()
		.gravity(.00)
		.distance(150)
		.charge(-2000)
		.size([place.width, place.height])
		.nodes(nodes)
		.links(links)
		//.start();
	
	var svg = d3.select("#chartWraper").append("svg");
	var svgGroup= svg.append("g"); // because of zooming/moving

	//alias component body
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
	
	// component name [TODO] text nad komponentu
	wrap.append('text')
		.attr("y", 10)
		.text(function(d) {
		    return d.name;
		});

	// [TODO] porty s dratkem ven z komponenty, ruzne typy portu viz stream/bus/wire ve Vivado
	// input port wraps
	var port_inputs = wrap.append("g")
		.attr("transform", function(d) { 
			return "translate(" + 0 + "," + 2*portHeight + ")"; 
		})
		.selectAll("g .port-input")
		.data(function (d){
			return d.inputs;
		})
		.enter()
		.append('g')
		.classed({"port-input": true});
	
	// input port icon [TODO] only for special types of connection, this is only example how to use it
	port_inputs.append("image")
		.attr("xlink:href", function(d) { 
			return "/static/hls/connections/arrow_right.ico"; 
		})
		.attr("y", function(d, i){
			return i*portHeight;
		})
		.attr("width", 10)
		.attr("height", portHeight);
	
	// portName text [TODO] intelligent alignment of port name
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
			var componentWidth = d3.select(this).node().parentNode.getBoundingClientRect().width;
			return "translate(" + componentWidth/2 + "," + 2*portHeight + ")"; 
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
	
	//grid higlight
    var link = svgGroup.selectAll(".link")
    	.data(links)
    	.enter()
    	.append("path")
    	.classed({"link": true})
    	.on("mouseover", netMouseOver)
    	.on("mouseout", netMouseOut);
	

    
    function update(){
    	//move component on its position
		wrap.attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
		var grid = RoutingNodesContainer(nodes);
		
		//create debug dots for routing nodes
		var flatenMap = [];
		grid.visitFromLeftTop(function(c){
			flatenMap.push(c);
		});
		svgGroup.selectAll("circle")
		.data(flatenMap)
		.enter().append("circle")
		.style("fill", "steelblue")
		.attr("r", 2)
		.attr("cx", function(d){
			return d.pos()[0];
		})
		.attr("cy", function(d){
			return d.pos()[1];
		});
		
		// route grids
		for(var i = 0; i< links.length; i++ ){
			var l = links[i];
			l.start = grid.componetOutputNode(l.source, l.sourceIndex);
			l.end = grid.componetInputNode(l.target, l.targetIndex);
			l.path = astar.search(grid, l.start, l.end );
		}
		//// line to parent componet
		//svgGroup.selectAll("#debuglink").data(flatenMap)
		//.enter()
		//.append("path") 
		//.classed({"link": true})
		//.attr("d", function (d) {
        //    var sx = d.pos()[0];
        //    var sy = d.pos()[1];
        //    var tx = d.originComponent.x;
        //    var ty = d.originComponent.y ;
        //    return "M" + sx + "," + sy + " L " + tx + "," + ty;
        //});
		
		//print link between them
    	link.attr("d", function (d) {
			var sp = d.start.pos();
			var pathStr = " M" + [sp[0] - COMPONENT_PADDING , sp[1]]; //connection from port node to port
			pathStr += " L " + sp +"\n";

			for(var pi = 0; pi< d.path.length; pi++){
				var p = d.path[pi];
				pathStr += " L " + p.pos() +"\n";
			}
			var ep = l.end.pos();
			pathStr += " L " + ep +"\n";
			pathStr += " L " + [ep[0]+COMPONENT_PADDING, ep[1]]+"\n";
			

			return pathStr;
    		//            var sx = d.source.x + d.source.width;
			//            var sy = d.source.y + portsOffset + d.sourceIndex * portHeight;
			//            var tx = d.target.x;
			//            var ty = d.target.y + portsOffset + d.targetIndex * portHeight;
			//            return "M" + sx + "," + sy + " L " + tx + "," + ty;
        });
	};
	
    //force.on("tick", function () {
    //	var q = d3.geom.quadtree(nodes),
    //        i = 0,
    //        n = nodes.length;
    //
    //	while (++i < n) 
    //		q.visit(nodeColisionResolver(nodes[i]));
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