describe('PlayerLink', () => {
	
	// const friend = false;

	var pl = new PlayerLink({username:"test", friend:true});
	it('Gets the right player link', () =>{
		expect(pl.makeHref()).toBe("/user/test")

	});
	
});

describe('PlayerDetail', () => {

	var pd = new PlayerDetail({team_member:{level:1,xp:10,hp:10, username:"test"}, friend:true});
	it ('Gives right player summary class', () =>{
		expect(pd.render().props.className).toBe("player-overview");
	});

	it ('Displays XP', () =>{
		expect(pd.render().props.children[1].props.children[1].props.children[0].props.children).toBe("XP");
	});

	it ('Displays correct XP', () =>{
		expect(pd.render().props.children[1].props.children[1].props.children[1].props.children).toBe(10);
	});

	it ('Displays HP', () =>{
		expect(pd.render().props.children[1].props.children[2].props.children[0].props.children).toBe("HP");
	});

	it ('Displays correct HP', () =>{
		expect(pd.render().props.children[1].props.children[2].props.children[1].props.children).toBe(10);
	});


});


describe('TeamDetail', () => {

	var leaveTeam= function(){
		return true
	}

	var td = new TeamDetail({teamname: "testTeam", teamname_view: "testTeam" , team_members: {'1':{level:1,xp:10,hp:10, username:"test"}},leaveTeam: leaveTeam, friends: [1]});


	it ('Shows correct team name', () => {
		expect(td.render().props.children[0].props.teamname).toBe("testTeam");


	});


});


describe('NewTeam', () =>{

	var nt = new NewTeam({createTeam:function(){return "Made new team"}})

	it ('Renders new team form', () => {
		expect(nt.render().props.id).toBe("new-team-div")

	});

	it ('Renders new team form title', () => {
		expect(nt.render().props.children[0].props.children).toBe(' Create new team ')

	});

	it ('Renders new team form input box', () => {
		expect(nt.render().props.children[1].props.children[1].props.children.props.children.props.name).toBe("teamname");
		expect(nt.render().props.children[1].props.children[1].props.children.props.children.props.id).toBe("new_teamname");
	});

	it ('Renders new team form submit button', () => {
		expect(nt.render().props.children[1].props.children[2].props.children.props.children.type).toBe("button");
		expect(nt.render().props.children[1].props.children[2].props.children.props.children.props.children).toContain("Create Team");
	});

});


describe("TeamListItem", () => {

	tli = new TeamListItem({team:{teamname: "test_team", avg_xp: "50"}, onClick: function(){return true}});

	it("Shows the correct teamname", () => {
		expect(tli.render().props.children[0].props.children).toBe("test_team")
	});

	it("Shows the correct XP", () => {
		expect(tli.render().props.children[1].props.children).toBe("50")
	});

	it("Makes a button", () => {
		expect(tli.render().props.className).toContain("btn btn-default")

	});



});

describe("TeamList", () => {


	tl = new TeamList({teams:[{teamname:"test_team1"},{teamname:"test_team2"}] });

	it("Shows team list elements", () =>{
		expect(tl.render().props.children[1][0].props.team.teamname).toBe("test_team1");
		expect(tl.render().props.children[1][1].props.team.teamname).toBe("test_team2");


	});

});


describe("Whole page", () => {

	content = new ContentBox();

	it("Renders container div", () => {
		expect(content.render().props.className).toBe("container-fluid");

	});

});


describe('Addition', () => {
  it('knows that 2 and 2 make 4', () => {
    expect(2 + 2).toBe(4);
  });
});


