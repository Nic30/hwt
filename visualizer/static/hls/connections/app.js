var App = angular.module('App', [ 'agGrid', 'cfp.hotkeys', 'ngAnimate', 'toastr']);
App.controller('mainController', function($scope, $http, toastr) {
	$scope.api = {
		nodes : [],
		nets : [],
		msg:toastr
	};
	//$scope.api.open()
	//$scope.open()
	//      .then($scope.redraw);
})
.controller('diagramCntrl', diagramCntrl)
.controller('filebrowserCntrl', filebrowserCntrl)
.controller('menuCntrl', menuCntrl)
.controller('diagramEditorCntrl', diagramEditorCntrl)
.config(function(toastrConfig) {
  angular.extend(toastrConfig, {
    templates: {
      toast: '/static/bower_components/angular-toastr/src/directives/toast/toast.html',
      progressbar: '/static/bower_components/angular-toastr/src/directives/progressbar/progressbar.html'
    },
    timeOut: 4000,
  });
})
.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{$');
	$interpolateProvider.endSymbol('$}');
});
