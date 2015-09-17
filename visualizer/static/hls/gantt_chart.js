/*
var tasks = [ {
	"start" : 12,
	"end" : 40,
	"taskName" : "E Job",
	"codeRef" : "main.cpp:14"
} ];

var taskNames = [ "D Job", "P Job", "E Job", "A Job", "N Job" ];

 * 
 * */
var taskStatus = {
	"SUCCEEDED" : "bar",
	"FAILED" : "bar-failed",
	"RUNNING" : "bar-running",
	"KILLED" : "bar-killed"
};
var min = 0;
var max = 10;
if (tasks.length > 0) {
	tasks.sort(function(a, b) {
		return a.end - b.end;
	});
	max = tasks[tasks.length - 1].end;
	tasks.sort(function(a, b) {
		return a.start - b.start;
	});
	min = tasks[0].start;
}
var format = "d";
var timeDomainString = "ns";

var gantt = d3.gantt().taskTypes(taskNames).taskStatus(taskStatus).tickFormat(
		format).height(500).width(1700);

gantt.timeDomainMode("fixed");
fitTasks(timeDomainString);

gantt(tasks);

function fitTasks(timeDomainString) {
	this.timeDomainString = timeDomainString;
	/*
	 * format = "%a %H:%M"; gantt.timeDomain([ d3.time.day.offset(getEnd(), -7),
	 * getEnd() ]);
	 */
	gantt.timeDomain([ 0, getEnd() ]);
	gantt.tickFormat(format);
	gantt.redraw(tasks);
}

function getEnd() {
	var lastEnd = 0;
	if (tasks.length > 0) {
		lastEnd = tasks[tasks.length - 1].end;
	}
	return lastEnd;
}

function addTask() {

	var lastEnd = getEnd();
	var taskStatusKeys = Object.keys(taskStatus);
	var taskStatusName = taskStatusKeys[Math.floor(Math.random()
			* taskStatusKeys.length)];
	var taskName = taskNames[Math.floor(Math.random() * taskNames.length)];
	var start = lastEnd + Math.ceil(5 * Math.random());
	var len = Math.ceil(5 * Math.random());
	tasks.push({
		"start" : start,
		"end" : start + len,
		"taskName" : taskName,
		"status" : taskStatusName
	});

	fitTasks(timeDomainString);
	gantt.redraw(tasks);
};

function removeTask() {
	tasks.pop();
	fitTasks(timeDomainString);
	gantt.redraw(tasks);
};