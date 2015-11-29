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