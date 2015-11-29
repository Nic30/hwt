function cookieManagerCntrl($scope, $cookies, $cookieStore) {
	var api = $scope.$parent.api;

	$scope.$watch(function() {
		return api.openedFile
	}, function(newValue) {
		$cookieStore.put('lastOpenedFile', newValue);
	});
	var lastOpened = $cookieStore.get('lastOpenedFile');
	if (lastOpened) {
		var unbindInitializer = $scope.$watch(function() {
			return api.open
		}, function() {
			// asynchronous initializer
			if (api.open) {
				api.openedFile = lastOpened;
				api.open(api.openedFile).then(function() {
					api.redraw();
					api.fitDiagram2Screen();
				});
				setTimeout(unbindInitializer, 1000);
			}
		});
	}

}