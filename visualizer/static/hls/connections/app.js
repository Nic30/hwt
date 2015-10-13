var links = generateLinks(nets);
resolveNodesInLinks(nodes, links);
components2columns(nodes, links);
redraw(nodes, links);
