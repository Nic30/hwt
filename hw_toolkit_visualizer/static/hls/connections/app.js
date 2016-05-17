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
})
.controller('diagramCntrl', diagramCntrl)
.controller('filebrowserCntrl', filebrowserCntrl)
.controller('menuCntrl', menuCntrl)
.controller('diagramEditorCntrl', diagramEditorCntrl)
.controller('cookieManagerCntrl', cookieManagerCntrl)
.controller('undoRedoCntrl', undoRedoCntrl)
.directive('includeReplace', function () {
    return {
        require: 'ngInclude',
        link: function (scope, el, attrs) {
            el.replaceWith(el.children());
        }
    };
}).config(function(hotkeysProvider) {
    hotkeysProvider.template = '<div class="cfp-hotkeys-container fade" ng-class="{in: helpVisible}" style="display: none;"><div class="cfp-hotkeys">' +
    '<h4 class="cfp-hotkeys-title" ng-if="!header">{$ title $}</h4>' +
    '<div ng-bind-html="header" ng-if="header"></div>' +
    '<table><tbody>' +
      '<tr ng-repeat="hotkey in hotkeys | filter:{ description: \'!$$undefined$$\' }">' +
        '<td class="cfp-hotkeys-keys">' +
          '<span ng-repeat="key in hotkey.format() track by $index" class="cfp-hotkeys-key">{$ key $}</span>' +
        '</td>' +
        '<td class="cfp-hotkeys-text">{$ hotkey.description $}</td>' +
      '</tr>' +
    '</tbody></table>' +
    '<div ng-bind-html="footer" ng-if="footer"></div>' +
    '<div class="cfp-hotkeys-close" ng-click="toggleCheatSheet()">×</div>' +
    '</div></div>';
});
