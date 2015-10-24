var App = angular.module('App', []);
/* [TODO] Michal: left top corner routing node is not moved away of nets as the others,
                this causes invalid mess in left top corner instead of nets (usually happens on the sides of diagram)
 [TODO] Michal: in super dma complex axi_regs_with_def_value have not connected outputs (probably bad channel width)
 [TODO] Michal: due net spacing dome of the connected nodes are no more aligned to each other, this causes non horizontal/vertical lines
 [TODO] Marek: external port style
 [TODO] find way how to allow temporary disable zoom/moving to allow copy of the text
 [TODO] net mouse over style
 [TODO] toolbar
 [TODO] select, multi-select
 [TODO] component dialog
 [TODO] add/delete component
 [TODO] add/delete connection
 [TODO] construct external port (shortcut)
 
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

					var links = generateLinks(nets);
					resolveNodesInLinks(nodes, links);
					components2columns(nodes, links);
					redraw(nodes, links);
				});
	}
	$scope.redraw()
});