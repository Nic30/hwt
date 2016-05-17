function RoutingBoundry(parentNode) {
	this.parent = parentNode;
	return this;
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
	grid.rNodes = new Set();

	grid.visitFromLeftTop = function(fn) {
		grid.rNodes.forEach(fn);
	};
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
	function gridAsign(x, y, item) {
		if (!grid[x])
			grid[x] = [];
		grid[x][y] = item;
	}
	function insertRectangularBoundry(node) {
		var x0 = node.x;
		var y0 = node.y;
		var width = node.widht
		var height = node.height;
		var boundry = new RoutingBoundry(node);
		var y_max = y0 + height
		var x_max = x0 + width;

		for (var y = y0; y < y_max; y++) {
			gridAsign(x0, y, boundry);
			gridAsign(x_max, y, boundry);
		}
		for(var x = x0; x < x_max;x++){
			gridAsign(x, y0, boundry);
			gridAsign(x, y_max, boundry);
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
		grid.rNodes.add(rnode)
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
		insertRectangularBoundry(node);

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
	grid.rNodes.forEach(function(n) {
		var p = n.pos()
		var x0 = p[0];
		var y0 = p[1];
		for (var x = x0 + 1; x < grid.length; x++) {
			var row = grid[x];
			if (row) {
				var neighbor = row[y0];
				if (neighbor) {
					if (neighbor instanceof RoutingBoundry)
						break;
					neighbor.left = n;
					n.right = neighbor;
					break;
				}
			}
		}
		var column = grid[x0];
		var y_max = column.length;
		for (var y = y0 + 1; y < y_max; y++) {
			var neighbor = column[y];
			if (neighbor) {
				if (neighbor instanceof RoutingBoundry)
					break;
				neighbor.top = n;
				n.bottom = neighbor;
				break;
			}
		}
	})
	grid.rNodes.forEach(function(n) {
		if (!(n.left || n.right || n.top || n.bottom))
			throw "Node is not connected";
		if (n.left && !n.left.pos)
			throw "left is not what was expected";
		if (n.right && !n.right.pos)
			throw "right is not what was expected";
		if (n.top && !n.top.pos)
			throw "top is not what was expected";
		if (n.bottom && !n.bottom.pos)
			throw "bottom is not what was expected";
	});

	return grid;
}
