var App = angular.module('App', []);
/*
 * [TODO] Michal: left top corner routing node is not moved away of nets as the
 * others, this causes invalid mess in left top corner instead of nets (usually
 * happens on the sides of diagram) [TODO] Michal: in super dma complex
 * axi_regs_with_def_value have not connected outputs (probably bad channel
 * width) [TODO] Michal: due net spacing dome of the connected nodes are no more
 * aligned to each other, this causes non horizontal/vertical lines [TODO]
 * Marek: external port style [TODO] find way how to allow temporary disable
 * zoom/moving to allow copy of the text [TODO] net mouse over style [TODO]
 * toolbar [TODO] select, multi-select [TODO] component dialog [TODO] add/delete
 * component [TODO] add/delete connection [TODO] construct external port
 * (shortcut)
 * 
 */

App.controller('diagramController', function($scope, $http) {

	$scope.redraw = function() {
		$http.get('/hls/connections/data.json').then(
				function(res) {
					var nets = res.data.nets;
					var nodes = res.data.nodes;
					var INTERNAL_SPACE = 20;
					var FONT_SIZE = 7;
					var maxNamesLen = 0;
					nodes.forEach(function(n) {
						if (n.inputs.length > n.outputs.length) {
							var biggerArr = n.inputs;
							var smallerArr = n.outputs;
						} else {
							var biggerArr = n.outputs;
							var smallerArr = n.inputs;
						}
						biggerArr.forEach(function(p, i) {
							var nameBlen = p.name.length;
							var sp = smallerArr[i];

							var nameSlen = 0;
							if (sp)
								nameSlen = sp.name.length

							maxNamesLen = Math.max(maxNamesLen, nameBlen
									+ nameSlen);
						});

					});
					COLUMN_WIDTH = Math.max(FONT_SIZE * maxNamesLen
							+ INTERNAL_SPACE, COLUMN_WIDTH);

					function findComponent(id){
						var tmp =	nodes.filter(function (node){return node.id == id});
						if(tmp.length == 0)
							throw "component with id " + id + " is not in nodes";
						else if (tmp.lengt >1)
							throw "component with id " + id + " has multiple definitions";
						else
							return tmp[0];
					}
					function findPort(node, portIndex, isOutput){
						if(isOutput){
							var arr =  node.outputs;
						}else{
							var arr =  node.inputs;
						}
						var pi = arr[portIndex];
						if(! pi)
							throw "Component has not port with index:" + portIndex + "( isOutput:"+isOutput+" )"
						return pi;
					}
					function assertPortExists(portItem, isOutput){
						var c = findComponent(portItem.id);
						findPort(c, portItem.portIndex, isOutput);
					}
					
					nets.forEach(function (net){
						assertPortExists(net.source, true);
						net.targets.forEach(function(t){
							assertPortExists(t, false);
						})
					});
					
					var links = generateLinks(nets);
					resolveNodesInLinks(nodes, links);
					components2columns(nodes, links);
					redraw(nodes, links);
				});
	}
	$scope.redraw()
});