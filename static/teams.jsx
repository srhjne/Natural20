"use strict";


class ContentBox extends React.Component {
	constructor(props) {
        super(props);
        this.state = {
            team_members: {},
            teams: [],
            teamname: "",
            teamname_view: "",
            friends: [],
        };
        this.getTeam = this.getTeam.bind(this);
        this.getTeam(this.state.teamname);
        this.setState({teamname: this.state.teamname_view});
        this.getLeaderboard = this.getLeaderboard.bind(this);
        this.getLeaderboard();
        this.getFriends = this.getFriends.bind(this);
        this.getFriends();
        console.log(this.state.friends);
        
    }

    getLeaderboard(){
    	$.get("/get_leaderboard.json", function (result){
    		this.setState({teams: result});
    	}.bind(this));

    }

    getTeam(teamname){
   		$.get("/get_team.json", {teamname: teamname}, function (result){
   			if (result.length !== 0){
   				console.log(result);
	   			this.setState({team_members:result[1]});
	   			this.setState({teamname_view: result[0]});
   			}

   		}.bind(this));
   		}
    
    getFriends(){
    	$.get("/get_friends.json", function (result){
    		console.log("friends json");
    		console.log(result);
    		this.setState({friends: result});
    		console.log("friends state");
    		console.log(this.state.friends);
    	}.bind(this));
    }

     render() {
        return (
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm-3 col-xs-12 teams">
                    	<TeamList teams={this.state.teams} teamChange = {this.getTeam}> </TeamList>
                        
                    </div>
                    <div className="col-sm-9 col-xs-12 my-team">
                        <TeamDetail teamname={this.state.teamname_view}  team_members={this.state.team_members} friends={this.state.friends}> </TeamDetail>
                    </div>
                </div>
            </div>
        );
	}

}

class TeamList extends React.Component {
	constructor(props){
		super(props);
		console.log(this.props);

	}

	teamChanger(teamname){
		this.props.teamChange(teamname);
	}

	render() {
		return (
		<div>
			<h1> Team List </h1>
			{this.props.teams.map(function(team){
                    return <TeamListItem team={team} onClick={this.teamChanger.bind(this,team.teamname)}/>;
                  }.bind(this))}


		</div>
		)
	}
	
}

class TeamListItem extends React.Component {
	constructor(props){
		super(props);
		console.log(this.props);
	}


	render() {
		return (
		<div className="btn btn-default leaderboard-element" onClick={this.props.onClick} >
		<div className="leaderboard-element-name">
		{this.props.team.teamname}

		</div>
		<div className="leaderboard-element-xp">
		{this.props.team.avg_xp}
		</div>
		</div>
		)
	}

}

class TeamDetail extends React.Component {
	constructor(props){
	super(props);
	console.log(this);
	//this.props.getTeam(this.props.teamname);
	this.isFriend = this.isFriend.bind(this);
	}


	isFriend (user_id) {
		if (this.props.friends.includes(parseInt(user_id))){
			
			return true;
		}else {
			
			return false;
		}
	}

	

	
	render () {
		return (
			<div>
			<h1> Team Detail </h1>
			<TeamJoin teamname={this.props.teamname}/>
			 {Object.keys(this.props.team_members).map(function(player_id){
                    return <PlayerDetail player_id ={player_id} team_member={this.props.team_members[player_id]} friend={this.isFriend(player_id)}></PlayerDetail>;
                  }.bind(this))}
			
			
			</div>
			)
	}
}

class PlayerDetail extends React.Component {
	constructor(props){
	super(props)
	
	}

	render (){
	
	return (
	<div className="player-overview">
	<PlayerLink username={this.props.team_member.username} friend={this.props.friend} />
	<table>
	<tr>
	<td>
	Level
	</td>
	<td>
	{this.props.team_member.level}
	</td>
	</tr>
	<tr>
	<td>
	XP
	</td>
	<td>
	{this.props.team_member.xp}
	</td>
	</tr>
	<tr>
	<td>
	HP
	</td>
	<td>
	{this.props.team_member.hp}
	</td>
	</tr>
	</table>
	
	</div> )
	}

}

class PlayerLink extends React.Component {
	constructor(props){
	super(props);
	console.log(this.props);
	this.makeHref = this.makeHref.bind(this);
	}

	makeHref () {
	return "/user/"+this.props.username;
	}

	render (){
	if (this.props.friend){
	return (
	<h3> <a href={this.makeHref()} > {this.props.username} </a> </h3>
	)} else {
	return (
	<h3> {this.props.username} </h3>
	)
	}
	}

}


class TeamJoin extends React.Component {
	constructor(props){
	super(props);
	console.log(this.props);
	}

	render () {
		return (
		<div>
		<h1> {this.props.teamname} </h1>
		</div>
		)

	}

}

ReactDOM.render(
    <ContentBox />,
    document.getElementById("content")
);