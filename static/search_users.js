"use strict";


$("#search_users").on("submit", function (evt) {
	evt.preventDefault();
	$("#user_list").html("");
	$.get("/users.json",{"search_term": $("#username").val()}, function (result){
		for (var i = 0; i<result.length; i++){
			var result0 = result[i][0]
			if (result[i][2]){
				$("#user_list").append("<tr><td><b>"+ result[i][1] + "</b></td><td>Friends </td> </tr>")
			}else if (result[i][3]){
				$("#user_list").append("<tr><td>"+ result[i][1] + " </td><td> <span class='request-sent'> Friend Request Sent </span></td></tr>")
			}else{
				$("#user_list").append("<tr><td>"+ result[i][1] + "</td><td>  <form class='friend-request-button' id="+result0+"> <input id='user_id"+result0+"'' type='hidden' name='friend_id' value='"+result0 +"'> <input type='submit' class='submit-button' id='btn_submit"+result0+"' value='Add Friend'> </form> <span id='request_response"+result0+"'></span></td> </tr>");
				$("#"+result[i][0]).on("submit", function (evt2){
					evt2.preventDefault();
					console.log(evt2.target.id)
					var result0Inner = parseInt(evt2.target.id);
					$.post("/add_friend.json", {"user_id": result0Inner}, function (request_result){
						$("#request_response"+result0Inner).html("Request sent");
						$('#btn_submit'+result0Inner).attr('disabled',true)
					});
				});
			}
		}
	});

	

});


