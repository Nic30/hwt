function onCompClick(d){
		var scope = angular.element(document.getElementsByTagName('body')[0]).scope();
		scope.api.compClick(d);	
		d3.event.stopPropagation();
		if (!d3.event.shiftKey) {
			removeSelections();
		}

		d3.select(this).classed({
			"selected-object" : true
		})
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

//Sets quick link creation state to none
function resetLinks()
{
	var scope = angular.element(document.getElementsByTagName('body')[0]).scope();
	scope.api.resetLinkingState();	
}

function onBoardClick() 
{
	console.log("boardclick")
	var exists = !d3.selectAll(".clicked-port").empty()
	var coordinates = d3.mouse(this);
	var x = coordinates[0];
	var y = coordinates[1];
	if (exists) {
		console.log(x,y)
	}
	removeSelections()
	resetLinks();
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
	d3.selectAll(".clicked-port").classed({
		"clicked-port" : false
	});
}

function removePortClicked()
{
	d3.selectAll(".selected-link").classed({
		"selected-link" : false
	});
}

function drawLink()
{
	var exists = !d3.selectAll(".clicked-port").empty()
	var object = d3.selectAll(".clicked-port")[0]
	var coordinates = d3.mouse(this);
	var x = coordinates[0];
	var y = coordinates[1];
	if (exists) {
		//console.log("")
	}
}
function onPortClick(d){
	var scope = angular.element(document.getElementsByTagName('body')[0]).scope();
	scope.api.portClick(d, this);	
}

function exPortDetail()
{
	console.log("ExPort Detail")
}