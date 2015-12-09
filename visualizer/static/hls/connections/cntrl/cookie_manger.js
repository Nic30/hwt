function cookieManagerCntrl($scope, $cookies, $cookieStore) {
	var api = $scope.$parent.api;

	var lastVisitedTime =  $cookieStore.get('lastVisitedTime');
	var hour = 60*60*1000;
	
	if(!lastVisitedTime || (lastVisitedTime > ((new Date()).getTime() + hour ))){
		api.msg.info("For help press '?'");// display help msg
	}
	
	$cookieStore.put('lastVisitedTime', (new Date()).getTime())
	
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
				api.open(api.openedFile)
				setTimeout(unbindInitializer, 1000);
			}
		});
	}

}