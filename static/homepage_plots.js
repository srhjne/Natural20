"use strict";

console.log("Hello World");


$.get("/goal_graph.json", function (result){
	if (Object.keys(result).length > 0){
		var data = []
		for (var prop in result){
			var date = [];
			var value = [];
			for (var j = 0; j<result[prop].length; j++){
				var date_string = result[prop][j][0].substr(5,15);
				var status_date = new Date(date_string)
				date.push(status_date);
				value.push(result[prop][j][1]);
			}
		var trace1 = {
  			x: date,
  			y: value,
  			type: 'scatter'
			};

		data.push(trace1)
				
		}
		Plotly.newPlot('graph-div'+prop, data);	

	}

});

// var trace1 = {
//   x: [1, 2, 3, 4],
//   y: [10, 15, 13, 17],
//   type: 'scatter'
// };

// var trace2 = {
//   x: [1, 2, 3, 4],
//   y: [16, 5, 11, 9],
//   type: 'scatter'
// };

// var data = [trace1, trace2];

// Plotly.newPlot('graph-div', data);
