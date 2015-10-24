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

function updateLayout(svgGroup, componentWrap, linkElements, nodes, links){ // move component on its positions and redraw links between them
	//move component on its position

	var router = new NetRouter(nodes, links);
	var grid = router.grid;
	router.route();
	
	(function moveComponetsOutOfNets(){
		/* find width of channels
		 * add it to component positions
		 * */
		function netPadding(netCnt){
			return netCnt * (NET_PADDING+1);
		}
		
		grid.maxNetCntY = [];
		grid.maxNetCntX = [];
		
		for(var x = 0; x < grid.length; x++){
			var col = grid[x];
			if(col){
				if(grid.maxNetCntX[x] === undefined)
					grid.maxNetCntX[x] = 0;
				for(var y =0; y < grid.length; y++){
					var n = col[y];
					if(n){
						var netCntY = n.horizontal.length;
						var netCntX = n.vertical.length;

						if(grid.maxNetCntY[y] === undefined)
							grid.maxNetCntY[y] = 0;
						if(grid.maxNetCntY[y] < netCntY)
							grid.maxNetCntY[y] = netCntY;
						if(grid.maxNetCntX[x] < netCntX)
							grid.maxNetCntX[x] = netCntX;
					}
				}
			}
		}

		var sumOfNetOffsetsX = [];
		var sumOfNetOffsetsY = [];
		var offset = 0;
		grid.maxNetCntX.forEach(function (d, i){
			if(d){
				offset += netPadding(d);
			}
			sumOfNetOffsetsX[i] = offset;
		});
		offset = 0;
		grid.maxNetCntY.forEach(function (d, i){
			if(d){
				offset += netPadding(d);
			}
			sumOfNetOffsetsY[i] = offset;
		});
		function previousDefined(arr, indx){
			return arr[indx]
			for(var i = indx-1; i >=0; i--){
				var offset  = arr[i];
				if(offset){
					return offset;
				}
			}
			return 0;
		}
		nodes.forEach(function (n){
			var x0 = n.x - COMPONENT_PADDING;
			var x1 = n.x + n.width + COMPONENT_PADDING;
			var y0 =n.y - COMPONENT_PADDING;
			var y1 = n.y + n.height + COMPONENT_PADDING;
			var npTop =  netPadding( previousDefined(grid.maxNetCntY, y0));
			if(npTop)
				n.netChannelPadding.top = npTop;
			var npLeft = netPadding(previousDefined(grid.maxNetCntX, x0));
			if (npLeft)
				n.netChannelPadding.left = npLeft;
			//var npBottom = netPadding(grid.maxNetCntY[y1]);
			//if(npBottom)
			//	n.netChannelPadding.bottom = npBottom;
			//var npRight = netPadding(grid.maxNetCntX[x1]);
			//if(npRight)
			//	n.netChannelPadding.right = npRight;
			var xOffset = sumOfNetOffsetsX[x0];
			if(xOffset  != undefined)
				n.x = xOffset + n.x;
			var yOffset = sumOfNetOffsetsY[y0];
			if(yOffset != undefined)
				n.y = yOffset + n.y;
		});
	})();
	//create debug dots for routing nodes
	(function debugRoterDots(){
		var toolTipDiv = d3.select("body")
			.append("div")   
		    .attr("class", "tooltip")               
		    .style("opacity", 0);
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
		    	
		    	
		    	toolTipDiv.transition()        
		            .duration(100)      
		            .style("opacity", .9);      
		    	toolTipDiv.html(html)
		            .style("left", d3.event.pageX + "px")     
		            .style("top", (d3.event.pageY - 28) + "px");    
		    })                  
		    .on("mouseout", function(d) {       
		    	toolTipDiv.transition()        
		            .duration(200)      
		            .style("opacity", 0);   
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
	
	componentWrap.attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
    });
	(function drawNets(){
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
			a[0] += b[0];
			a[1] += b[1];			
		}
		//print link between them
		linkElements.attr("d", function (d) {
			var sp = d.start.pos();
			var spOffset = offsetInRoutingNode(d.start, d.net);
			var pathStr = " M" + [sp[0] - COMPONENT_PADDING , sp[1]]; //connection from port node to port
			pointAdd(sp, spOffset);
			pathStr += " L " + sp +"\n";
	
			for(var pi = 0; pi< d.path.length; pi++){
				var p = d.path[pi];
				spOffset = offsetInRoutingNode(p, d.net);
				sp = p.pos();
				pointAdd(sp, spOffset);
				pathStr += " L " + sp +"\n";
			}
			var ep = d.end.pos();
			pathStr += " L " + [ep[0]+COMPONENT_PADDING +d.end.originComponent.netChannelPadding.left, ep[1]]+"\n";
			return pathStr;
		});
	})();
};

function redraw(nodes, links){ //main function for rendering components layout
	var wrapper = d3.select("#chartWraper");
	
	wrapper.selectAll("svg").remove(); // delete old on redraw
	
	
	

	var svg = wrapper.append("svg");
	var svgGroup= svg.append("g"); // because of zooming/moving

	addShadows(svg);

	 
	var componentWrap = (function drawComponents(svgGroup,nodes){
	//alias component body
	var componentWrap = svgGroup.selectAll("g")
		.data(nodes)
		.enter()
		.append("g")
	    .classed({"component": true});

	// background
	componentWrap.append("rect")
	    .attr("rx", 5) // this make rounded corners
	    .attr("ry", 5)
	    .classed({"component": true})
	    .attr("border", 1)
	    .style("stroke", "#BDBDBD")
	    .attr("fill", "url(#gradient)")
	    .style("filter", "url(#drop-shadow)")
	    .attr("width", function(d) { return d.width})
	    .attr("height", function(d) { return d.height});
	
	componentWrap.append('text')
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
	var port_inputs = componentWrap.append("g")
		.attr("transform", function(d) { 
			return "translate(" + 0 + "," + 2*PORT_HEIGHT + ")"; 
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
			return (i-0.5)*PORT_HEIGHT;
		})
		.attr("width", 10)
		.attr("height", PORT_HEIGHT);
	
	// portName text [TODO] intelligent alignment of port name
	port_inputs.append('text')
		.attr("x", 10)
		.attr("y", function(d, i){
			return (i+0.3)*PORT_HEIGHT;
		})
		.attr("height", PORT_HEIGHT)
		.text(function(port) { 
			return port.name; 
		});
	
	// output port wraps
	var port_out = componentWrap.append("g")
		.attr("transform", function(d) { 
			var componentWidth = d3.select(this).node().parentNode.getBoundingClientRect().width;
			return "translate(" + componentWidth + "," + 2*PORT_HEIGHT + ")"; 
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
			return (i-0.5)*PORT_HEIGHT;
		})
		.attr("width", 10)
		.attr("height", PORT_HEIGHT);	

	// portName text
	port_out.append('text') 
		.attr("x", -10)	// posunuty okrej o 10 dolava
		.attr("y", function(d, i){
			return (i+0.3)*PORT_HEIGHT; //Zuzana: neviem ci je spravne manualne posunutie prvku ale vyzera to dobre, zalezi aj od velkosti fontu
		})
		.attr("height", PORT_HEIGHT)
		.text(function(port) { 
			return port.name; 
		});

		return componentWrap
	})(svgGroup, nodes);
	//grid higlight
    var linkElements = svgGroup.selectAll(".link")
    	.data(links)
    	.enter()
    	.append("path")
    	.classed({"link": true})
    	.on("mouseover", netMouseOver)
    	.on("mouseout", netMouseOut);
	
    updateLayout(svgGroup, componentWrap, linkElements, nodes, links);
    
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

	componentWrap.call(force.drag); //component dragging

    // define the zoomListener which calls the zoom function on the "zoom" event constrained within the scaleExtents
    var zoomListener = d3.behavior.zoom()
    	.scaleExtent([0.1, 3])
    	.on("zoom", function () {
    			svgGroup.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    	});
    function diagramSize(){
    	var widthMax =0;
    	var heigthtMax = 0;
    	nodes.forEach(function (n){
    		widthMax = Math.max(n.x +n.width + COMPONENT_PADDING, widthMax);
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
    
    svg.call(zoomListener);
 
}