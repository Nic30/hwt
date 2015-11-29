var App = angular.module('App', [ 'agGrid', 'cfp.hotkeys', 'ngAnimate', 'toastr']);
App.config(function(toastrConfig) {
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
.directive('includeReplace', function () {
    return {
        require: 'ngInclude',
        restrict: 'A', /* optional */
        link: function (scope, el, attrs) {
            el.replaceWith(el.children());
        }
    };
});;
