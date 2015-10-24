
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
				throw "Error:invalid use with undefined node";
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
			if (p == undefined){
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
				// console.log([leftIndx, rightIndx])
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
			self.grid.visitFromLeftTop(function(n) {
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

		}
	};
	return self;
}