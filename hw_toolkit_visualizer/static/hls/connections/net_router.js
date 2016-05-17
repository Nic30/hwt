function NetRouter(nodes, links) {
	var HORIZONTAL = "h";
	var VERTICAL = "v";
	function dir2arrName(dir) {
		switch (dir) {
		case HORIZONTAL:
			return "horizontal";
		case VERTICAL:
			return "vertical";
		default:
			throw "undefined dir";
		}
	}

	var self = {
		nodes : nodes,
		links : links,
		grid : new RoutingNodesContainer(nodes),
		getNextPathDir : function(nodeA, nodeB) {
			if (!nodeA || !nodeB)
				throw "Error:Invalid use with undefined node";
			if (nodeA.left == nodeB || nodeA.right == nodeB) {
				return HORIZONTAL;
			}
			if (nodeA.top == nodeB || nodeA.bottom == nodeB) {
				return VERTICAL;
			}
			throw "Error:Nodes are not even connected";
		},
		walkLinkSubPaths : function(link, fn) {
			var dir, dirTmp, last = link.start;
			var subPath = [ link.start ];
			var p = link.path[0];
			if (p == undefined) {
				fn(subPath, HORIZONTAL);
				return;
			}

			dir = self.getNextPathDir(last, p);

			for (var i = 0; i < link.path.length; i++) {
				// end is already in path
				var p = link.path[i];
				dirTmp = self.getNextPathDir(last, p);
				if (dir != dirTmp) {
					fn(subPath, dir);
					subPath = [ last, p ];
					dir = dirTmp;
				} else {
					subPath.push(p);
				}
				last = p;
			}
			if (subPath.length > 0) {
				fn(subPath, dir);
			}

		},
		findLowestNetIndexInSubPath : function(subPath, dir, net) {
			function findMaxPossible(arrName, minimum, leftIndx, rightIndx) {
				if (leftIndx == rightIndx) {
					var arr = subPath[leftIndx][arrName];
					return {
						"minFromSameNet" : arr.indexOf(net, minimum),
						"minFromLen" : Math.max(minimum, arr.length)
					};
				} else {

					var midle = Math.ceil((leftIndx + rightIndx) / 2);
					var ml = findMaxPossible(arrName, minimum, leftIndx,
							midle - 1);
					var mr = findMaxPossible(arrName, minimum, midle, rightIndx);

					while (ml.minFromSameNet != mr.minFromSameNet
							|| ml.minFromLen != mr.minFromLen) {
						if (ml.minFromSameNet == mr.minFromSameNet
								&& ml.minFromSameNet >= 0)
							break;
						var min = Math
								.max(ml.minFromSameNet, mr.minFromSameNet,
										ml.minFromLen, mr.minFromLen);
						var ml = findMaxPossible(arrName, min, leftIndx,
								midle - 1);
						var mr = findMaxPossible(arrName, min, midle, rightIndx);
					}
					return ml;
				}
			}
			var m = findMaxPossible(dir2arrName(dir), 0, 0, subPath.length - 1);
			if (m.minFromSameNet < 0) {
				return m.minFromLen;
			} else {
				return m.minFromSameNet;
			}
			return i;
		},
		route : function() {
			/*
			 * paths keep out ideology: for each routing node build vertical and
			 * horizontal netlist if path is curved in this node vertical index ==
			 * horizontal index if there is path from same net join them for
			 * each component increase padding to let space for nets from each
			 * node extract routing node position for this path (use horizontal
			 * and/or vertical index, this node pos and NET_PADDING ) draw path
			 */
			function wipeNetFromSubpath(net, subPath, dir) {
				var arrName = dir2arrName(dir);
				var rmFn = function(n) {
					var i = n[arrName].indexOf(net)
					if (i >= 0)
						n[arrName][i] = undefined;
				}
				subPath.forEach(rmFn);
			}
			self.grid.visitFromLeftTop(function(n) { // init node
				n.vertical = [];
				n.horizontal = [];
			});
			// route grids
			links.forEach(function(l) {
				var grid = self.grid;
				l.start = grid.componetOutputNode(l.source, l.sourceIndex);
				l.end = grid.componetInputNode(l.target, l.targetIndex);
				l.path = astar.search(grid, l.start, l.end);
			});
			links.forEach(function(link, li) {
				self.walkLinkSubPaths(link, function(subPath, dir) {
					var i = self.findLowestNetIndexInSubPath(subPath, dir,
							link.net);
					wipeNetFromSubpath(link.net, subPath, dir);
					var arrName = dir2arrName(dir);
					subPath.forEach(function(n) {
						n[arrName][i] = link.net;
					});
				});
			});
			self.moveComponetsOutOfNets();
		},
		moveComponetsOutOfNets : function() {
			/*
			 * find width of channels add it to component positions
			 */
			function netPadding(netCnt) {
				return netCnt * (NET_PADDING + 1);
			}
			var grid = self.grid;

			grid.maxNetCntY = [];
			grid.maxNetCntX = [];

			for (var x = 0; x < grid.length; x++) { 
				// discover sizes of net channels
				var col = grid[x];
				if (col) {
					if (grid.maxNetCntX[x] === undefined)
						grid.maxNetCntX[x] = 0;
					for (var y = 0; y < col.length; y++) {
						var n = col[y];
						if (n && !( n instanceof RoutingBoundry)) {
							var netCntY = n.horizontal.length;
							var netCntX = n.vertical.length;

							if (grid.maxNetCntY[y] === undefined)
								grid.maxNetCntY[y] = 0;
							if (grid.maxNetCntY[y] < netCntY)
								grid.maxNetCntY[y] = netCntY;
							if (grid.maxNetCntX[x] < netCntX)
								grid.maxNetCntX[x] = netCntX;
						}
					}
				}
			}

			var sumOfNetOffsetsX = [];
			var sumOfNetOffsetsY = [];
			var offset = 0;
			grid.maxNetCntX.forEach(function(d, i) {
				if (d) {
					offset += netPadding(d);
				}
				sumOfNetOffsetsX[i] = offset;
			});
			offset = 0;
			grid.maxNetCntY.forEach(function(d, i) {
				if (d) {
					offset += netPadding(d);
				}
				sumOfNetOffsetsY[i] = offset;
			});
			function previousDefined(arr, indx) {
				return arr[indx]
				for (var i = indx - 1; i >= 0; i--) {
					var offset = arr[i];
					if (offset) {
						return offset;
					}
				}
				return 0;
			}
			nodes.forEach(function(n) {
				var x0 = n.x - COMPONENT_PADDING;
				var x1 = n.x + n.width + COMPONENT_PADDING;
				var y0 = n.y - COMPONENT_PADDING;
				var y1 = n.y + n.height + COMPONENT_PADDING;
				var npTop = netPadding(previousDefined(grid.maxNetCntY, y0));
				if (npTop)
					n.netChannelPadding.top = npTop;
				var npLeft = netPadding(previousDefined(grid.maxNetCntX, x0));
				if (npLeft)
					n.netChannelPadding.left = npLeft;
				// var npBottom = netPadding(grid.maxNetCntY[y1]);
				// if(npBottom)
				// n.netChannelPadding.bottom = npBottom;
				// var npRight = netPadding(grid.maxNetCntX[x1]);
				// if(npRight)
				// n.netChannelPadding.right = npRight;
				var xOffset = sumOfNetOffsetsX[x0];
				if (xOffset != undefined)
					n.x = xOffset + n.x;
				var yOffset = sumOfNetOffsetsY[y0];
				if (yOffset != undefined)
					n.y = yOffset + n.y;
			});
		}
	};
	return self;
}