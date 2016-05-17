function menuCntrl($scope){
	var api = $scope.$parent.api;
	api.sidebarCollapsed = true
	api.collapseSidebar = function($event) {
		if (api.sidebarCollapsed == true) {
			api.sidebarCollapsed = false;
		} else {
			api.sidebarCollapsed = true;
		}
	}
	api.newDiagram = function() {
		api.nodes = [];
		api.nets = [];
		api.redraw();
	}
}