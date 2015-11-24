var App = angular.module('App', [ 'agGrid' ]);

App
		.controller(
				'diagramController',
				function($scope, $http) {
					$scope.sidebarCollapsed = true
					$scope.collapseSidebar = function($event) {
						//console.log($event.target.className)
						if($scope.sidebarCollapsed == true)
							{
							$scope.sidebarCollapsed = false;
							}
						else{
							$scope.sidebarCollapsed = true;
						}
					}

					$scope.redraw = function() {
						$http
								.get(
										'/hls/connections-data/'
												+ $scope.selectedFile)
								.then(
										function(res) {
											var nets = res.data.nets;
											var nodes = res.data.nodes;
											COLUMN_WIDTH = findColumnWidth(nodes);
											checkDataConsistency(nodes, nets);
											
											var links = generateLinks(nets);
											resolveNodesInLinks(nodes, links);
											components2columns(nodes, links);
											ComponentDiagram("#chartWrapper",
													nodes, links);
										});
					}

					function rowClicked(params) {
						var node = params.node;
						var path = node.data.name;
						while (node.parent) {
							node = node.parent;
							path = node.data.name + '/' + path;
						}
						if(node.group){
							if(!node.expanded){
								node.children = [];
								return;
							}
							$scope.loadFolderData(path);
						}else{
							$scope.selectedFile = path;
							d3.selectAll("#fileDialog").style({
							"display" : "none"
							});
							$scope.redraw();	
						}
						
					}

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
						var imageFullUrl = "/static/hls/connections/" + image
								+ '.png';
						return '<img src="' + imageFullUrl
								+ '" style="padding-left: 4px;" /> '
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

					$scope.loadFolderData  = function(path){
						$http.get('/hls/connections-data-ls/' + path)
								.then(
										function(res) {
											function findDir(path) {
												if(path == "")
													return filesRowData
												 
												var dir = filesRowData.filter(function(f){
													return f.data.name == path;
												})[0] 

												return dir;
											}
											var files = res.data;
											var dir = findDir(path);
											if (dir.child === undefined) {
												
													filesRowData = files;
												
											} else {
												dir.children = files;
											}

											$scope.fileGridOptions.api
													.setRowData(filesRowData);
										});
					}
					
					$scope.selectedFile = 'example1.json';
					$scope.fileDialog = function() {
						d3.selectAll("#chartWrapper").html("");
						d3.selectAll("#fileDialog").style({
							"display" : "block"
						});
						filesRowData = [];
						$scope.loadFolderData("");
					}
					 //$scope.fileDialog()
					 $scope.redraw()
					 //drawMenu();
				}).config(function($interpolateProvider) {
			$interpolateProvider.startSymbol('{$');
			$interpolateProvider.endSymbol('$}');
		});
;