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
		//.nodes(nodes)
		//.links(links)
		//.start();
	
	var svg = d3.select("#chartWraper").append("svg");
	var svgGroup= svg.append("g"); // because of zooming/moving

	/**add shadow*************************************/
	//Dufam ze navadi ze som to skopirovala :D ak pojde ten tien inac radsej to prerobme
	
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

	/************************************/

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
	    .classed({"component": true})
	    .attr("border", 1)
	    .style("stroke", "#BDBDBD")
	    .attr("fill", "url(#gradient)")
	    .style("filter", "url(#drop-shadow)")
	    .attr("width", function(d) { return d.width})
	    .attr("height", function(d) { return d.height});
	
	//var externalPorts = wrap.filter( function(d){ return d.inputs.length + d.outputs.length == 1});	
	//externalPorts.classed({"external-port" :true});
	//wrap = wrap.filter( function(d){ return d.inputs.length + d.outputs.length != 1});	


	// component name [TODO] text nad komponentu
	wrap.append('text')
		.classed({"component-title": true})
		.attr("y", 0)	
		.attr("x", function(d){
			return d.width/2;
		})
		.text(function(d) {
		    return d.name;
		})
		//.attr("font-size", 40);

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
			return (i-0.5)*portHeight;
		})
		.attr("width", 10)
		.attr("height", portHeight);
	
	// portName text [TODO] intelligent alignment of port name
	port_inputs.append('text')
		.attr("x", 10)
		.attr("y", function(d, i){
			return (i+0.3)*portHeight;
		})
		.attr("height", portHeight)
		.text(function(portName) { 
			return portName; 
		});
	
	// output port wraps
	var port_out = wrap.append("g")
		.attr("transform", function(d) { 
			var componentWidth = d3.select(this).node().parentNode.getBoundingClientRect().width;
			return "translate(" + componentWidth + "," + 2*portHeight + ")"; 
		})
		.selectAll("g .port-group")
		.data(function (d){
			return d.outputs;
		})
		.enter()
		.append('g')
		.classed({"port-output": true});

	//  output port image
	port_out.append("image")
		.attr("xlink:href", function(d) { 
			return "/static/hls/connections/arrow_right.ico"; 
		})
		.attr("x", -10)
		.attr("y", function(d, i){
			return (i-0.5)*portHeight;
		})
		.attr("width", 10)
		.attr("height", portHeight);	

	// portName text
	port_out.append('text') 
		.attr("x", -10)	// posunuty okrej o 10 dolava
		.attr("y", function(d, i){
			return (i+0.3)*portHeight; //Zuzana: neviem ci je spravne manualne posunutie prvku ale vyzera to dobre, zalezi aj od velkosti fontu
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
		var grid = new RoutingNodesContainer(nodes);
		
		////create debug dots for routing nodes
		//var flatenMap = [];
		//grid.visitFromLeftTop(function(c){
		//	flatenMap.push(c);
		//});
		//svgGroup.selectAll("circle")
		//.data(flatenMap)
		//.enter().append("circle")
		//.style("fill", "steelblue")
		//.attr("r", 2)
		//.attr("cx", function(d){
		//	return d.pos()[0];
		//})
		//.attr("cy", function(d){
		//	return d.pos()[1];
		//});
		
		// route grids
		links.forEach(function (l){
			l.start = grid.componetOutputNode(l.source, l.sourceIndex);
			l.end = grid.componetInputNode(l.target, l.targetIndex);
			l.path = astar.search(grid, l.start, l.end );
		});
		grid.visitFromLeftTop(function (n){
			n.vertical = [];
			n.horizontal = [];
		});
		/*
		 * paths keep out ideology:
		 *  for each routing node build vertical and horizontal netlist
		 *    if path is curved in this node vertical index == horizontal index
		 *    if there is path from same net join them
		 *  for each component increase padding to let space for nets
		 *  from each node extract routing node position for this path (use horizontal and/or vertical index, this node pos and NET_PADDING )
		 *  draw path    
		 * */
		function walkLinkPath(link, fn){
			if( !link.path || link.path.length == 0){
				fn(link.start,link.end);
			}else{
				fn(link.start, link.path[0]);
				for(var i =0; i< link.path.length; i++){
					if(i==link.path.length -1){
						fn(link.path[i], link.end);
					}else{
						fn(link.path[i],link.path[i+1]);
					}
				}
			}
			fn(link.end);	
		}
		function add2routingNode(arrA, arrB, net){
			if(arrA.indexOf(net) >= 0){
				return; // net is already routed on this node
			}
			var minIndex = arrB.indexOf(net);
			if(minIndex < 0)
				minIndex =0;
			if(minIndex < arrA.length)
				minIndex = arrA.length;
			arrA[minIndex] = net;
		}
		function add2verticalList(node, link){
			add2routingNode(node.vertical, node.horizontal, link.net);
		}
		function add2horizontalList(node, link){
			add2routingNode(node.horizontal, node.vertical, link.net);
		}
		
		links.forEach(function (link){
			walkLinkPath(link, function (node, next){
				if(next){
					if(node.left == next || node.right == next){
						add2verticalList(node, link);
					}
					if(node.top == next || node.bottom == next){
						add2horizontalList(node, link);
					}
				}else{
					add2horizontalList(node, link);
					//add2verticalList(node, link);
				}
			});
		})

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
		function offsetFromNodeNetLists(node, net){
			var x= NET_PADDING,
				y= NET_PADDING;
			
			var xindx= node.horizontal.indexOf(net);
			if(xindx > 0)
				x += xindx*NET_PADDING;
			
			var yindx= node.vertical.indexOf(net);
			if(yindx > 0)
				y += yindx*NET_PADDING;
			
			return [x, y];
		}
		function pointAdd(a, b){
			a[0] += b[0];
			a[1] += b[1];			
		}
		//print link between them
    	link.attr("d", function (d) {
			var sp = d.start.pos();
			var spOffset = offsetFromNodeNetLists(d.start, d.net);
			var pathStr = " M" + [sp[0] - COMPONENT_PADDING , sp[1]]; //connection from port node to port
			pointAdd(sp, spOffset);
			pathStr += " L " + sp +"\n";

			for(var pi = 0; pi< d.path.length; pi++){
				var p = d.path[pi];
				spOffset = offsetFromNodeNetLists(p, d.net);
				sp = p.pos();
				pointAdd(sp, spOffset);
				pathStr += " L " + sp +"\n";
			}
			var ep = d.end.pos();
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