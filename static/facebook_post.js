




// $("#test_button").on("click", function(){

var facebook_function = function(quest_string) {
  var FBDesc      = 'My '+quest_string;
  var FBTitle     = 'I am currently battling to complete a quest on Natural 20';
  var FBLink      = 'http://natural20.sarahjaneiom.com';
  var FBPic       = 'http://example.com/img/your-custom-image.jpg';

  FB.ui({
  method: 'share_open_graph',
  action_type: 'og.shares',
  action_properties: JSON.stringify({
                        object: {
                            'og:title': FBTitle,
                            'og:description': FBDesc,
                        	'og:link': FBLink,}})
                            }, function(response){
		console.log("test")
	})
}
// }

  // )
