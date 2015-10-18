function NetRouter(nodes, links) {
	var HORIZONTAL = "h";
	var VERTICAL = "v";
	var self = {
		nodes : nodes,
		links : links,
		grid : new RoutingNodesContainer(nodes),
		getNextPathDir : function(nodeA, nodeB) {
			if (!nodeA || !nodeB)
				throw "invalid use with undefined node";
			if (nodeA.left == nodeB || nodeA.right == nodeB) {
				return HORIZONTAL;
			}
			if (nodeA.top == nodeB || nodeA.bottom == nodeB) {
				return VERTICAL;
			}
			throw "Nodes are not even connected";
		},
		walkLinkSubPaths : function(link, fn) {
			var dir, dirTmp, last = link.start;
			var subPath = [ link.start ];
			var p = link.path[0];
			dir = self.getNextPathDir(last, p);
			last = link.start;

			for (var i = 0; i < link.path.length; i++) {// end is already in
				// path
				var p = link.path[i];
				dirTmp = self.getNextPathDir(last, p);
				if (dir != dirTmp) {
					subPath.push(p);
					fn(subPath, dir);
					subPath = [ p ];
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
			/*
			 * [0,4] [0,1] [2,4] [0,0] [1,1] [2,3] [4,4] [2,2] [3,3]
			 * 
			 * 
			 * [0,3] [0,1] [2,3] [0,0] [1,1] [2,2] [3,3]
			 */
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

			switch (dir) {
			case HORIZONTAL:
				var m = findMaxPossible("horizontal", 0, 0, subPath.length - 1);
				break;
			case VERTICAL:
				var m = findMaxPossible("vertical", 0, 0, subPath.length - 1);
				break;
			default:
				throw "invalid direction of subpath";
			}
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
			links.forEach(function(link) {
				self.walkLinkSubPaths(link,
						function(subPath, dir) {
							var i = self.findLowestNetIndexInSubPath(subPath, dir,
									link.net);
							switch (dir) {
							case HORIZONTAL:
								subPath.forEach(function(n) {
									n.horizontal[i] = link.net;
								});
								break;
							case VERTICAL:
								subPath.forEach(function(n) {
									n.vertical[i] = link.net;
								});
								break;
							default:
								throw "invalid direction of subpath";
							}
						});
			});

		}
	};
	return self;
}