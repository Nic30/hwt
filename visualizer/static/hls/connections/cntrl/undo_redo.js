function undoRedoCntrl($scope) {
	var api = $scope.$parent.api;
	$scope.buff = [];
	$scope.actualIndx = -1;
	
	api.undoRedoAction = function(fowardFn, backwardFn) {
		$scope.actualIndx++
		$scope.buff[$scope.actualIndx] = [fowardFn, backwardFn];
		delete $scope.buff[$scope.actualIndx +1 ];
	}

	api.redo = function() {
		var rec = $scope.buff[$scope.actualIndx+1];
		if(rec){
			rec[0]();
			$scope.actualIndx++;
		}
		api.redraw();
	}
	api.undo = function() {
		var rec = $scope.buff[$scope.actualIndx];
		if(rec){
			rec[1](); 
			$scope.actualIndx--;
		}
		api.redraw();
	}

}