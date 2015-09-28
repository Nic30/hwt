var svg, tooltip, biHiSankey, path, defs, colorScale, highlightColorScale, isTransitioning;

var OPACITY = {
	NODE_DEFAULT : 0.9,
	NODE_FADED : 0.1,
	NODE_HIGHLIGHT : 0.8,
	LINK_DEFAULT : 0.6,
	LINK_FADED : 0.05,
	LINK_HIGHLIGHT : 0.9
}
var TYPES = [ "Asset", "Expense", "Revenue", "Equity", "Liability" ];
var TYPE_COLORS = [ "#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#66a61e",
		"#e6ab02", "#a6761d" ];
var TYPE_HIGHLIGHT_COLORS = [ "#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3",
		"#a6d854", "#ffd92f", "#e5c494" ];
var LINK_COLOR = "#b3b3b3", INFLOW_COLOR = "#2E86D1", OUTFLOW_COLOR = "#D63028", NODE_WIDTH = 36;
var COLLAPSER = {
	RADIUS : NODE_WIDTH / 2,
	SPACING : 2
}, OUTER_MARGIN = 10;
var MARGIN = {
	TOP : 2 * (COLLAPSER.RADIUS + OUTER_MARGIN),
	RIGHT : OUTER_MARGIN,
	BOTTOM : OUTER_MARGIN,
	LEFT : OUTER_MARGIN
};
var TRANSITION_DURATION = 400, HEIGHT = 500 - MARGIN.TOP - MARGIN.BOTTOM, WIDTH = 960
		- MARGIN.LEFT - MARGIN.RIGHT, LAYOUT_INTERATIONS = 32, REFRESH_INTERVAL = 7000;

function formatNumber(d) {
	var numberFormat = d3.format(",.0f"); // zero decimal places
	return "£" + numberFormat(d);
};
function formatFlow(d) {
	var flowFormat = d3.format(",.0f"); // zero decimal places with sign
	return "£" + flowFormat(Math.abs(d)) + (d < 0 ? " CR" : " DR");
};
// Used when temporarily disabling user interractions to allow animations to
// complete
function disableUserInterractions(time) {
	isTransitioning = true;
	setTimeout(function() {
		isTransitioning = false;
	}, time);
};
function hideTooltip() {
	return tooltip.transition().duration(TRANSITION_DURATION).style("opacity",
			0);
};
function showTooltip() {
	return tooltip.style("left", d3.event.pageX + "px").style("top",
			d3.event.pageY + 15 + "px").transition().duration(
			TRANSITION_DURATION).style("opacity", 1);
};
var colorScale = d3.scale.ordinal().domain(TYPES).range(TYPE_COLORS), highlightColorScale = d3.scale
		.ordinal().domain(TYPES).range(TYPE_HIGHLIGHT_COLORS)

var svg = d3.select("#chart").append("svg").attr("width",
		WIDTH + MARGIN.LEFT + MARGIN.RIGHT).attr("height",
		HEIGHT + MARGIN.TOP + MARGIN.BOTTOM).append("g").attr("transform",
		"translate(" + MARGIN.LEFT + "," + MARGIN.TOP + ")");

svg.append("g").attr("id", "links");
svg.append("g").attr("id", "nodes");
svg.append("g").attr("id", "collapsers");

tooltip = d3.select("#chart").append("div").attr("id", "tooltip");

tooltip.style("opacity", 0).append("p").attr("class", "value");

biHiSankey = d3.biHiSankey();

// Set the biHiSankey diagram properties
biHiSankey.nodeWidth(NODE_WIDTH).nodeSpacing(10).linkSpacing(4)
		.arrowheadScaleFactor(0.5) // Specifies that 0.5 of the link's stroke
		// WIDTH should be allowed for the marker at
		// the end of the link.
		.size([ WIDTH, HEIGHT ]);

path = biHiSankey.link().curvature(0.45);

defs = svg.append("defs");

defs.append("marker").style("fill", LINK_COLOR).attr("id", "arrowHead").attr(
		"viewBox", "0 0 6 10").attr("refX", "1").attr("refY", "5").attr(
		"markerUnits", "strokeWidth").attr("markerWidth", "1").attr(
		"markerHeight", "1").attr("orient", "auto").append("path").attr("d",
		"M 0 0 L 1 0 L 6 5 L 1 10 L 0 10 z");

defs.append("marker").style("fill", OUTFLOW_COLOR)
		.attr("id", "arrowHeadInflow").attr("viewBox", "0 0 6 10").attr("refX",
				"1").attr("refY", "5").attr("markerUnits", "strokeWidth").attr(
				"markerWidth", "1").attr("markerHeight", "1").attr("orient",
				"auto").append("path").attr("d",
				"M 0 0 L 1 0 L 6 5 L 1 10 L 0 10 z");

defs.append("marker").style("fill", INFLOW_COLOR).attr("id", "arrowHeadOutlow")
		.attr("viewBox", "0 0 6 10").attr("refX", "1").attr("refY", "5").attr(
				"markerUnits", "strokeWidth").attr("markerWidth", "1").attr(
				"markerHeight", "1").attr("orient", "auto").append("path")
		.attr("d", "M 0 0 L 1 0 L 6 5 L 1 10 L 0 10 z");

function update() {
	var link, linkEnter, node, nodeEnter, collapser, collapserEnter;

	function dragmove(node) {
		node.x = Math.max(0, Math.min(WIDTH - node.width, d3.event.x));
		node.y = Math.max(0, Math.min(HEIGHT - node.height, d3.event.y));
		d3.select(this).attr("transform",
				"translate(" + node.x + "," + node.y + ")");
		biHiSankey.relayout();
		svg.selectAll(".node").selectAll("rect").attr("height", function(d) {
			return d.height;
		});
		link.attr("d", path);
	}

	function containChildren(node) {
		node.children.forEach(function(child) {
			child.state = "contained";
			child.parent = this;
			child._parent = null;
			containChildren(child);
		}, node);
	}

	function expand(node) {
		node.state = "expanded";
		node.children.forEach(function(child) {
			child.state = "collapsed";
			child._parent = this;
			child.parent = null;
			containChildren(child);
		}, node);
	}

	function collapse(node) {
		node.state = "collapsed";
		containChildren(node);
	}

	function restoreLinksAndNodes() {
		link.style("stroke", LINK_COLOR).style("marker-end", function() {
			return 'url(#arrowHead)';
		}).transition().duration(TRANSITION_DURATION).style("opacity",
				OPACITY.LINK_DEFAULT);

		node.selectAll("rect").style("fill", function(d) {
			d.color = colorScale(d.type.replace(/ .*/, ""));
			return d.color;
		}).style("stroke", function(d) {
			return d3.rgb(colorScale(d.type.replace(/ .*/, ""))).darker(0.1);
		}).style("fill-opacity", OPACITY.NODE_DEFAULT);

		node.filter(function(n) {
			return n.state === "collapsed";
		}).transition().duration(TRANSITION_DURATION).style("opacity",
				OPACITY.NODE_DEFAULT);
	}

	function showHideChildren(node) {
		disableUserInterractions(2 * TRANSITION_DURATION);
		hideTooltip();
		if (node.state === "collapsed") {
			expand(node);
		} else {
			collapse(node);
		}

		biHiSankey.relayout();
		update();
		link.attr("d", path);
		restoreLinksAndNodes();
	}

	function highlightConnected(g) {
		link.filter(function(d) {
			return d.source === g;
		}).style("marker-end", function() {
			return 'url(#arrowHeadInflow)';
		}).style("stroke", OUTFLOW_COLOR)
				.style("opacity", OPACITY.LINK_DEFAULT);

		link.filter(function(d) {
			return d.target === g;
		}).style("marker-end", function() {
			return 'url(#arrowHeadOutlow)';
		}).style("stroke", INFLOW_COLOR).style("opacity", OPACITY.LINK_DEFAULT);
	}

	function fadeUnconnected(g) {
		link.filter(function(d) {
			return d.source !== g && d.target !== g;
		}).style("marker-end", function() {
			return 'url(#arrowHead)';
		}).transition().duration(TRANSITION_DURATION).style("opacity",
				OPACITY.LINK_FADED);

		node.filter(function(d) {
			return (d.name === g.name) ? false : !biHiSankey.connected(d, g);
		}).transition().duration(TRANSITION_DURATION).style("opacity",
				OPACITY.NODE_FADED);
	}

	link = svg.select("#links").selectAll("path.link").data(
			biHiSankey.visibleLinks(), function(d) {
				return d.id;
			});

	link.transition().duration(TRANSITION_DURATION).style("stroke-WIDTH",
			function(d) {
				return Math.max(1, d.thickness);
			}).attr("d", path).style("opacity", OPACITY.LINK_DEFAULT);

	link.exit().remove();

	linkEnter = link.enter().append("path").attr("class", "link").style("fill",
			"none");

	linkEnter.on('mouseenter', function(d) {
		if (!isTransitioning) {
			showTooltip().select(".value").text(
					function() {
						if (d.direction > 0) {
							return d.source.name + " → " + d.target.name + "\n"
									+ formatNumber(d.value);
						}
						return d.target.name + " ← " + d.source.name + "\n"
								+ formatNumber(d.value);
					});

			d3.select(this).style("stroke", LINK_COLOR).transition().duration(
					TRANSITION_DURATION / 2).style("opacity",
					OPACITY.LINK_HIGHLIGHT);
		}
	});

	linkEnter.on('mouseleave', function() {
		if (!isTransitioning) {
			hideTooltip();

			d3.select(this).style("stroke", LINK_COLOR).transition().duration(
					TRANSITION_DURATION / 2).style("opacity",
					OPACITY.LINK_DEFAULT);
		}
	});

	linkEnter.sort(function(a, b) {
		return b.thickness - a.thickness;
	}).classed("leftToRight", function(d) {
		return d.direction > 0;
	}).classed("rightToLeft", function(d) {
		return d.direction < 0;
	}).style("marker-end", function() {
		return 'url(#arrowHead)';
	}).style("stroke", LINK_COLOR).style("opacity", 0).transition().delay(
			TRANSITION_DURATION).duration(TRANSITION_DURATION).attr("d", path)
			.style("stroke-WIDTH", function(d) {
				return Math.max(1, d.thickness);
			}).style("opacity", OPACITY.LINK_DEFAULT);

	node = svg.select("#nodes").selectAll(".node").data(
			biHiSankey.collapsedNodes(), function(d) {
				return d.id;
			});

	node.transition().duration(TRANSITION_DURATION).attr("transform",
			function(d) {
				return "translate(" + d.x + "," + d.y + ")";
			}).style("opacity", OPACITY.NODE_DEFAULT).select("rect").style(
			"fill", function(d) {
				d.color = colorScale(d.type.replace(/ .*/, ""));
				return d.color;
			}).style("stroke", function(d) {
		return d3.rgb(colorScale(d.type.replace(/ .*/, ""))).darker(0.1);
	}).style("stroke-WIDTH", "1px").attr("height", function(d) {
		return d.height;
	}).attr("width", biHiSankey.nodeWidth());

	node.exit().transition().duration(TRANSITION_DURATION).attr("transform",
			function(d) {
				var collapsedAncestor, endX, endY;
				collapsedAncestor = d.ancestors.filter(function(a) {
					return a.state === "collapsed";
				})[0];
				endX = collapsedAncestor ? collapsedAncestor.x : d.x;
				endY = collapsedAncestor ? collapsedAncestor.y : d.y;
				return "translate(" + endX + "," + endY + ")";
			}).remove();

	nodeEnter = node.enter().append("g").attr("class", "node");

	nodeEnter
			.attr(
					"transform",
					function(d) {
						var startX = d._parent ? d._parent.x : d.x, startY = d._parent ? d._parent.y
								: d.y;
						return "translate(" + startX + "," + startY + ")";
					}).style("opacity", 1e-6).transition().duration(
					TRANSITION_DURATION).style("opacity", OPACITY.NODE_DEFAULT)
			.attr("transform", function(d) {
				return "translate(" + d.x + "," + d.y + ")";
			});

	nodeEnter.append("text");
	nodeEnter.append("rect").style("fill", function(d) {
		d.color = colorScale(d.type.replace(/ .*/, ""));
		return d.color;
	}).style("stroke", function(d) {
		return d3.rgb(colorScale(d.type.replace(/ .*/, ""))).darker(0.1);
	}).style("stroke-WIDTH", "1px").attr("height", function(d) {
		return d.height;
	}).attr("width", biHiSankey.nodeWidth());

	node
			.on(
					"mouseenter",
					function(g) {
						if (!isTransitioning) {
							restoreLinksAndNodes();
							highlightConnected(g);
							fadeUnconnected(g);

							d3.select(this).select("rect").style(
									"fill",
									function(d) {
										d.color = d.netFlow > 0 ? INFLOW_COLOR
												: OUTFLOW_COLOR;
										return d.color;
									}).style("stroke", function(d) {
								return d3.rgb(d.color).darker(0.1);
							}).style("fill-opacity", OPACITY.LINK_DEFAULT);

							tooltip
									.style("left", g.x + MARGIN.LEFT + "px")
									.style(
											"top",
											g.y + g.height + MARGIN.TOP + 15
													+ "px")
									.transition()
									.duration(TRANSITION_DURATION)
									.style("opacity", 1)
									.select(".value")
									.text(
											function() {
												var additionalInstructions = g.children.length ? "\n(Double click to expand)"
														: "";
												return g.name
														+ "\nNet flow: "
														+ formatFlow(g.netFlow)
														+ additionalInstructions;
											});
						}
					});

	node.on("mouseleave", function() {
		if (!isTransitioning) {
			hideTooltip();
			restoreLinksAndNodes();
		}
	});

	node.filter(function(d) {
		return d.children.length;
	}).on("dblclick", showHideChildren);

	// allow nodes to be dragged to new positions
	node.call(d3.behavior.drag().origin(function(d) {
		return d;
	}).on("dragstart", function() {
		this.parentNode.appendChild(this);
	}).on("drag", dragmove));

	// add in the text for the nodes
	node.filter(function(d) {
		return d.value !== 0;
	}).select("text").attr("x", -6).attr("y", function(d) {
		return d.height / 2;
	}).attr("dy", ".35em").attr("text-anchor", "end").attr("transform", null)
			.text(function(d) {
				return d.name;
			}).filter(function(d) {
				return d.x < WIDTH / 2;
			}).attr("x", 6 + biHiSankey.nodeWidth()).attr("text-anchor",
					"start");

	collapser = svg.select("#collapsers").selectAll(".collapser").data(
			biHiSankey.expandedNodes(), function(d) {
				return d.id;
			});

	collapserEnter = collapser.enter().append("g").attr("class", "collapser");

	collapserEnter.append("circle").attr("r", COLLAPSER.RADIUS).style("fill",
			function(d) {
				d.color = colorScale(d.type.replace(/ .*/, ""));
				return d.color;
			});

	collapserEnter.style("opacity", OPACITY.NODE_DEFAULT).attr(
			"transform",
			function(d) {
				return "translate(" + (d.x + d.width / 2) + ","
						+ (d.y + COLLAPSER.RADIUS) + ")";
			});

	collapserEnter.on("dblclick", showHideChildren);

	collapser.select("circle").attr("r", COLLAPSER.RADIUS);

	collapser.transition().delay(TRANSITION_DURATION).duration(
			TRANSITION_DURATION).attr(
			"transform",
			function(d, i) {
				return "translate("
						+ (COLLAPSER.RADIUS + i * 2
								* (COLLAPSER.RADIUS + COLLAPSER.SPACING)) + ","
						+ (-COLLAPSER.RADIUS - OUTER_MARGIN) + ")";
			});

	collapser.on("mouseenter",
			function(g) {
				if (!isTransitioning) {
					showTooltip().select(".value").text(function() {
						return g.name + "\n(Double click to collapse)";
					});

					var highlightColor = highlightColorScale(g.type.replace(
							/ .*/, ""));

					d3.select(this).style("opacity", OPACITY.NODE_HIGHLIGHT)
							.select("circle").style("fill", highlightColor);

					node.filter(function(d) {
						return d.ancestors.indexOf(g) >= 0;
					}).style("opacity", OPACITY.NODE_HIGHLIGHT).select("rect")
							.style("fill", highlightColor);
				}
			});

	collapser.on("mouseleave", function(g) {
		if (!isTransitioning) {
			hideTooltip();
			d3.select(this).style("opacity", OPACITY.NODE_DEFAULT).select(
					"circle").style("fill", function(d) {
				return d.color;
			});

			node.filter(function(d) {
				return d.ancestors.indexOf(g) >= 0;
			}).style("opacity", OPACITY.NODE_DEFAULT).select("rect").style(
					"fill", function(d) {
						return d.color;
					});
		}
	});

	collapser.exit().remove();

}

var exampleNodes = [ {
	"type" : "Asset",
	"id" : "a",
	"parent" : null,
	"name" : "Assets"
}, {
	"type" : "Asset",
	"id" : 1,
	"parent" : "a",
	"number" : "101",
	"name" : "Cash"
}, {
	"type" : "Asset",
	"id" : 2,
	"parent" : "a",
	"number" : "120",
	"name" : "Accounts Receivable"
}, {
	"type" : "Asset",
	"id" : 3,
	"parent" : "a",
	"number" : "140",
	"name" : "Merchandise Inventory"
}, {
	"type" : "Asset",
	"id" : 4,
	"parent" : "a",
	"number" : "150",
	"name" : "Supplies"
}, {
	"type" : "Asset",
	"id" : 5,
	"parent" : "a",
	"number" : "160",
	"name" : "Prepaid Insurance"
}, {
	"type" : "Asset",
	"id" : 6,
	"parent" : "a",
	"number" : "170",
	"name" : "Land"
}, {
	"type" : "Asset",
	"id" : 7,
	"parent" : "a",
	"number" : "175",
	"name" : "Buildings"
}, {
	"type" : "Asset",
	"id" : 8,
	"parent" : "a",
	"number" : "178",
	"name" : "Acc. Depreciation Buildings"
}, {
	"type" : "Asset",
	"id" : 9,
	"parent" : "a",
	"number" : "180",
	"name" : "Equipment"
}, {
	"type" : "Asset",
	"id" : 10,
	"parent" : "a",
	"number" : "188",
	"name" : "Acc. Depreciation Equipment"
}, {
	"type" : "Liability",
	"id" : "l",
	"parent" : null,
	"number" : "l",
	"name" : "Liabilities"
}, {
	"type" : "Liability",
	"id" : 11,
	"parent" : "l",
	"number" : "210",
	"name" : "Notes Payable"
}, {
	"type" : "Liability",
	"id" : 12,
	"parent" : "l",
	"number" : "215",
	"name" : "Accounts Payable"
}, {
	"type" : "Liability",
	"id" : 13,
	"parent" : "l",
	"number" : "220",
	"name" : "Wages Payable"
}, {
	"type" : "Liability",
	"id" : 14,
	"parent" : "l",
	"number" : "230",
	"name" : "Interest Payable"
}, {
	"type" : "Liability",
	"id" : 15,
	"parent" : "l",
	"number" : "240",
	"name" : "Unearned Revenues"
}, {
	"type" : "Liability",
	"id" : 16,
	"parent" : "l",
	"number" : "250",
	"name" : "Mortage Loan Payable"
}, {
	"type" : "Equity",
	"id" : "eq",
	"parent" : null,
	"number" : "eq",
	"name" : "Equity"
}, {
	"type" : "Revenue",
	"id" : "r",
	"parent" : null,
	"number" : "r",
	"name" : "Revenues"
}, {
	"type" : "Revenue",
	"id" : "or",
	"parent" : "r",
	"number" : "",
	"name" : "Operating Revenue"
}, {
	"type" : "Revenue",
	"id" : 17,
	"parent" : "or",
	"number" : "310",
	"name" : "Service Revenues"
}, {
	"type" : "Revenue",
	"id" : "nor",
	"parent" : "r",
	"number" : "",
	"name" : "Non-Operating Revenue"
}, {
	"type" : "Revenue",
	"id" : 18,
	"parent" : "nor",
	"number" : "810",
	"name" : "Interest Revenues"
}, {
	"type" : "Revenue",
	"id" : 19,
	"parent" : "nor",
	"number" : "910",
	"name" : "Asset Sale Gain"
}, {
	"type" : "Revenue",
	"id" : 20,
	"parent" : "nor",
	"number" : "960",
	"name" : "Asset Sale Loss"
}, {
	"type" : "Expense",
	"id" : "ex",
	"parent" : null,
	"number" : "ex",
	"name" : "Expenses"
}, {
	"type" : "Expense",
	"id" : 21,
	"parent" : "ex",
	"number" : "500",
	"name" : "Salaries Expense"
}, {
	"type" : "Expense",
	"id" : 22,
	"parent" : "ex",
	"number" : "510",
	"name" : "Wages Expense"
}, {
	"type" : "Expense",
	"id" : 23,
	"parent" : "ex",
	"number" : "540",
	"name" : "Supplies Expense"
}, {
	"type" : "Expense",
	"id" : 24,
	"parent" : "ex",
	"number" : "560",
	"name" : "Rent Expense"
}, {
	"type" : "Expense",
	"id" : 25,
	"parent" : "ex",
	"number" : "570",
	"name" : "Utilities Expense"
}, {
	"type" : "Expense",
	"id" : 26,
	"parent" : "ex",
	"number" : "576",
	"name" : "Telephone Expense"
}, {
	"type" : "Expense",
	"id" : 27,
	"parent" : "ex",
	"number" : "610",
	"name" : "Advertising Expense"
}, {
	"type" : "Expense",
	"id" : 28,
	"parent" : "ex",
	"number" : "750",
	"name" : "Depreciation Expense"
} ]

var exampleLinks = [ {
	"source" : 8,
	"target" : 28,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 17,
	"target" : 18,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 22,
	"target" : 24,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 3,
	"target" : 13,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 24,
	"target" : 24,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 5,
	"target" : 4,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 15,
	"target" : 5,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 18,
	"target" : 8,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 3,
	"target" : 20,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 17,
	"target" : 18,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 22,
	"target" : 5,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 4,
	"target" : 24,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 26,
	"target" : 16,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 27,
	"target" : 6,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 23,
	"target" : 4,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 10,
	"target" : 24,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 17,
	"target" : 16,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 5,
	"target" : 12,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 12,
	"target" : 16,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 19,
	"target" : 5,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 15,
	"target" : 24,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 27,
	"target" : 2,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 26,
	"target" : 28,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 22,
	"target" : 24,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 3,
	"target" : 18,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 18,
	"target" : 5,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 25,
	"target" : 28,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 12,
	"target" : 1,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 28,
	"target" : 21,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 9,
	"target" : 16,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 14,
	"target" : 23,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 6,
	"target" : 1,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 9,
	"target" : 15,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 16,
	"target" : 24,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 22,
	"target" : 28,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 8,
	"target" : 21,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 22,
	"target" : 7,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 18,
	"target" : 10,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : "eq",
	"target" : 1,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 1,
	"target" : 21,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 1,
	"target" : 24,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : 17,
	"target" : 1,
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : Math.ceil(Math.random() * 28),
	"target" : Math.ceil(Math.random() * 28),
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : Math.ceil(Math.random() * 28),
	"target" : Math.ceil(Math.random() * 28),
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : Math.ceil(Math.random() * 28),
	"target" : Math.ceil(Math.random() * 28),
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : Math.ceil(Math.random() * 28),
	"target" : Math.ceil(Math.random() * 28),
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : Math.ceil(Math.random() * 28),
	"target" : Math.ceil(Math.random() * 28),
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : Math.ceil(Math.random() * 28),
	"target" : Math.ceil(Math.random() * 28),
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : Math.ceil(Math.random() * 28),
	"target" : Math.ceil(Math.random() * 28),
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : Math.ceil(Math.random() * 28),
	"target" : Math.ceil(Math.random() * 28),
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : Math.ceil(Math.random() * 28),
	"target" : Math.ceil(Math.random() * 28),
	"value" : Math.floor(Math.random() * 100)
}, {
	"source" : Math.ceil(Math.random() * 28),
	"target" : Math.ceil(Math.random() * 28),
	"value" : Math.floor(Math.random() * 100)
} ]

biHiSankey.nodes(exampleNodes).links(exampleLinks).initializeNodes(
		function(node) {
			node.state = node.parent ? "contained" : "collapsed";
		}).layout(LAYOUT_INTERATIONS);

disableUserInterractions(2 * TRANSITION_DURATION);

update();