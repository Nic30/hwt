function doesRectangleOverlap(a, b) {
	  return (Math.abs(a.x - b.x) * 2 < (a.width + b.width)) &&
	         (Math.abs(a.y - b.y) * 2 < (a.height + b.height));
}

function offsetInRoutingNode(node, net){
	var x= 0,
		y= 0;
	
	var xindx= node.vertical.indexOf(net);
	if(xindx > 0)
		x += xindx*NET_PADDING;
	
	var yindx= node.horizontal.indexOf(net);
	if(yindx > 0)
		y += yindx*NET_PADDING;
	
	return [x, y];
}


function pointAdd(a, b){
	return [a[0] +b[0], a[1] + b[1]]
}

function isOnLineVerticaly(line, point){
	if(line[0][1] < line[1][1]){
		var lUp = line[0];
		var lDown = line[1];
	}else{
		var lUp = line[1];
		var lDown = line[0];
	}
	if(lUp[0] != lDown[0]){ // if this is not vertical line, point does not lay on vertically 
		return false;
	}
	if(point[0] == lUp[0]){ // x == line.x
		return lUp[1] <= point[1] && point[1] <= lDown[1]; // is between lUp and lDown vertically
	}else{
		return false;
	}
}

function pointEq(pointA , pointB){
	return pointA[0] == pointB[0] && pointA[1] == pointB[1];
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
		  			return d.net === net;
	  		  });
}
function higlightNets(nets){
	d3.selectAll(".link")
	  .classed("link-selected", 
			  function(d){
		  			return nets.indexOf(d.net ) >-1; 
	  		  });
}
function netMouseOut() {
	d3.selectAll(".link")
	  .classed("link-selected", false);
}

function addShadows(svg){
	// filters go in defs element
	var defs = svg.append("defs");

	// create filter with id #drop-shadow
	// height=130% so that the shadow is not clipped
	var filter = defs.append("filter")
	    .attr("id", "drop-shadow")
	    .attr("height", "130%");

	// SourceAlpha refers to opacity of graphic that this filter will be applied to
	// convolve that with a Gaussian with standard deviation 3 and store result
	// in blur
	filter.append("feGaussianBlur")
	    .attr("in", "SourceAlpha")
	    .attr("stdDeviation", 1)
	    .attr("result", "blur");

	// translate output of Gaussian blur to the right and downwards with 2px
	// store result in offsetBlur
	filter.append("feOffset")
	    .attr("in", "blur")
	    .attr("dx", 2)
	    .attr("dy", 2)
	    .attr("result", "offsetBlur");

	// overlay original SourceGraphic over translated blurred opacity by using
	// feMerge filter. Order of specifying inputs is important!
	var feMerge = filter.append("feMerge");

	feMerge.append("feMergeNode")
	    .attr("in", "offsetBlur")
	feMerge.append("feMergeNode")
	    .attr("in", "SourceGraphic");

	//gradient
	var minY = 10;
	var maxY = 210;

	var gradient = svg
		.append("linearGradient")
		.attr("y1", minY)
		.attr("y2", maxY)
		.attr("x1", "0")
		.attr("x2", "0")
		.attr("id", "gradient")
		.attr("gradientUnits", "userSpaceOnUse")
    
	gradient
	.append("stop")
	.attr("offset", "0")
	.attr("stop-color", "#E6E6E6")
    
	gradient
    .append("stop")
    .attr("offset", "0.5")
    .attr("stop-color", "#A9D0F5")    
}

function showTooltip(toolTipDiv, html){
	toolTipDiv.transition()        
	    .duration(100)      
	    .style("opacity", .9);      
	toolTipDiv.html(html)
	    .style("left", d3.event.pageX + "px")     
	    .style("top", (d3.event.pageY - 28) + "px");  
}
function hideTooltip(toolTipDiv){
	toolTipDiv.transition()        
		.duration(200)      
		.style("opacity", 0);
}

function updateNetLayout(svgGroup, toolTipDiv, linkElements, nodes, links){ // move component on its positions and redraw links between them
	//move component on its position

	var router = new NetRouter(nodes, links);
	var grid = router.grid;
	router.route();
	
	create debug dots for routing nodes
	(function debugRouterDots(){
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
			}) 
		    .on("mouseover", function(d) {
		    	var html = d.pos() + "</br><b>horizontal:</b><ol>"
					d.horizontal.forEach(function (net){
						if (net)
							html += "<li>" + net.name  + "</li>";
					});
		    	html += "</ol><b>vertical:</b><ol>";
		    	d.vertical.forEach(function (net){
		    		if (net)
		    			html += "<li>" + net.name  + "</li>";
				});
		    	html += "</ol>";
		    	showTooltip(toolTipDiv, html);
		    	var connectedNets = [];
		    	d.horizontal.forEach(function (n){
		    		connectedNets.push(n);
		    	})
		    	d.vertical.forEach(function (n){
		    		connectedNets.push(n);
		    	})
		    	higlightNets(connectedNets);
		    })                  
		    .on("mouseout", function(d) {       
		    	hideTooltip(toolTipDiv);   
		    	netMouseOut();
		    });
		
		//// line to parent componet
		//svgGroup.selectAll("#debuglink")
		//	.data(flatenMap)
		//	.enter()
		//	.append("path") 
		//	.classed({"link": true})
		//	.attr("d", function (d) {
		//        var sx = d.pos()[0];
		//        var sy = d.pos()[1];
		//        var tx = d.originComponent.x;
		//        var ty = d.originComponent.y ;
		//        return "M" + sx + "," + sy + " L " + tx + "," + ty;
		//    });
	})();
	

	function drawNet(d){
		var pos = d.start.pos();
		var spOffset = offsetInRoutingNode(d.start, d.net);
		var pathStr = "M " + [pos[0] - COMPONENT_PADDING - d.source.netChannelPadding.right, pos[1]] + "\n"; //connection from port node to port
		var posWithOffset = pointAdd(pos, spOffset);
		pathStr += " L " + posWithOffset +"\n";

		router.walkLinkSubPaths(d, function(subPath, dir){
			var p0 = subPath[0];
			var p1 = subPath[subPath.length -1];
			
			pathStr += " L " + pointAdd(p0.pos(), offsetInRoutingNode(p0, d.net)); +"\n";
			pathStr += " L " + pointAdd(p1.pos(), offsetInRoutingNode(p1, d.net)); +"\n";
		});
		
		pos = d.end.pos();
		pathStr += " L " + [pos[0]+COMPONENT_PADDING +d.target.netChannelPadding.left, pos[1]]+"\n"; //connection from port node to port
		return pathStr;
	}
		
		
	linkElements.attr("d", drawNet);

	
	links.forEach(function (link){ //rm tmp variables
		delete link.path;
		delete link.end;
		delete link.start;
	});
	
};

function ComponentDiagram(selector, nodes, links){ //main function for rendering components layout
	var wrapper = d3.select(selector);
	wrapper.selectAll("svg").remove(); // delete old on redraw

	var svg = wrapper.append("svg");
	var svgGroup= svg.append("g"); // because of zooming/moving

	addShadows(svg);

	//grid higlight
    var linkElements = svgGroup.selectAll(".link")
    	.data(links)
    	.enter()
    	.append("path")
    	.classed({"link": true})
    	.on("mouseover", netMouseOver)
    	.on("mouseout", netMouseOut);

	var toolTipDiv = d3.select("body")
		.append("div")   
	    .attr("id", "tooltip")               
	    .style("opacity", 0);
    for(var i =0; i< 3; i++)
    	updateNetLayout(svgGroup, toolTipDiv, linkElements, nodes, links);


    var place = svg.node().getBoundingClientRect();
	//force for self organizing of diagram
	var force = d3.layout.force()
		.gravity(.00)
		.distance(150)
		.charge(-2000)
		.size([place.width, place.height])
		//.nodes(nodes)
		//.links(links)
		//.start();
	drawExternalPorts(svgGroup, nodes.filter(function (n){
			return n.isExternalPort;
		}));
	drawComponents(svgGroup, nodes.filter(function (n){
			return !n.isExternalPort;
		}))
		.call(force.drag); //component dragging

    // define the zoomListener which calls the zoom function on the "zoom" event constrained within the scaleExtents
    var zoomListener = d3.behavior.zoom()
    	.scaleExtent([0.2, 30])
    	.on("zoom", function () {
    			svgGroup.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    	});
    (function fitDiagram2Screen(zoomListener){
        function diagramSize(){
        	var widthMax = 0;
        	var heigthtMax = 0;
        	nodes.forEach(function (n){
        		widthMax = Math.max(n.x + n.width + COMPONENT_PADDING, widthMax);
        		heigthtMax = Math.max(n.y + n.height +COMPONENT_PADDING, heigthtMax);
        	});
        	return [widthMax, heigthtMax];
        }
        var size = diagramSize();
        var scaleX = place.width /size[0] ;
        var scaleY = place.height / size[1];
        var scale = Math.min(scaleX, scaleY); 
        //this is processiong of zoomListener explicit translate and scale on start
        zoomListener.translate([0,0])
        	.scale(scale);
        zoomListener.event(svg.transition()
        					  .duration(100));
    })(zoomListener);
    
    svg.call(zoomListener);

    
    d3.select('body')
    	.call(d3.keybinding("keydown")
    	    .on('p', function (){
    	    	showTooltip(toolTipDiv, d3.mouse(this))
    	    })
    	).call(d3.keybinding("keyup")
        	    .on('p', function (){
        	    	hideTooltip(toolTipDiv)
        	    })
        );
    
}