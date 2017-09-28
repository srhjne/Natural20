"use strict";

console.log("Hello World");



$("#make-stuff-happen").on('click', function () {
	$.get("/outcome.json", function (result) {
		var num_goals = result.length;
		for (var i=0; i<num_goals; i++){
			console.log(result[i]['achieved'], result[i].username)
			if (result[i]['achieved'] === true){
				$("#outcome-text").append("<br>Congratulations you completed your quest and gained "+result[i]['xp'].toString()+" xp");
			} else {
				$('#outcome-text').append("<br>Uh Oh, looks like you failed on your quest. As punishment the evil wizard, Rakshasas Shadowmend, has sent one of his minions after you!");
				$('#outcome-text').append("<br>A "+result[i].monster+" leaps out as you and attacks with his "+ result[i].attack.name+"! You take "+result[i]['attack']['damage_val'].toString()+" "+result[i]['attack']['damage_type']+" damage");
			};
		};
		$("#make-stuff-happen").off();
		$("#go-back").append(
			// "<form action='/user/"+result[0].username+"'><input type='submit' value='Continue on your campaign'></form>"
			"<a class='btn' href='/user/"+result[0].username+"'>Continue with campaign</a>"
			);
	});
});
