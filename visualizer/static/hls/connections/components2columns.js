var DIRECTION = {
	IN : "IN",
	OUT : "OUT"
};

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
				indx = (-indx) - 1;
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
		get : function(indx){
			if(indx<0)
				return self.left[(-indx) -1];
			else
				return self.midleRight[indx];
		},
		mostRightIndx(){
			return self.midleRight.length -1;
		},
		mostLeftIndx(){
			return - (self.left.length);
		},
		length : function() {
			return self.left.length + self.midleRight.length;
		}
	};
	return self;
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
	function rmDiscoveredFlag(nodes){
		nodes.forEach(function (n){
			delete n.discovered;
		})
	}
	rmDiscoveredFlag(nodes);
	// now take triplets and build columns out of them
	// go from biggest component on left and right at symetricaly,
	// use set to control if this component was discovered
	function popTriplet(component) {
		if (component.discovered)
			throw new ReDiscoveredErr();

		for (var index = 0; index < triplets.length; index++) {
			if (triplets[index].me == component)
				break;
		}
		if (index == triplets.length)
			throw "this component is not in triplets"
		var triplet = triplets[index];
		triplets.splice(index, 1);
		triplet.me.discovered = true;
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

		if (!triplet.me.isExternalPort)
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


	// add unconnected components on right side
	var mostRightColumn = columns.mostRightIndx()  +1;
	var mostLeftColumn = columns.mostLeftIndx() -1;
	nodes.forEach(function(component) {
		
		if (component.isExternalPort){
			if(component.direction == DIRECTION.IN){
				columns.push(mostLeftColumn, component);
			} else{
				columns.push(mostRightColumn, component);
			}
		}else if( !component.discovered){
			columns.push(mostRightColumn, component);
		}
		
	});
	// set possitions forEach column
	var x = 0;
	for (var x; x < columns.length(); x++) {
		var column = columns.accessFromLeft(x);
		positionsForColumn(x, column);
	}	
	// @assert
	nodes.forEach(function(n) {
		if (!Number.isFinite(n.x) || !Number.isFinite(n.y))
			throw "Node " + n.name + " is not properly placed";
	});
	rmDiscoveredFlag(nodes);
	return columns;
}