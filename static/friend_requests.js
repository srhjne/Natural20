"use strict"


$.get("/friend_request.json", function(result){
	for (var i=0; i<result.length; i++){
		var result0 = result[i]["friendship_id"]
			$("#friend_requests").append("<li>"+ result[i]["friend_name"] + "  <form id="+result0+"> <input id='user_id"+result0+"'' type='hidden' name='friend_id' value='"+result0 +"'> <input class='submit-button' type='submit' id='btn_submit"+result0+"' value='Add Friend'> </form> <div id='request_response"+result0+"'></div>");
			$("#"+result0).on("submit", function (evt2){
				evt2.preventDefault();
				var result0Inner = parseInt(evt2.target.id);
				$.post("/friend_request.json", {"friendship_id": result0Inner}, function (request_result){
					if (request_result[0]){
					$("#request_response"+request_result[0]).html("Added");
					$('#btn_submit'+request_result[0]).attr('disabled',true)
				}
			});
		});
	};
});