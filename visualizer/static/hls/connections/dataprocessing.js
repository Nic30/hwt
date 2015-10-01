
function generateLinks(nets){
	var links = [];
	for(var i =0; i < nets.length; i++){
		var net = nets[i];
		for(var i2=0; i2< net.targets.length; i2++){
			var target = net.targets[i2];
			var link = {
					"net": net,
					"source":net.source.id,
					"sourceIndex": net.source.portIndex,
					"target": target.id,
					"targetIndex": target.portIndex};
			links.push(link);
		}
	}
	
	return links;
}

// replaces ID with node object
function resolveNodesInLinks(nodes, links){
	var dict = {};
	for(var i=0; i< nodes.length; i++){
		var n =nodes[i];
		dict[n.id] =n;
	}
	for(var i=0; i< links.length; i++){
		var l = links[i];
		var s = dict[l.source];
		var t = dict[l.target];
		if(s === undefined || t == undefined ){
			throw "Can not resolve link source or target";
		}
		l.source = s;
		l.target = t;
	}	
}

function ReDiscoveredErr(message) { //is exception
	this.name = 'ReDiscoveredErr';
	this.message = message ;
	this.stack = (new Error()).stack;
}
ReDiscoveredErr.prototype = Object.create(Error.prototype);
ReDiscoveredErr.prototype.constructor = ReDiscoveredErr;

// Column container is like an array which allow negative indexing and indexing from most left (and ColumnContainer() is its constructor)
function ColumnContainer(){
	var self = {
			left : [],
			midleRight : [],
			push : function(indx, elm){
				var arr;
				if(indx < 0){
					arr= self.left;
					indx = -indx -1;
				} else {
					arr = self.midleRight;
				}
				if(! arr[indx]){
					arr[indx] = [];
				}
				arr[indx].push(elm); 
				
			},	
			accessFromLeft : function (indx){
				var leftLen = self.left.length;
				if(indx < leftLen){
					return self.left[indx];
				}else{
					return self.midleRight[indx - leftLen];
				}
			},
			length : function() {
				return self.left.length + self.midleRight.length;
			}	
	};
	return self;
}

function components2columns(nodes, links){ // discover component with most ports (bigger) then go on both sides and assign components to columns
	function findBiggestComponent(nodes){ // find component with biggest no of ports
		var biggestComponent = null;
		for(var i =0; i<nodes.length; i++){
			var c = nodes[i];
			if(biggestComponent){
				var portCnt = biggestComponent.inputs.length + biggestComponent.outputs.length;
				var thisCompPortCnt = c.inputs.length + c.outputs.length;
				if(thisCompPortCnt > portCnt)
					biggestComponent = c;
			}else{
				biggestComponent = c;
			}
		}	
		return biggestComponent;
	}
	function constructTriplets(nodes, links){ //for each node discover what is on left and right side
		var triplets = [];
		function Triplet(){ // triplet obj constructor
			return { me: null, left: new Set(), right:new Set()};
		}
		for(var i =0; i<nodes.length; i++){
			var c = nodes[i];
			var t = new Triplet();
			t.me = c;
			for(var i2 =0; i2 < links.length; i2++){
				var l = links[i2];
				if(l.target == c && l.source != c) 
					t.left.add(l.source)
				if(l.source == c && l.target != c)
					t.right.add(l.target)
			}
			triplets.push(t);
		}
		return triplets;
	}

	
	var columns = new ColumnContainer();
	var biggestComponent = findBiggestComponent(nodes);
	var triplets = constructTriplets(nodes, links);

	// now take triplets and build columns out of them
	// go from biggest component on left and right at symetricaly,
	// use set to control if this component was discovered
	var discovered = new Set();
	function popTriplet( component){
		if(discovered.has(component))
			throw new ReDiscoveredErr();
		
		for(var index =0;index< triplets.length; index++ ){
			if(triplets[index].me == component)
				break;
		}
		if(index == triplets.length)
			throw "this component is not in triplets"
		var triplet = triplets[index];
		triplets.splice(index, 1);
		discovered.add(triplet.me);
		return triplet;
	}
	
	function makeColumns(baseIndx, triplet){
		function discoverSide(sideSet, indxShift){
			sideSet.forEach(function (c) {
				try {
					makeColumns(baseIndx+indxShift, popTriplet(c));
				} catch (e){
					if (e instanceof ReDiscoveredErr) {
					//	console.log("found same " +c.name )
					}else 
						throw e;
				}
			});	
		}
		discoverSide(triplet.left, -1);
		discoverSide(triplet.right, 1);

		columns.push(baseIndx, triplet.me);
	}
	makeColumns(0, popTriplet(biggestComponent));
	
	function heightOfPrevious(column, myIndx){
		var y =0;
		for(var i =0; i < myIndx; i++ ){
			y+= column[i].height + COMPONENT_PADDING;
		}
		return y;
	}
	
	for(var i=0; i<nodes.length; i++ ){
		var component = nodes[i]; 
		component.width = columnWidth;
		component.height = portHeight*3 + portHeight * Math.max(component.inputs.length, component.outputs.length);
	}
	
	for(var x = 0; x< columns.length(); x++){
		var column = columns.accessFromLeft(x);	
		for(var y =0; y < column.length; y++ ){
			var component = column[y]; 
			console.log(component.name + "\n");
			component.x = (columnWidth +COMPONENT_PADDING)* x;
			component.y = heightOfPrevious(column, y);
		}
	}
}
