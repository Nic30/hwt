function ReDiscoveredErr(message) { // is exception
	this.name = 'ReDiscoveredErr';
	this.message = message;
	this.stack = (new Error()).stack;
}
ReDiscoveredErr.prototype = Object.create(Error.prototype);
ReDiscoveredErr.prototype.constructor = ReDiscoveredErr;

// Column container is like an array which allow negative indexing and indexing
// from most left (and ColumnContainer() is its constructor)
function ColumnContainer() {
	var self = {
		left : [],
		midleRight : [],
		push : function(indx, elm) {
			var arr;
			if (indx < 0) {
				arr = self.left;
				indx = -indx - 1;
			} else {
				arr = self.midleRight;
			}
			if (!arr[indx]) {
				arr[indx] = [];
			}
			arr[indx].push(elm);

		},
		accessFromLeft : function(indx) {
			var leftLen = self.left.length;
			if (indx < leftLen) {
				return self.left[indx];
			} else {
				return self.midleRight[indx - leftLen];
			}
		},
		length : function() {
			return self.left.length + self.midleRight.length;
		}
	};
	return self;
}

function RoutingNode() {
	return {
		"top" : null,
		"bottom" : null,
		"left" : null,
		"right" : null
	};
}

function generateLinks(nets) {
	var links = [];
	nets.forEach(function(net) {
		net.targets.forEach(function(target) {
			var link = {
				"net" : net,
				"source" : net.source.id,
				"sourceIndex" : net.source.portIndex,
				"target" : target.id,
				"targetIndex" : target.portIndex
			};
			links.push(link);
		});
	});

	return links;
}

// replaces ID with node object
function resolveNodesInLinks(nodes, links) {
	var dict = {};
	nodes.forEach(function(n) {
		dict[n.id] = n;
	});
	links.forEach(function(l) {
		var s = dict[l.source];
		var t = dict[l.target];
		if (s === undefined || t == undefined) {
			throw "Can not resolve link source or target";
		}
		l.source = s;
		l.target = t;
	});
}

function components2columns(nodes, links) { // discover component with most
	// ports (bigger) then go on both
	// sides and assign components to
	// columns
	function findBiggestComponent(nodes) { // find component with biggest no of
		// ports
		var biggestComponent = null;
		nodes.forEach(function(c) {
			if (biggestComponent) {
				var portCnt = biggestComponent.inputs.length
						+ biggestComponent.outputs.length;
				var thisCompPortCnt = c.inputs.length + c.outputs.length;
				if (thisCompPortCnt > portCnt)
					biggestComponent = c;
			} else {
				biggestComponent = c;
			}
		});
		return biggestComponent;
	}
	function constructTriplets(nodes, links) { // for each node discover what
		// is on left and right side
		var triplets = [];
		function Triplet() { // triplet obj constructor
			return {
				me : null,
				left : new Set(),
				right : new Set()
			};
		}
		nodes.forEach(function(c) {
			var t = new Triplet();
			t.me = c;
			for (var i2 = 0; i2 < links.length; i2++) {
				var l = links[i2];
				if (l.target == c && l.source != c)
					t.left.add(l.source)
				if (l.source == c && l.target != c)
					t.right.add(l.target)
			}
			triplets.push(t);
		});
		return triplets;
	}

	var columns = new ColumnContainer();
	var biggestComponent = findBiggestComponent(nodes);
	var triplets = constructTriplets(nodes, links);

	// now take triplets and build columns out of them
	// go from biggest component on left and right at symetricaly,
	// use set to control if this component was discovered
	var discovered = new Set();
	function popTriplet(component) {
		if (discovered.has(component))
			throw new ReDiscoveredErr();

		for (var index = 0; index < triplets.length; index++) {
			if (triplets[index].me == component)
				break;
		}
		if (index == triplets.length)
			throw "this component is not in triplets"
		var triplet = triplets[index];
		triplets.splice(index, 1);
		discovered.add(triplet.me);
		return triplet;
	}

	function makeColumns(baseIndx, triplet) {
		function discoverSide(sideSet, indxShift) {
			sideSet.forEach(function(c) {
				try {
					makeColumns(baseIndx + indxShift, popTriplet(c));
				} catch (e) {
					if (e instanceof ReDiscoveredErr) {
						// console.log("found same " +c.name )
					} else
						throw e;
				}
			});
		}
		discoverSide(triplet.left, -1);
		discoverSide(triplet.right, 1);

		columns.push(baseIndx, triplet.me);
	}
	makeColumns(0, popTriplet(biggestComponent));

	function heightOfPrevious(column, myIndx) {
		var y = 0;
		for (var i = 0; i < myIndx; i++) {
			y += column[i].height + 2 * COMPONENT_PADDING;
		}
		return y;
	}

	nodes.forEach(function(component) {
		component.netChannelPadding = {
			left : 0,
			right : 0,
			bottom : 0,
			top : 0
		};
		component.width = COLUMN_WIDTH;
		component.height = PORT_HEIGHT * 3 + PORT_HEIGHT
				* Math.max(component.inputs.length, component.outputs.length);

	});
	function positionsForColumn(x, column) {
		column.forEach(function(component, y) {
			component.x = COMPONENT_PADDING
					+ (COLUMN_WIDTH + 2 * COMPONENT_PADDING) * x;
			component.y = COMPONENT_PADDING + heightOfPrevious(column, y);
		});
	}
	// set possitions forEach column
	for (var x = 0; x < columns.length(); x++) {
		var column = columns.accessFromLeft(x);
		positionsForColumn(x, column);
	}

	// add unconnected components on right side
	var mostLeftColumn = columns.length() - 1;
	for (var i = 0; i < nodes.length; i++) {
		var component = nodes[i];
		if (component.x === undefined)
			columns.push(mostLeftColumn, component);
	}
	positionsForColumn(x, columns.midleRight[mostLeftColumn]);
}

/*
 * routing ideology: find shortest paths between routing nodes and then move
 * components and paths to not lay on each other
 * 
 * what are nodes for routing: component ports, component boundary corners
 * (component + padding)
 * 
 * what is content of routing node: pos(); set of grids connected to it;
 * leftTop, leftBottom, rightTop, rightBottom neighbor
 * 
 */

function RoutingNodesContainer(nodes) {
	var grid = [];

	function insertRNode(rnode, canGoLeftAndRight) {
		var pos = rnode.pos();
		var x = Math.ceil(pos[0]);
		var y = Math.ceil(pos[1]);

		// check if exists
		var col = grid[x];
		if (col) {
			if (col[y])
				return; // this node already exists
		} else {
			col = [];
			grid[x] = col;
		}
		grid[x][y] = rnode;

		var bottFound = false;
		var rightFound = false;
		// connect top
		for (var i = y - 1; i >= 0; i--) {
			var tn = col[i];
			if (tn) {
				if (tn.bottom) { // insert rnode between top and its bottom
					rnode.bottom = tn.bottom;
					rnode.bottom.top = rnode;
					bottFound = true;
				}
				tn.bottom = rnode;
				rnode.top = tn;
				break;
			}
		}
		// connect bottom
		if (!bottFound) {
			for (var i = y + 1; i < col.length; i++) {
				var bn = col[i];
				if (bn) {
					if (bn.top)
						throw "top node should be found recently";
					bn.top = rnode;
					rnode.bottom = bn;
					break;
				}
			}
		}

		if (canGoLeftAndRight) {
			// connect left
			for (var i = x - 1; i >= 0; i--) {
				var col = grid[i];
				if (col) {
					var ln = col[y];
					if (ln) {
						if (ln.right) {
							rnode.right = ln.right;
							rnode.right.left = rnode;
							rightFound = true;
						}
						ln.right = rnode;
						rnode.left = ln;
						break;
					}
				}

			}
			// find right
			if (!rightFound) {
				for (var i = x + 1; i < grid.length; i++) {
					var col = grid[i];
					if (col) {
						var rn = col[y];
						if (rn) {
							if (rnode.right)
								throw "right should be found recently";
							rnode.right = rn;
							rn.left = rnode;
							break;
						}
					}
				}
			}
		}
	}
	for (var ni = 0; ni < nodes.length; ni++) { // add corner nodes and node for
		// each port
		var node = nodes[ni];
		var leftTop = new RoutingNode();
		leftTop.originComponent = node;
		leftTop.pos = function() {
			return [ this.originComponent.x - COMPONENT_PADDING,
					this.originComponent.y - COMPONENT_PADDING ];
		};
		var leftBottom = new RoutingNode();
		leftBottom.originComponent = node;
		leftBottom.pos = function() {
			var c = this.originComponent;
			return [
					c.x - COMPONENT_PADDING - c.netChannelPadding.left,
					c.y + c.height + COMPONENT_PADDING
							+ c.netChannelPadding.bottom ];
		};
		var rightTop = new RoutingNode();
		rightTop.originComponent = node;
		rightTop.pos = function() {
			var c = this.originComponent;
			return [ c.x + c.width + COMPONENT_PADDING,
					c.y - COMPONENT_PADDING - c.netChannelPadding.top ];
		};
		var rightBottom = new RoutingNode();
		rightBottom.originComponent = node;
		rightBottom.pos = function() {
			var c = this.originComponent;
			return [
					c.x + c.width + COMPONENT_PADDING
							+ c.netChannelPadding.right,
					c.y + c.height + COMPONENT_PADDING
							+ c.netChannelPadding.bottom ];
		};
		// insert port nodes
		node.inputs.forEach(function(port, i) {
			var pn = new RoutingNode();
			pn.originComponent = node;
			pn.originPortIndex = i;
			pn.pos = function() {
				var c = this.originComponent;
				return [ c.x - COMPONENT_PADDING - c.netChannelPadding.left,
						c.y + (2 + this.originPortIndex) * PORT_HEIGHT ];
			};
			insertRNode(pn);
		});
		node.outputs.forEach(function(port, i) {
			var pn = new RoutingNode();
			pn.originComponent = node;
			pn.originPortIndex = i;
			pn.pos = function() {
				var c = this.originComponent;
				return [
						c.x + +c.width + COMPONENT_PADDING
								+ c.netChannelPadding.right,
						c.y + (2 + this.originPortIndex) * PORT_HEIGHT ];
			};
			insertRNode(pn);
		});

		insertRNode(leftTop, true);
		insertRNode(leftBottom, true);
		insertRNode(rightTop, true);
		insertRNode(rightBottom, true);

	}

	grid.visitFromLeftTop = function(fn) {
		for (var x = 0; x < grid.length; x++) {
			var col = grid[x];
			if (col) {
				for (var y = 0; y < col.length; y++) {
					var comp = col[y];
					if (comp) {
						fn(comp);
					}
				}
			}
		}
	}
	grid.componetOutputNode = function(component, portIndex) {
		var x = Math.ceil(component.x + component.width + COMPONENT_PADDING);
		var y = Math.ceil(component.y + (2 + portIndex) * PORT_HEIGHT);
		return grid[x][y];

	}
	grid.componetInputNode = function(component, portIndex) {
		var x = Math.ceil(component.x - COMPONENT_PADDING);
		var y = Math.ceil(component.y + (2 + portIndex) * PORT_HEIGHT);
		return grid[x][y];
	}

	return grid;

}
