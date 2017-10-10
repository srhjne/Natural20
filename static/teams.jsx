"use strict";


class ContentBox extends React.Component {
	constructor(props) {
        super(props);
        this.state = {
            team_members: {},
            teams: [],
            teamname: "",
            friends: []
        };
        this.getTeam = this.getTeam.bind(this);
        this.getTeam(this.state.teamname);
        this.getLeaderboard = this.getLeaderboard.bind(this);
        this.getLeaderboard();
        this.getFriends = this.getFriends.bind(this);
        this.getFriends();
        
    }

    getLeaderboard(){
    	$.get("/get_leaderboard.json", function (result){
    		this.setState({teams: result});
    	}.bind(this));

    }

    getTeam(teamname){
   		$.get("/get_team.json", {teamname: teamname}, function (result){
   			this.setState({team_members:result});

   		}.bind(this));
   		}
    
    getFriends(){
    	$.get("/get_friends.json", function (result){
    		this.setState({friends: result})
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
                        <TeamDetail teamname={this.state.teamname}  team_members={this.state.team_members} friends={this.state.friends}> </TeamDetail>
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
		if (parseInt(user_id) in this.props.friends){
			return true;
		}else {
			return false;
		}
	}

	

	
	render () {
		return (
			<div>
			<h1> Team Detail </h1>
			 {Object.keys(this.props.team_members).map(function(player_id){
                    return <PlayerDetail team_member={this.props.team_members[player_id]} friend={this.isFriend(player_id)}></PlayerDetail>;
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
     
	<h3>{this.props.team_member.username }</h3>
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

ReactDOM.render(
    <ContentBox />,
    document.getElementById("content")
);