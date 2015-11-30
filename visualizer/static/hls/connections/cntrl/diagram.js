function findColumnWidth(nodes) {
	var INTERNAL_SPACE = 20;
	var FONT_SIZE = 7;
	var maxNamesLen = 0;
	COLUMN_WIDTH =0;
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

			maxNamesLen = Math.max(maxNamesLen, nameBlen + nameSlen);
		});

	});
	return Math.max(FONT_SIZE * maxNamesLen + INTERNAL_SPACE, COLUMN_WIDTH);
}

function diagramCntrl($scope) {
	var api = $scope.$parent.api;
	var diagram = ComponentDiagram("#chartWrapper");
	api.fitDiagram2Screen = diagram.fit2Screen;
	api.redraw = function() {
		var nodes = api.nodes;
		var nets = api.nets;

		COLUMN_WIDTH = findColumnWidth(nodes);
		checkDataConsistency(nodes, nets);
		
		var links = generateLinks(nets);
		resolveNodesInLinks(nodes, links);
		components2columns(nodes, links);
		diagram.bindData(nodes, links)
		diagram.on('mousemove', function(){
			if(api.onMouseroverDiagram){
			    var mousePosition = d3.mouse(diagram.wrapper[0][0].parentElement)
				diagram.wrapper.call(api.onMouseroverDiagram, mousePosition);
			}
		});
		api.diagramSvg = diagram.svg;
	}
}