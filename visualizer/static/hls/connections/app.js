var App = angular.module('App', [ 'ngCookies', 'agGrid', 'cfp.hotkeys', 'ngAnimate', 'toastr']);
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
 
App.controller('mainController', function($scope, $http, toastr, $cookies,$cookieStore) {
	$scope.api = {
		nodes : [],
		nets : [],
		msg:toastr,
		unimplemented: function(msg){
			$scope.api.msg.error("Unimplemented",msg);
		}
	};
	//$scope.api.open()
	//$scope.open()
	//      .then($scope.redraw);
})
.controller('diagramCntrl', diagramCntrl)
.controller('filebrowserCntrl', filebrowserCntrl)
.controller('menuCntrl', menuCntrl)
.controller('diagramEditorCntrl', diagramEditorCntrl)
.controller('cookieManagerCntrl', cookieManagerCntrl)
.directive('includeReplace', function () {
    return {
        require: 'ngInclude',
        link: function (scope, el, attrs) {
            el.replaceWith(el.children());
        }
    };
});;
