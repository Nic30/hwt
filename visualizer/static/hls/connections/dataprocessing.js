
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

function findColumnWidth(nodes) {
	var INTERNAL_SPACE = 20;
	var FONT_SIZE = 7;
	var maxNamesLen = 0;
	nodes.forEach(function(n) {
		if (n.inputs.length > n.outputs.length) {
			var biggerArr = n.inputs;
			var smallerArr = n.outputs;
		} else {
			var biggerArr = n.outputs;
			var smallerArr = n.inputs;
		}
		biggerArr.forEach(function(p, i) {
			var nameBlen = p.name.length;
			var sp = smallerArr[i];

			var nameSlen = 0;
			if (sp)
				nameSlen = sp.name.length

			maxNamesLen = Math.max(maxNamesLen, nameBlen + nameSlen);
		});

	});
	return Math.max(FONT_SIZE * maxNamesLen + INTERNAL_SPACE, COLUMN_WIDTH);
}

function checkDataConsistency(nodes, nets) {
	function findComponent(id) {
		var tmp = nodes.filter(function(node) {
			return node.id == id
		});
		if (tmp.length == 0)
			throw "component with id " + id + " is not in nodes";
		else if (tmp.lengt > 1)
			throw "component with id " + id + " has multiple definitions";
		else
			return tmp[0];
	}
	function findPort(node, portIndex, isOutput) {
		if (isOutput) {
			var arr = node.outputs;
		} else {
			var arr = node.inputs;
		}
		var pi = arr[portIndex];
		if (!pi)
			throw "Component " + node.name + " has not port with index:"
					+ portIndex + "( isOutput:" + isOutput + " )"
		return pi;
	}
	function assertPortExists(portItem, isOutput) {
		var c = findComponent(portItem.id);
		findPort(c, portItem.portIndex, isOutput);
	}

	nets.forEach(function(net) {
		assertPortExists(net.source, true);
		net.targets.forEach(function(t) {
			assertPortExists(t, false);
		})
	});
}