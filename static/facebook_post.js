



$("#test_button").on("click", function(){FB.ui({
  method: 'feed',
  link: 'https://developers.facebook.com/docs/',
  caption: 'An example caption',
	}, function(response){
		console.log("test")
	})})
