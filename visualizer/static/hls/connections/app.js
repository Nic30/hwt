var App = angular.module('App', [ 'agGrid', 'cfp.hotkeys']);
App.controller('mainController', function($scope, $http) {
	$scope.api = {
		nodes : [],
		nets : []
	};

	/********************************
	**                              *-
	**        MENU ACTIONS          *
	**                              *
	********************************/
	
	// $scope.fileDialog()
	//$scope.open()
	//      .then($scope.redraw);
})
.controller('diagramCntrl', diagramCntrl)
.controller('filebrowserCntrl', filebrowserCntrl)
.controller('menuCntrl', menuCntrl)
.controller('diagramEditorCntrl', diagramEditorCntrl)
.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{$');
	$interpolateProvider.endSymbol('$}');
});
