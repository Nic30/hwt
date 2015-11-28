function sizeCellStyle() {
	return {
		'text-align' : 'right'
	};
}

function innerCellRenderer(params) {
	var image;
	if (params.node.group) {
		image = 'folder';
	} else {
		image = 'file';
	}
	var imageFullUrl = "/static/hls/connections/graphic/" + image + '.png';
	return '<img src="' + imageFullUrl + '" style="padding-left: 4px;" /> '
			+ params.data.name;
}

var columnDefs = [ {
	headerName : "Name",
	field : "name",
	width : 350,
	cellRenderer : {
		renderer : 'group',
		innerRenderer : innerCellRenderer
	}
}, {
	headerName : "Size",
	field : "size",
	width : 100,
	cellStyle : sizeCellStyle
}, {
	headerName : "Type",
	field : "type",
	width : 150
}, {
	headerName : "Date Modified",
	field : "dateModified",
	width : 200
} ];

var App = angular.module('App', [ 'agGrid', 'cfp.hotkeys']);
App.controller(
		'diagramController',
		function($scope, $http) {
			$scope.sidebarCollapsed = true
			$scope.collapseSidebar = function($event) {
				if ($scope.sidebarCollapsed == true) {
					$scope.sidebarCollapsed = false;
				} else {
					$scope.sidebarCollapsed = true;
				}
			}
			$scope.redraw = function() {
				var nodes = $scope.nodes;
				var nets = $scope.nets;

				COLUMN_WIDTH = findColumnWidth(nodes);
				checkDataConsistency(nodes, nets);
				
				var links = generateLinks(nets);
				resolveNodesInLinks(nodes, links);
				components2columns(nodes, links);
				ComponentDiagram("#chartWrapper", nodes, links);
			}

			$scope.open = function() {
				return $http.get('/hls/connections-data/' + $scope.openedFile)
					        .then(function(res) {
					            var nets = res.data.nets;
					            var nodes = res.data.nodes;
					            $scope.nodes = nodes;
					            $scope.nets = nets;
					        });
			}

			function rowClicked(params) {
				var node = params.node;
				var path = node.data.name;
				var tmpnode = node;
				while (tmpnode.parent) {
					var tmpnode = tmpnode.parent;
					path = tmpnode.data.name + '/' + path;
				}
				if (node.group) {
					if (!node.expanded) {
						node.children = [];
						return;
					}
					$scope.loadFolderData(path);
				} else {
					$scope.openedFile = path;
					d3.selectAll("#fileDialog").style({
						"display" : "none"
					});
					$scope.redraw();
				}

			}

			$scope.rootDir = "";
			var filesRowData = [];

			$scope.fileGridOptions = {
				columnDefs : columnDefs,
				rowData : filesRowData,
				rowSelection : 'multiple',
				rowsAlreadyGrouped : true,
				enableColResize : true,
				enableSorting : true,
				rowHeight : 20,
				icons : {
					groupExpanded : '<i class="fa fa-minus-square-o"/>',
					groupContracted : '<i class="fa fa-plus-square-o"/>'
				},
				onRowClicked : rowClicked
			};

			$scope.loadFolderData = function(path) {
				$http.get('/hls/connections-data-ls/' + path)
						.then(
								function(res) {
									function findDir(path) {
										if (path == "")
											return filesRowData

										var dir = filesRowData.filter(function(
												f) {
											return f.data.name == path;
										})[0]

										return dir;
									}
									var files = res.data;
									var dir = findDir(path);
									if (dir.children === undefined) {

										filesRowData = files;

									} else {
										dir.children = files;
									}

									$scope.fileGridOptions.api
											.setRowData(filesRowData);
								});
			}

			$scope.openedFile = 'example1.json';
			$scope.fileDialog = function() {
				d3.selectAll("#chartWrapper").html("");
				d3.selectAll("#fileDialog").style({
					"display" : "block"
				});
				filesRowData = [];
				$scope.loadFolderData("");
			}

			$scope.save = function(path) {
				var data = {
					"path" : path,
					"nodes" : $scope.nodes,
					"nets" : $scope.nets
				};
				return $http.post("/hls/connections-save", data, {
					headers : {
						'Content-Type' : 'application/json'
					}
				}).then(function(response) {
					return response;
				});
			};
			$scope.editedObject = {}
			$scope.newObject = {
					"name": "",
					//"id": null,
					//"type" : null,
					"inputs": [],
					"outputs": []
			}
			$scope.portarrays = []
			
			$scope.componentEditDetail = function ()
			{
				//console.log("Component Detail")
				var selection = d3.selectAll(".selected-object");
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
					d3.selectAll("#componentEdit").style("display" , "block");
					
					//console.log(selection[0][0])
					var object = selection[0][0]
					var selected = object.getElementsByTagName("g");
					//console.log(object.__data__)
					$scope.editedObject = object.__data__;
					$scope.portarrays = [{'array': $scope.editedObject.inputs, 'name': 'Inputs'}, {'array': $scope.editedObject.outputs, 'name': 'Outputs'}]
				}

			}
		
			$scope.componentRemovePort = function(object, group, port)
			{
				console.log("ComponentEditRemovePort")
				console.log(object, group, port);
				var portGroup = (group == 'Inputs' ? object.inputs : object.outputs)
				//console.log(portGroup, port);
				var index = portGroup.indexOf(port);
				if(index > -1) {
					portGroup.splice(index, 1);
				}
				else
					{
					console.log("Remove port error: port does not exist")
					}
				//componentEdit redraw
				//$scope.redraw();
			}
			
			$scope.componentAddPort = function(object, group)
			{
				console.log("ComponentEditAddPort")
				console.log(group, object)
				var portGroup = (group == 'Inputs' ? object.inputs : object.outputs)
				
				portGroup.unshift({
                    "name": ""
					}
					);
				//componentEdit redraw
				//$scope.redraw();
			}
			
			$scope.componentEditSubmit = function ()
			{
				$scope.redraw();
				console.log("Submit")
				console.log($scope.editedObject.inputs)
				//d3.selectAll("#componentEdit").style("display", "none");
			}
			
			$scope.componentEditCancel = function ()
			{
				console.log("Cancel")
				d3.selectAll("#componentEdit").style("display", "none");
			}
			
			$scope.componentDelete = function()
			{
				var objects = d3.selectAll(".selected-object")[0];
				//console.log("Selected objects", objects);
				for (i = 0; i < objects.length; i++)
				{
					var obj = objects[i].__data__;
					console.log(obj)
					console.log("Nodes: ", $scope.nodes)
					console.log("Nets: ", $scope.nets)
					for(var i = 0; i < $scope.nodes.length;i++)
					{
						//console.log($scope.nodes[i].name)
						if ($scope.nodes[i].name == obj.name)
						{
							console.log("MATCH", i)
							$scope.nodes.splice(i, 1);	
						}
					}
					console.log("Nets", obj.id)
					for(var j = 0; j < $scope.nets.length; j++)
					{
						var net = $scope.nets[j];
						for (var l = 0; l < net.targets.length; l++)
						{
							var target = net.targets[l];
							if ((target.id == obj.id) | (net.source.id == obj.id))
							{
								console.log("Net: ", target, net.source)
								var removed = $scope.nets.splice(j, 1);
								j--;
								console.log("Removed: ", removed)
								break;
							}
						}
					}
				}
				console.log($scope.nets)
				$scope.redraw();
				return;
			}
			
			$scope.componentAdd = function()
			{
				d3.selectAll("#componentAdd").style("display" , "block");
				$scope.newObject = {
						"name": "",
						//"id": null,
						//"type" : null,
						"inputs": [],
						"outputs": []
				}
				$scope.portarrays = [{'array': $scope.newObject.inputs, 'name': 'Inputs'}, {'array': $scope.newObject.outputs, 'name': 'Outputs'}]
			}
			
			$scope.componentAddSubmit = function ()
			{
				console.log("Submit")
				console.log("Before: ",$scope.nodes)
				$scope.nodes.push($scope.newObject);
				console.log("After: ",$scope.nodes)
				
				$scope.redraw();
				
				
				//d3.selectAll("#componentAdd").style("display", "none");
			}
			
			$scope.componentAddCancel = function ()
			{
				console.log("Cancel")
				d3.selectAll("#componentAdd").style("display", "none");
			}
			
			// $scope.fileDialog()
			$scope.open()
			      .then($scope.redraw);
			// drawMenu();
		}).config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{$');
	$interpolateProvider.endSymbol('$}');
});
