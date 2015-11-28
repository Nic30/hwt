

// create debug dots for routing nodes
function debugRouterDots(svgGroup, grid){
	var toolTipDiv = d3.select("body")
	.append("div")   
    .attr("id", "tooltip")               
    .style("opacity", 0);
	
	var flatenMap = [];
	grid.visitFromLeftTop(function(c){
		flatenMap.push(c);
	});

	var debugLinks = svgGroup.selectAll(".debug-link2component");
	// line to parent componet
	debugLinks
		.data(flatenMap)
		.enter()
		.append("path")
		.classed({"debug-link2component": true})
		.attr("d", function (d) {
			var sx = d.pos()[0];
			var sy = d.pos()[1];
			var tx = d.originComponent.x;
			var ty = d.originComponent.y ;
			return "M" + sx + "," + sy + " L " + tx + "," + ty;
		});
	
	//line connected nodes
	function forEveryDirection(fn){
		var directions = ["top", "bottom", "left", "right"];
		for(var i =0; i<  directions.length; i++ ){
			var direction = directions[i];
			fn(direction);
		}
	}
	var interNodeLines = [];
	flatenMap.forEach(function(d){
		forEveryDirection(function(direction){
			if(d[direction]){
				var p0 = d.pos()
				var p1 = d[direction].pos();
				interNodeLines.push({"p0": p0, "p1": p1});
			}
		})
	})
	
	//inter nodes connections
	var linkBetweenNodes =	svgGroup.selectAll(".debug-link-between-nodes")
		.data(interNodeLines)
		.enter()
		.append("path")
		.classed({	"debug-link-between-nodes" : true	})
		.attr("d", function(d) {	
			return "M" + d.p0[0] + "," + d.p0[1] + " L " + d.p1[0] + "," + d.p1[1];
		});
	
	var arrows = [];
	flatenMap.forEach(function(d){
		forEveryDirection(function(direction){
			var angle;
			switch(direction){ 
			case "top":
				angle = -90;
				break;
			case "bottom":
				angle = 90;
				break;
			case "left":
				angle = 180;
				break;
			case "right":
				angle = 0;
				break;
			}
			arrows.push({"routingNode":d, "angle" : angle});
		})
	});
	svgGroup.selectAll(".debug-routing-arrow")
		.data(arrows)
		.enter()
		.append("svg:g")
		.classed({"debug-routing-arrow": true})
		.attr("transform", function(d) { 
			return "translate(" + d.routingNode.pos() + ") " + "rotate("+ d.angle + ")"; 
		})
		.append("svg:path")
		.attr("d", "M1,-3 L6,0 L1,3");
    

	var routingNodes = svgGroup.selectAll(".debug-routing-node")
		.data(flatenMap)
		.enter()
		.append("circle")
		.classed({"debug-routing-node":true})
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
}   
