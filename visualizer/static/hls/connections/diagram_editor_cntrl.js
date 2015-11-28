function diagramEditorCntrl($scope){
	var api = $scope.$parent.api;
	$scope.editedObject = {}
	$scope.newObject = {
		"name" : "",
		// "id": null,
		// "type" : null,
		"inputs" : [],
		"outputs" : []
	}
	$scope.portarrays = [];

	$scope.componentEditDetail = function() {
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
		// $scope.redraw();
	}

	$scope.componentAddPort = function(object, group) {
		console.log("ComponentEditAddPort")
		console.log(group, object)
		var portGroup = (group == 'Inputs' ? object.inputs : object.outputs)

		portGroup.unshift({
			"name" : ""
		});
		// componentEdit redraw
		// $scope.redraw();
	}

	$scope.componentEditSubmit = function() {
		$scope.redraw();
		console.log("Submit")
		console.log($scope.editedObject.inputs)
		// d3.selectAll("#componentEdit").style("display", "none");
	}

	$scope.componentEditCancel = function() {
		console.log("Cancel")
		d3.selectAll("#componentEdit").style("display", "none");
	}

	$scope.objectDelete = function() {
		// All selected objects
		var objects = d3.selectAll(".selected-object")[0];
		var links = d3.selectAll(".selected-link")[0];
		// console.log("Selected objects", objects);
		console.log("Selected links", links.length, links);
		for (i = 0; i < objects.length; i++) {
			var obj = objects[i].__data__;
			// console.log(obj)
			// console.log("Nodes: ", $scope.nodes)
			// console.log("Nets: ", $scope.nets)
			// console.log("Object check")
			// For all nodes in scope
			for (var i = 0; i < $scope.nodes.length; i++) {
				// console.log($scope.nodes[i].name)
				// Delete matching objects
				if ($scope.nodes[i].name == obj.name) {
					$scope.nodes.splice(i, 1);
				}
			}
			// console.log("Nets", obj.id)
			// For all nets in scope
			for (var j = 0; j < $scope.nets.length; j++) {
				// For all links
				var net = $scope.nets[j];
				for (var l = 0; l < net.targets.length; l++) {
					// Delete all links from deleted object
					var target = net.targets[l];
					if ((target.id == obj.id) | (net.source.id == obj.id)) {
						// console.log("Net: ", target, net.source)
						var removed = $scope.nets.splice(j, 1);
						j--;
						break;
					}
				}// for net targets
			}// for scope nets
		}// for selected objects

		// console.log("Link check")
		// For all selected links
		for (var m = 0; m < links.length; m++) {
			var net = links[m].__data__.net;
			var index = $scope.nets.indexOf(net);
			// Delete all selected links
			if (index > -1) {
				$scope.nets.splice(index, 1);
			}
		}
		// console.log($scope.nets)
		$scope.redraw();
		return;
	}

	$scope.componentAdd = function() {
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
		console.log("Before: ", $scope.nodes)
		$scope.nodes.push($scope.newObject);
		console.log("After: ", $scope.nodes)

		$scope.redraw();

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

	$scope.portClick = function(d) {
		// console.log("portClick data", d);
		switch ($scope.linkstatus) {
		case "none":
			// console.log("Setting origin")
			$scope.origin.port = d;
			$scope.linkstatus = "origincomp";
			break;
		case "destination":
			// console.log("Setting destination")
			$scope.destination.port = d;
			$scope.linkstatus = "destinationcomp";
			break;
		}
		// console.log("Link status", $scope.linkstatus)
		// console.log("Origin", $scope.origin)
		// console.log("Destination", $scope.destiantion)
	}

	$scope.compClick = function(d) {
		// console.log("Component Click data", d);
		switch ($scope.linkstatus) {
		case "origincomp":
			// console.log("Setting origin component")
			$scope.origin.component = d;
			$scope.linkstatus = "destination";
			break;
		case "destinationcomp":
			// console.log("Setting destination component")
			$scope.destination.component = d;
			$scope.linkstatus = "link";
			break;
		default:
			// console.log("Breaking")
			break;
		}

		// console.log("Link status", $scope.linkstatus)
		// console.log("Origin", $scope.origin)
		// console.log("Destination", $scope.destiantion)

		if ($scope.linkstatus == "link") {
			console.log("Linking");
			$scope.resetLinkingState();
		}

	}

	$scope.resetLinkingState = function() {
		$scope.linkstatus = "none";
	}
}