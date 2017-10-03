"use strict"


$("#update-email-form").on("submit", function (evt) {
	evt.preventDefault();
	var email = $("#new-email").val();
	var confirm_email = $("#confirm-email").val();
	if (email !== confirm_email){
		alert("Email addresses do not match");
	} else {
		console.log(email)
		$.post("/update_settings.json", {email: email}, function (result){
			if (result) {
				alert("Email address successfully changed");
				$("#current-email").html(" Email address: "+ result['email']);
			};
		});
	};


});


$("#update-password-form").on("submit", function (evt) {
	evt.preventDefault();
	var old_password = $("#old-password").val();
	var password = $("#new-password").val();
	var confirm_password = $("#confirm-password").val();
	if (password !== confirm_password){
		alert("Passwords do not match");
	} else {
		$.post("/update_settings.json", {old_password: old_password, password: password}, function (result){
			if (result) {
				alert("Password successfully changed");
			} else {
				alert("Current password incorrect");
			};
		});
	};


});