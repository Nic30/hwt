function diagramEditorCntrl($scope){
	var api = $scope.$parent.api;
	api.editedObject = {}
	$scope.newObject = {
		"name" : "",
		// "id": null,
		// "type" : null,
		"inputs" : [],
		"outputs" : []
	}
	$scope.portarrays = [];

	api.componentEditDetail = function() {
		// console.log("Component Detail")
		var selection = d3.selectAll(".selected-object");
		var count = selection[0].length
		if (count == 0) {
			console.log("No object selected!")
		} else if (count > 1) {
			console.log("Too many objects selected!")
		} else {
			d3.selectAll("#componentEdit").style("display", "block");

			// console.log(selection[0][0])
			var object = selection[0][0]
			var selected = object.getElementsByTagName("g");
			// console.log(object.__data__)
			$scope.editedObject = object.__data__;
			$scope.portarrays = [ {
				'array' : $scope.editedObject.inputs,
				'name' : 'Inputs'
			}, {
				'array' : $scope.editedObject.outputs,
				'name' : 'Outputs'
			} ]
		}

	}

	$scope.componentRemovePort = function(object, group, port) {
		console.log("ComponentEditRemovePort")
		// console.log(object, group, port);
		var portGroup = (group == 'Inputs' ? object.inputs : object.outputs)
		// console.log(portGroup, port);
		var index = portGroup.indexOf(port);
		if (index > -1) {
			portGroup.splice(index, 1);
		} else {
			console.log("Remove port error: port does not exist")
		}
		// componentEdit redraw
		// api.redraw();
	}

	$scope.componentAddPort = function(object, group) {
		console.log("ComponentEditAddPort")
		console.log(group, object)
		var portGroup = (group == 'Inputs' ? object.inputs : object.outputs)

		portGroup.unshift({
			"name" : ""
		});
		// componentEdit redraw
		// api.redraw();
	}

	$scope.componentEditSubmit = function() {
		api.redraw();
		console.log("Submit")
		console.log($scope.editedObject.inputs)
		// d3.selectAll("#componentEdit").style("display", "none");
	}

	$scope.componentEditCancel = function() {
		console.log("Cancel")
		d3.selectAll("#componentEdit").style("display", "none");
	}

	api.objectDelete = function() {
		// All selected objects
		var objects = d3.selectAll(".selected-object")[0];
		var links = d3.selectAll(".selected-link")[0];
		//console.log("Selected objects", objects);
		//console.log("Selected links", links.length, links);
		for (i = 0; i < objects.length; i++) {
			var obj = objects[i].__data__;
			// console.log(obj)
			// console.log("Nodes: ", api.nodes)
			// console.log("Nets: ", api.nets)
			// console.log("Object check")
			// For all nodes in scope
			for (var i = 0; i < api.nodes.length; i++) {
				// console.log(api.nodes[i].name)
				// Delete matching objects
				if (api.nodes[i].name == obj.name) {
					api.nodes.splice(i, 1);
				}
			}
			//console.log("Nets", obj.id)
			// For all nets in scope
			for (var j = 0; j < api.nets.length; j++) {
				// For all links
				var net = api.nets[j];
				for (var l = 0; l < net.targets.length; l++) {
					// Delete all links from deleted object
					var target = net.targets[l];
					if ((target.id == obj.id) | (net.source.id == obj.id)) {
						// console.log("Net: ", target, net.source)
						var removed = api.nets.splice(j, 1);
						j--;
						break;
					}
				}// for net targets
			}// for scope nets
		}// for selected objects

		//console.log("Link check")
		// For all selected links
		for (var m = 0; m < links.length; m++) {
			var net = links[m].__data__.net;
			var index = api.nets.indexOf(net);
			// Delete all selected links
			if (index > -1) {
				api.nets.splice(index, 1);
			}
		}
		// console.log(api.nets)
		api.redraw();
		return;
	}

	api.componentAdd = function() {
		d3.selectAll("#componentAdd").style("display", "block");
		$scope.newObject = {
			"name" : "",
			// "id": null,
			// "type" : null,
			"inputs" : [],
			"outputs" : []
		}
		$scope.portarrays = [ {
			'array' : $scope.newObject.inputs,
			'name' : 'Inputs'
		}, {
			'array' : $scope.newObject.outputs,
			'name' : 'Outputs'
		} ]
	}

	$scope.componentAddSubmit = function() {
		console.log("Submit")
		console.log("Before: ", api.nodes)
		api.nodes.push($scope.newObject);
		console.log("After: ", api.nodes)

		api.redraw();

		// d3.selectAll("#componentAdd").style("display", "none");
	}

	$scope.componentAddCancel = function() {
		console.log("Cancel")
		d3.selectAll("#componentAdd").style("display", "none");
	}

	$scope.origin = {
		"component" : {},
		"port" : {}
	};
	$scope.destination = {
		"component" : {},
		"port" : {}
	};
	$scope.linkstatus = "none";
	
	function drawDashedLine2port(event){
		var coordinates = d3.mouse(this);
		var x = coordinates[0];
		var y = coordinates[1];
		console.log(x,y);
	}
	
	api.portClick = function(d) {
		//console.log("portClick data", d);
		//console.log("Link status", $scope.linkstatus)
		switch ($scope.linkstatus) {
		case "none":
			//console.log("Setting origin")
			$scope.origin.port = d;
			$scope.linkstatus = "origincomp";
			break;
		case "destination":
			//console.log("Setting destination")
			$scope.destination.port = d;
			$scope.linkstatus = "destinationcomp";
			break;
		}
		//console.log("Link status", $scope.linkstatus)
		//console.log("Origin", $scope.origin)
		//console.log("Destination", $scope.destination)
	}

	api.compClick = function(d) {
		//console.log("Component Click data", d);
		//console.log("Link status", $scope.linkstatus)
		switch ($scope.linkstatus) {
		case "origincomp":
			//console.log("Setting origin component")
			$scope.origin.component = d;
			$scope.linkstatus = "destination";
			api.onMouseroverDiagram = drawDashedLine2port;
			break;
		case "destinationcomp":
			//console.log("Setting destination component")
			$scope.destination.component = d;
			$scope.linkstatus = "link";
			break;
		default:
			// console.log("Breaking")
			break;
		}

		//console.log("Link status", $scope.linkstatus)
		//console.log("Origin", $scope.origin)
		//console.log("Destination", $scope.destination)
		
		if ($scope.linkstatus == "link") {
			//console.log("Linking");
			var originport = $scope.getPortIndexByName($scope.origin.port.name, $scope.origin.component)
			var destinationport = $scope.getPortIndexByName($scope.destination.port.name, $scope.destination.component)
			//console.log("Origin portindex", originport)
			//console.log("Destination portindex", destinationport)			
			if (originport[1] == "inputs")
			{
				var net = {
						"targets": [
						           {
						        	   "portIndex": originport[0],
						        	   "id": $scope.origin.component.id
						           }
						],
						"source": {
							"portIndex": destinationport[0],
				        	 "id": $scope.destination.component.id
						}
				}
			}// if originport inputs
			else if (originport[1] == "outputs")
			{
				var net = {
						"targets": [
						           {
						        	   "portIndex": destinationport[0],
							        	"id": $scope.destination.component.id
						           }
						],
						"source": {
							"portIndex": originport[0],
				        	   "id": $scope.origin.component.id
						}
				}
			}
			else
			{
				var net = ""
				console.log("Quicklink: Cant construct link, port name corrupted")
			}
			//console.log("Net to be added: ", net)
			api.nets.push(net);
			api.redraw();
			api.resetLinkingState();
		}// if scopestatus link

	}

	$scope.getPortIndexByName = function (name, component)
	{
		for (var i = 0; i < component.inputs.length;i++)
		{
			if (name == component.inputs[i].name)
			{
				//console.log("Match input", name, component.inputs[i].name)
				return [i, "inputs"];
			}
		}
		
		for (var j = 0; j < component.outputs.length;j++)
		{
			if (name == component.outputs[j].name)
			{
				//console.log("Match output", name, component.outputs[i].name)
				return [j, "outputs"];
			}
		}
		return [null, null];
	}
	
	api.resetLinkingState = function() {
		$scope.linkstatus = "none";
	}
}