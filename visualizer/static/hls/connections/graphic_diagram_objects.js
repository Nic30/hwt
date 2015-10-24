function drawExternalPorts(svgGroup, exterPortNodes){
	var externalPorts = svgGroup.selectAll(".external-port")
		.data(exterPortNodes)
		.enter()
		.append("g")
		.classed({"external-port" :true});
	
	externalPorts.append("text")
		.attr("x", function(d) {
			return (d.inputs.length == 0)?-10:-44;
		})
		.attr("y", function(d) {
			return (d.inputs.length == 0)?4:27;
		})
		.text(function(d) {
			return d.name;
		})
	
	
	externalPorts.append("image")
		.attr("xlink:href", function(d) { 
			return "/static/hls/connections/arrow_right.ico"; 
		})
		.attr("x", function(d) {
			return (d.inputs.length == 0)?-10:-78;
		})
		.attr("y", function(d) {
			return (d.inputs.length == 0)?-5:19;
		})
		.attr("width", 10)
		.attr("height", PORT_HEIGHT);

	externalPorts.attr("transform", function(d) { 
		return "translate(" + (d.x + d.width) + "," + (d.y + d.height/2) + ")"; 
	})
	
	return externalPorts;
}


function drawComponents(svgGroup, componentNodes){
	//alias component body
	var componentWrap = svgGroup.selectAll(".component")
		.data(componentNodes)
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
		});

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

	componentWrap.attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
    });
	
	return componentWrap;
}