function componentOnClick() {
	// var selectedObject = console.log(d3.select(this)[0][0].__data__)

	d3.event.stopPropagation();
	if (!d3.event.shiftKey) {
		removeSelections();
	}

	d3.select(this).classed({
		"selected-object" : true
	})
	// d3.select(this).style("stroke", "red");
}

function exPortOnClick() {

	d3.event.stopPropagation();
	if (!d3.event.shiftKey) {
		removeSelections();
	}

	d3.select(this).classed({
		"selected-port" : true
	})
}

function netOnClick() {
	d3.event.stopPropagation();
	if (!d3.event.shiftKey) {
		removeSelections();
	}

	d3.select(this).classed({
		"selected-link" : true
	})
}

function onBoardClick() 
{
	removeSelections()
	var exists = !d3.selectAll(".clicked-port").empty()
	if (exists) {
		//makePort
	}
}

function removeSelections() {
	d3.selectAll(".selected-port").classed({
		"selected-port" : false
	});
	d3.selectAll(".selected-object").classed({
		"selected-object" : false
	});
	d3.selectAll(".selected-link").classed({
		"selected-link" : false
	});
}

function removePortClicked()
{
	d3.selectAll(".selected-link").classed({
		"selected-link" : false
	});
}

function portOnClick() {
	removeSelections();

	d3.event.stopPropagation();
	console.log("port Click");
	d3.select(this).classed({
		"clicked-port" : true
	})
}

function drawLink()
{
	var exists = !d3.selectAll(".clicked-port").empty()
	var object = d3.selectAll(".clicked-port")[0]
	var coordinates = d3.mouse(this);
	var x = coordinates[0];
	var y = coordinates[1];
	if (exists) {
		console.log("")
	}
}

function componentDetail()
{
	console.log("Component Detail")
	var selection = d3.selectAll(".selected-object")
	var count = selection[0].length
	if (count == 0)
	{
		console.log("No object selected!")
	}
	else if (count > 1)
	{
		console.log("Too many objects selected!")
	}
	else
	{
		console.log(selection[0][0])
		var object = selection[0][0]
		var selected = object.getElementsByTagName("g");
		console.log(object.__data__)
	}

}

function exPortDetail()
{
	console.log("ExPort Detail")
}