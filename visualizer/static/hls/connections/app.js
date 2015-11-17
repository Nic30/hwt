var App = angular.module('App', [ 'agGrid' ]);
/*
 * https://leanpub.com/D3-Tips-and-Tricks/read
 * http://www.d3noob.org/2013/03/d3js-force-directed-graph-examples.html
 * http://blog.pixelingene.com/demos/d3_tree/
 * http://bl.ocks.org/Neilos/584b9a5d44d5fe00f779
 * http://www.jointjs.com/tutorial/ports
 * http://gojs.net/latest/samples/dynamicPorts.html
 * http://bl.ocks.org/GerHobbelt/3104394 http://bl.ocks.org/mbostock/3681006
 * --zoom
 * http://www.codeproject.com/Articles/709340/Implementing-a-Flowchart-with-SVG-and-AngularJS
 * http://www.coppelia.io/2014/07/an-a-to-z-of-extra-features-for-the-d3-force-layout/
 * http://bl.ocks.org/explunit/5603250
 * http://www.ece.northwestern.edu/~haizhou/357/lec6.pdf
 * http://bl.ocks.org/lgersman/5310854 -- selection
 * http://ag-grid.com/example-file-browser/fileBrowser.html
 * 
 * [TODO][Michal] connection to next left boundary of component to allow router
 * make more straight line for long nets
 * 
 * [TODO][Zuzana] find way how to allow temporary disable zoom/moving to allow
 * copy of the text [TODO][Zuzana] javaskriptova funkce ktera snizi jas a
 * kontrast vsech objektu v svg (vse zasedne, a pak dalsi ukol bude pouzit to se
 * zvyraznovanim...)
 * 
 * [TODO][Zuzana] net mouse over style/ net(link) style (chce to i sjednotit
 * nazvoslovi, na net) soucasne spoje jsou moc tenke, neda se na ne najet myssi
 * po najeti stejne nic neni videt protoze ta cervena se strati
 * 
 * [TODO][Marek] toolbar, funkcionalita (open, a pod...)
 * 
 * [TODO][Marek] multi-select
 * 
 * [TODO][Marek] component edit dialog
 * 
 * 
 * [TODO][Marek] add/delete component (prozatim jen predpripraveny json, nebo
 * tak neco bude potreba integrace s filebrowserem)
 * 
 * [TODO][Marek] add/delete connection /construct external port (shortcut),
 * predstava je takova ze kdyz se klikne na sit tak se jakoby nalinkuje na
 * kurzor a kde se klikne tam se pripoji (i vickrat za sebou), zrusi se to pres
 * ESC a pri kliknuti a drzeni napr ctrl se misto pripojeni vytvori externi port
 * 
 * 
 * Prioritne: [Zuzana] filebrower : lazy load, slozky  
 * 
 * [Marek] postranni panel ze ktereho se bude
 * dat spustit filebrowser, smazat komponenta, pridat komponenta [Michal]
 * otevreni vybrane veci z filebrowser, predpracovat editace
 * 
 * Proc? Protoze nemuzeme pohodlne prepinat mezi diagramy, a tak to asi tezko
 * dobre otestujeme....
 * 
 */
App
		.controller(
				'diagramController',
				function($scope, $http) {
					
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
						$scope.selectedFile = path;
						d3.selectAll("#fileDialog").style({
							"display" : "none"
						});
						$scope.redraw();
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

					$scope.selectedFile = 'workspace/example1.json';
					$scope.fileDialog = function() {
						d3.selectAll("#fileDialog").style({
							"display" : "block"
						});
						$http.get('/hls/connections-data-ls/' + $scope.rootDir)
								.then(
										function(res) {
											function findDir(path) {
												return filesRowData;
											}
											var files = res.data;
											var dir = findDir($scope.rootDir);
											if (dir.childs === undefined) {
												files.forEach(function(f) {
													filesRowData.push(f);
												})
											} else {
												dir.childs = files;
											}

											$scope.fileGridOptions.api
													.setRowData(filesRowData);
										});
					}
					 $scope.fileDialog()
					 //$scope.redraw()
					 //drawMenu();
				}).config(function($interpolateProvider) {
			$interpolateProvider.startSymbol('{$');
			$interpolateProvider.endSymbol('$}');
		});
;