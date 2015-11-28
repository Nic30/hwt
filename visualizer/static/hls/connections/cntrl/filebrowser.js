function filebrowserCntrl($scope, $http) {
	var api = $scope.$parent.api;
	var fileDialog = $('#fileDialog');
	var saveDialog = $('#saveDialog');
	$scope.doSave = false;
	function sizeCellStyle() {
		return {
			'text-align' : 'right'
		};
	}

	function innerCellRenderer(params) {
		var image;
		if (params.node.group) {
			image = 'folder';
		} else {
			image = 'file';
		}
		var imageFullUrl = "/static/hls/connections/graphic/" + image + '.png';
		return '<img src="' + imageFullUrl + '" style="padding-left: 4px;" /> '
				+ params.data.name;
	}

	var columnDefs = [ {
		headerName : "Name",
		field : "name",
		width : 350,
		cellRenderer : {
			renderer : 'group',
			innerRenderer : innerCellRenderer
		}
	}, {
		headerName : "Size",
		field : "size",
		width : 100,
		cellStyle : sizeCellStyle
	}, {
		headerName : "Type",
		field : "type",
		width : 150
	}, {
		headerName : "Date Modified",
		field : "dateModified",
		width : 198
	} ];
	$scope.open = function() {
		return $http.get('/hls/connections-data/' + $scope.openedFile).then(
				function(res) {
					var nets = res.data.nets;
					var nodes = res.data.nodes;
					api.nodes = nodes;
					api.nets = nets;
				}, function errorCallback(response) {
					api.msg.error("Can not open file", $scope.openedFile);
				});
	}

	function rowClicked(params) {
		var node = params.node;
		var path = node.data.name;
		var tmpnode = node;
		while (tmpnode.parent) {
			var tmpnode = tmpnode.parent;
			path = tmpnode.data.name + '/' + path;
		}
		if (node.group) {
			if (!node.expanded) {
				node.children = [];
				return;
			}
			$scope.loadFolderData(path);
		} else {
			$scope.openedFile = path;
			fileDialog.modal('hide');
			
			$scope.open().then(function(){
				api.redraw();
			});
		}
	}

	$scope.rootDir = "";
	var filesRowData = [];

	$scope.fileGridOptions = {
		columnDefs : columnDefs,
		rowData : filesRowData,
		rowSelection : 'multiple',
		rowsAlreadyGrouped : true,
		enableColResize : true,
		enableSorting : true,
		rowHeight : 20,
		icons : {
			groupExpanded : '<i class="fa fa-minus-square-o"/>',
			groupContracted : '<i class="fa fa-plus-square-o"/>'
		},
		onRowClicked : rowClicked
	};

	$scope.loadFolderData = function(path) {
		$http.get('/hls/connections-data-ls/' + path)
		.then(function(res) {
			function findDir(path) {
				if (path == "")
					return filesRowData

				var dir = filesRowData.filter(function(f) {
					return f.data.name == path;
				})[0]

				return dir;
			}
			var files = res.data;
			var dir = findDir(path);
			if (dir.children === undefined) {
				filesRowData = files;
			} else {
				dir.children = files;
			}

			$scope.fileGridOptions.api.setRowData(filesRowData);
		});
	}

	$scope.openedFile = 'example1.json';
	api.fileDialog = function(doSave) {
		//d3.selectAll("#chartWrapper").html(""); // [TODO] to different controller
		$scope.doSave = doSave;
		fileDialog.modal('show');
		filesRowData = [];
		$scope.loadFolderData("");

	}

	$scope.save = function(path) {
		var data = {
			"path" : path,
			"nodes" : $scope.nodes,
			"nets" : $scope.nets
		};
		return $http.post("/hls/connections-save", data, {
			headers : {
				'Content-Type' : 'application/json'
			}
		}).then(function(response) {
			return response;
		});
	};

	api.saveAs = function() {
		filesRowData = [];
		$scope.loadFolderData("");
		saveDialog.modal('show');
	};

}