




$("#test_button").on("click", function(){
  var FBDesc      = 'Come see my quests and join me on the adventure!';
  var FBTitle     = 'I am currently battling to complete a quest on Natural 20';
  var FBLink      = 'http://example.com/your-page-link';
  var FBPic       = 'http://example.com/img/your-custom-image.jpg';

  FB.ui({
  method: 'share_open_graph',
  action_type: 'og.shares',
  action_properties: JSON.stringify({
                        object: {
                            'og:title': FBTitle,
                            'og:description': FBDesc,}})
                            }, function(response){
		console.log("test")
	})})
