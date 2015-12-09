function filebrowserCntrl($scope, $http) {
	var api = $scope.$parent.api;
	var fileDialog = $('#fileDialog');
	var saveDialog = $('#saveDialog');
	$scope.rootDir = "";
	api.openedFile = '';
	
	var filesRowData = [];
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
	api.new = function(){
		api.nodes = [];
		api.nets = [];
		api.redraw();
		api.openedFile = '';
	} 
	api.open = function(path) {
		return $http.get('/hls/connections-data/' + path).then(
				function(res) {
					var nets = res.data.nets;
					var nodes = res.data.nodes;
					api.nodes = nodes;
					api.nets = nets;
				}, function errorCallback(response) {
					api.msg.error("Can not open file", path);
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
			api.openedFile = path;
			fileDialog.modal('hide');
			
			api.open(path).then(function(){
				api.redraw();
				api.fitDiagram2Screen();
			});
		}
	}

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


	api.fileDialog = function(conf) {
		//d3.selectAll("#chartWrapper").html(""); // [TODO] to different controller
		$scope.conf = conf;
		fileDialog.modal('show');
		filesRowData = [];
		$scope.loadFolderData("");
	}

	api.save = function(path) {
		var data = {
			"path" : path,
			"nodes" : api.nodes,
			"nets" : api.nets
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