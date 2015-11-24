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

var App = angular.module('App', [ 'agGrid' ]);
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
				return $http.post("/customer/data/autocomplete", data, {
					headers : {
						'Content-Type' : 'application/json'
					}
				}).then(function(response) {
					return response;
				});
			};

			// $scope.fileDialog()
			$scope.open()
			      .then($scope.redraw);
			// drawMenu();
		}).config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{$');
	$interpolateProvider.endSymbol('$}');
});
;