function RoutingBoundry(parentNode) {
	return {
		"parent" : parentNode
	}
}

function RoutingNode() {
	return {
		"top" : null,
		"bottom" : null,
		"left" : null,
		"right" : null
	};
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
	grid.visitFromLeftTop = function(fn) {
		for (var x = 0; x < grid.length; x++) {
			var col = grid[x];
			if (col) {
				for (var y = 0; y < col.length; y++) {
					var comp = col[y];
					if (comp && !(comp instanceof RoutingBoundry)) {
						fn(comp);
					}
				}
			}
		}
	}
	grid.componetOutputNode = function(component, portIndex) {
		var x = component.x + component.width + COMPONENT_PADDING
				+ component.netChannelPadding.right;
		var y = component.y + (2 + portIndex) * PORT_HEIGHT;
		return this[x][y];

	}
	grid.componetInputNode = function(component, portIndex) {
		var x = component.x - COMPONENT_PADDING
				- component.netChannelPadding.left;
		var y = component.y + (2 + portIndex) * PORT_HEIGHT;
		return this[x][y];
	}

	function insertRectangularBoundry(node) {
		var x0 = node.x;
		var y0 = node.y;
		var width = node.widht
		var height = node.height;
		var boundry = new RoutingBoundry(node);

		for (var y = y0; y < y0 + height; y++) {
			var col = grid[y];
			if (col == undefined) {
				col = [];
				grid[y] = col;
			}
			if (y == y0 || y == y0 + height - 1) {
				for (var x = x0; x < x0 + width; x++) {
					col[x] = boundry;
				}
			} else {
				col[x0] = boundry;
				col[x0 + width - 1] = boundry;
			}
		}
	}

	function insertRNode(rnode, canGoLeftAndRight) {
		var pos = rnode.pos();
		var x = pos[0];
		var y = pos[1];

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
			if (tn instanceof RoutingBoundry)
				break;
			if (tn) {
				if (tn.bottom) { // insert rnode between top and its
					// bottom
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
				if (bn instanceof RoutingBoundry)
					break;
				if (bn) {
					if (bn.top)
						throw "Error: top node should be founded recently";
					bn.top = rnode;
					rnode.bottom = bn;
					break;
				}
			}
		}

		// connect left
		if (canGoLeftAndRight) {
			for (var i = x - 1; i >= 0; i--) {
				var col = grid[i];
				if (col) {
					var ln = col[y];
					if (ln instanceof RoutingBoundry)
						break;
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
						if (rn instanceof RoutingBoundry)
							break;
						if (rn) {
							if (rnode.right)
								throw "Error: right should be founded recently";
							rnode.right = rn;
							rn.left = rnode;
							break;
						}
					}
				}
			}
		}
	}
	(function normalizeNodesPosition(nodes) {
		nodes.forEach(function(n) {
			n.x = Math.ceil(n.x);
			n.y = Math.ceil(n.y);
		});
	})(nodes);
	for (var ni = 0; ni < nodes.length; ni++) {
		// add corner nodes and node for each port
		var node = nodes[ni];
		insertRectangularBoundry(node.x, node.y, node.width, node.height);

		if (!(node.isExternalPort && node.direction == DIRECTION.IN)) {
			var leftTop = new RoutingNode();
			leftTop.originComponent = node;
			leftTop.pos = function() {
				var c = this.originComponent;
				return [
						this.originComponent.x - COMPONENT_PADDING
								- c.netChannelPadding.left,
						this.originComponent.y - COMPONENT_PADDING
								- c.netChannelPadding.top ];
			};
			insertRNode(leftTop, true);

			var leftBottom = new RoutingNode();
			leftBottom.originComponent = node;
			leftBottom.pos = function() {
				var c = this.originComponent;
				return [
						c.x - COMPONENT_PADDING - c.netChannelPadding.left,
						c.y + c.height + COMPONENT_PADDING
								+ c.netChannelPadding.bottom ];
			};
			insertRNode(leftBottom, true);
		}

		if (!(node.isExternalPort && node.direction == DIRECTION.OUT)) {
			var rightTop = new RoutingNode();
			rightTop.originComponent = node;
			rightTop.pos = function() {
				var c = this.originComponent;
				return [ c.x + c.width + COMPONENT_PADDING,
						c.y - COMPONENT_PADDING - c.netChannelPadding.top ];
			};
			insertRNode(rightTop, true);

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
			insertRNode(rightBottom, true);
		}
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
						c.x + c.width + COMPONENT_PADDING
								+ c.netChannelPadding.right,
						c.y + (2 + this.originPortIndex) * PORT_HEIGHT ];
			};
			insertRNode(pn);
		});

	}

	return grid;
}
