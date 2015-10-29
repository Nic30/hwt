var App = angular.module('App', []);
/*
 * https://leanpub.com/D3-Tips-and-Tricks/read
 * http://www.d3noob.org/2013/03/d3js-force-directed-graph-examples.html
 * http://blog.pixelingene.com/demos/d3_tree/
 * http://bl.ocks.org/Neilos/584b9a5d44d5fe00f779
 * http://www.jointjs.com/tutorial/ports
 * http://gojs.net/latest/samples/dynamicPorts.html
 * http://bl.ocks.org/GerHobbelt/3104394
 * http://bl.ocks.org/mbostock/3681006    --zoom
 * http://www.codeproject.com/Articles/709340/Implementing-a-Flowchart-with-SVG-and-AngularJS
 * http://www.coppelia.io/2014/07/an-a-to-z-of-extra-features-for-the-d3-force-layout/
 * http://bl.ocks.org/explunit/5603250
 * http://www.ece.northwestern.edu/~haizhou/357/lec6.pdf
 * http://bl.ocks.org/lgersman/5310854                 -- selection 
 * 
 * [TODO][Michal] connection to next left boundary of component to allow router make more straight line for long nets
 * [TODO][Zuzana] find way how to allow temporary disable zoom/moving to allow copy of the text 
 * [TODO][Zuzana] javaskriptova funkce ktera snizi jas a kontrast vsech objektu v svg (vse zasedne, a pak dalsi ukol bude pouzit to se zvyraznovanim...)
 * [TODO][Zuzana] net mouse over style/ net(link) style (chce to i sjednotit nazvoslovi, na net) soucasne spoje jsou moc tenke, neda se na ne najet myssi
 * 				  po najeti stejne nic neni videt protoze ta cervena se strati
 * [TODO][Marek] toolbar 
 * [TODO][Marek] select, multi-select 
 * [TODO][Marek] component edit dialog 
 * [TODO][Zuzana] filebrowser napriklad tento, nebo jakykoli jiny, http://ag-grid.com/example-file-browser/index.php , backend udela Michal
 * [TODO][Marek] add/delete component (prozatim jen predpripraveny json, nebo tak neco bude potreba integrace s filebrowserem)
 * [TODO][Marek] add/delete connection  /construct external port (shortcut), predstava je takova ze kdyz se klikne na sit tak se jakoby nalinkuje na kurzor a kde se klikne tam se pripoji (i vickrat za sebou),
 * 				 zrusi se to pres ESC a pri kliknuti a drzeni napr ctrl se  misto pripojeni vytvori externi port
 *
 * [TODO][All] Stranka s demy
 *
 *
 * Prioritne:
 * 	[Zuzana] filebrowser
 *	[Marek]  postranni panel ze ktereho se bude dat spustit filebrowser, smazat komponenta, pridat komponenta
 *	[Michal] otevreni vybrane veci z filebrowser, predpracovat editace
 *
 * Proc? 
 *  Protoze nemuzeme pohodlne prepinat mezi diagramy, a tak to asi tezko dobre otestujeme....
 *
 */

App.controller('diagramController', function($scope, $http) {

	$scope.redraw = function() {
		$http.get('/hls/connections/data.json').then(
				function(res) {
					var nets = res.data.nets;
					var nodes = res.data.nodes;
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

							maxNamesLen = Math.max(maxNamesLen, nameBlen
									+ nameSlen);
						});

					});
					COLUMN_WIDTH = Math.max(FONT_SIZE * maxNamesLen
							+ INTERNAL_SPACE, COLUMN_WIDTH);

					function findComponent(id){
						var tmp =	nodes.filter(function (node){return node.id == id});
						if(tmp.length == 0)
							throw "component with id " + id + " is not in nodes";
						else if (tmp.lengt >1)
							throw "component with id " + id + " has multiple definitions";
						else
							return tmp[0];
					}
					function findPort(node, portIndex, isOutput){
						if(isOutput){
							var arr =  node.outputs;
						}else{
							var arr =  node.inputs;
						}
						var pi = arr[portIndex];
						if(! pi)
							throw "Component has not port with index:" + portIndex + "( isOutput:"+isOutput+" )"
						return pi;
					}
					function assertPortExists(portItem, isOutput){
						var c = findComponent(portItem.id);
						findPort(c, portItem.portIndex, isOutput);
					}
					
					nets.forEach(function (net){
						assertPortExists(net.source, true);
						net.targets.forEach(function(t){
							assertPortExists(t, false);
						})
					});
					
					var links = generateLinks(nets);
					resolveNodesInLinks(nodes, links);
					components2columns(nodes, links);
					ComponentDiagram("#chartWraper", nodes, links);
				});
	}
	$scope.redraw()
});