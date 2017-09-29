"use strict";


$.get("/goal_graph.json", function (result){
	if (Object.keys(result).length > 0){
		var data = []
		for (var prop in result){
			var date = [];
			var value = [];
			for (var j = 0; j<result[prop]["series"].length; j++){
				var date_string = result[prop]["series"][j][0].substr(5,15);
				var status_date = new Date(date_string);
				date.push(status_date);
				value.push(result[prop]["series"][j][1]);
			}
		var trace1 = {
  			x: date,
  			y: value,
  			type: 'scatter',
  			mode: 'lines'
			};

		var valid_from_string = result[prop]["valid_from"];
		var valid_from = new Date(valid_from_string);
		console.log(valid_from);
		var valid_to_string = result[prop]["valid_to"];
		var valid_to = new Date(valid_to_string);
		console.log(valid_to);
		var goal_value = result[prop]["value"];
		// data.push(trace1)
		var layout = {
  		xaxis: {range: [valid_from_string, valid_to_string],
  		type: 'date'},
  		yaxis: {range: [0, goal_value]}
		};

		Plotly.newPlot('graph-div'+prop, [trace1], layout);		
		};
			

	};

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
