"use strict";


$.get("/goal_graph.json", function (result){
	if (Object.keys(result).length > 0){
		var data = []
		for (var prop in result){
			var date = [];
			var value = [];
			if (result[prop]["frequency"] === "Daily"){
				for (var day in result[prop]["series"]){
					console.log(day)
					var date_string = result[prop]["series"][day]["date_recorded"].substr(5,15);
					var status_date = new Date(date_string);
					console.log("status_date"+status_date)
					date.push(status_date);
					value.push(result[prop]["series"][day]["value"]);
				}
		
			var trace1 = {
  			x: date,
  			y: value,
  			type: 'bar',
  			name: 'goal progress'
			};
			var valid_from_string = result[prop]["valid_from"];
			var valid_from = new Date(valid_from_string);
			var valid_to_string = result[prop]["valid_to"];
			var valid_to = new Date(valid_to_string);
			var goal_value = result[prop]["value"];
			// data.push(trace1)
			var layout = {
	  		yaxis: {range: [0, goal_value]},
	  		paper_bgcolor: 'rgba(0,0,0,0)',
	  		plot_bgcolor: 'rgba(0,0,0,0)',
	  		margin: {
	    	l: 50,
	    	r: 50,
	    	b: 50,
	    	t: 50,
	    	pad: 10
	  		}, 
	  		title: false
			};

			Plotly.newPlot('graph-div'+prop, [trace1], layout);
			} else {

				for (var j = 0; j<result[prop]["series"].length; j++){
					var date_string = result[prop]["series"][j]["date_recorded"].substr(5,15);
					console.log(result[prop]["series"][j])
					var status_date = new Date(date_string);
					date.push(status_date);
					value.push(result[prop]["series"][j]["value"]);
				}
		
				var trace1 = {
	  			x: date,
	  			y: value,
	  			type: 'scatter',
	  			mode: 'lines',
	  			name: 'goal progress'
				};
				var valid_from_string = result[prop]["valid_from"];
			var valid_from = new Date(valid_from_string);
			var valid_to_string = result[prop]["valid_to"];
			var valid_to = new Date(valid_to_string);
			var goal_value = result[prop]["value"];
			// data.push(trace1)
			var layout = {
	  		xaxis: {range: [valid_from_string, valid_to_string],
	  		type: 'date'},
	  		yaxis: {range: [0, goal_value]},
	  		paper_bgcolor: 'rgba(0,0,0,0)',
	  		plot_bgcolor: 'rgba(0,0,0,0)',
	  		margin: {
	    	l: 50,
	    	r: 50,
	    	b: 50,
	    	t: 50,
	    	pad: 10
	  		}, 
	  		title: false
			};

			Plotly.newPlot('graph-div'+prop, [trace1], layout);
			};

				
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
