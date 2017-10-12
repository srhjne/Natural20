// import React from 'react';
// import ReactDOM from "react-dom";
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
            team_requests: []
        };
        
        this.getLeaderboard = this.getLeaderboard.bind(this);
        this.getFriends = this.getFriends.bind(this);
        this.getTeam = this.getTeam.bind(this);
        this.leaveTeam = this.leaveTeam.bind(this);
        this.getTeamRequests = this.getTeamRequests.bind(this);
        this.joinTeam = this.joinTeam.bind(this);
        this.createTeam = this.createTeam.bind(this);
        console.log(this.state);
        
    }


    componentDidMount(){
    	this.getLeaderboard();
    	this.getFriends();
        this.getTeam(this.state.teamname);
        this.setState({teamname: this.state.teamname_view});
        this.getTeamRequests();
        console.log("component did mount");
        console.log(this.state);
    }

    leaveTeam(teamname){
    	var retVal = confirm("Are you sure you want to leave this team?");
    	if (retVal == true){
			$.post("/leave_team.json",{teamname: teamname},function(result){
				if (result){
					this.setState({teamname:""})
					this.getTeam(this.state.teamname)
				}
				console.log("This is leave team")
				console.log(result);
				console.log(this.state);

			}.bind(this));
		}
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
	   			if (this.state.teamname === teamname) {
	   				this.setState({teamname: result[0]});
	   			}
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

    getTeamRequests(){
    	$.get("/get_team_requests.json", function (result){
    		if (result){
    			this.setState({team_requests: result});
    		}
    	}.bind(this))
    }

    joinTeam(team_request){
		var retVal = confirm("Joining a new team will cause you to leave your current team. Are you sure you want to leave this team?");
		if (retVal){
			$.post("/join_team.json",team_request, function(result){
				console.log(result);
				if (result) {
					console.log("inside jointeam");
					console.log(this);
					this.setState({teamname:result.teamname});
					this.getTeam(this.state.teamname);
					this.getTeamRequests();
				} 

			}.bind(this));
		}
		
	}


	createTeam(){
		var teamname = $("#new_teamname").val();
		if (teamname === "") {
			alert("You need to fill in a team name")
		} else {
			var retVal = confirm("Forming a new team will cause you to leave your current team. Are you sure you want to leave this team?");
			if (retVal){
				console.log("new teamname is "+teamname);
				$.post("/make_new_team.json", {teamname: teamname}, function (result){
					console.log(result);
					console.log("testing");
					if (result){
						this.setState({teamname: result["teamname"]});
						this.getTeam(this.state.teamname);
						this.getLeaderboard();
					} else {
						alert("That team name is already taken")
					}
				}.bind(this))

			}
		}
		
	}

     render() {
        return (
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm-3 col-xs-12 teams">
                    	<TeamList teams={this.state.teams} teamChange = {this.getTeam}> </TeamList>
                        <NewTeam createTeam = {this.createTeam}/>
                    </div>
                    <div className="col-sm-9 col-xs-12 my-team">
                    <h1> Team Detail </h1>
                    {this.state.team_requests.map(function(team_request){
                    	return <TeamRequest team_request={team_request} joinTeam={this.joinTeam.bind(this,team_request)}/>
                    }.bind(this))}
                    	
                        <TeamDetail teamname={this.state.teamname}
                        teamname_view={this.state.teamname_view}  team_members={this.state.team_members} friends={this.state.friends} leaveTeam={this.leaveTeam.bind(this, this.state.teamname)}> </TeamDetail>
                    </div>
                </div>
            </div>
        );
	}

}

class NewTeam extends React.Component {
	constructor(props){
		super(props);

	}

	render(){
		return (
			<div id="new-team-div">
			<h1> Create new team </h1>
			
			<table>
			<tr>
			<td>
			Team name  
			</td>
			</tr>
			<tr>

			<td>
			 <input id="new_teamname" type="text" name="teamname"/>
			</td>
			</tr>
			<tr>
			<td>
			<button onClick={this.props.createTeam} > Create Team </button>
			</td>
			</tr>
			</table>
			
			</div>
			)
	}
}


class TeamRequest extends React.Component {
	constructor(props){
		super(props);
		console.log(this.props);

	}



	render (){
		
		return (
			<div>
			Stories of your adventuring have reached across the kingdom
			<br/>
			<br/>
			{this.props.team_request.inviter_name} wants you to join the {this.props.team_request.teamname} Guild
			<button className="btn btn-default" onClick={this.props.joinTeam}>Join team </button>
			</div>
			)
		
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


	isFriend (username) {
		if (this.props.friends.includes(username)){
			
			return true;
		}else {
			
			return false;
		}
	}

	

	
	render () {
		return (
			<div>
			
			<TeamJoin teamname={this.props.teamname} teamname_view={this.props.teamname_view} leaveTeam={this.props.leaveTeam} friends={this.props.friends}/>
			 {Object.keys(this.props.team_members).map(function(player_id){
                    return <PlayerDetail player_id ={player_id} team_member={this.props.team_members[player_id]} friend={this.isFriend(this.props.team_members[player_id]['username'])}></PlayerDetail>;
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
	<h3 className="team_name"> <a href={this.makeHref()} > {this.props.username} </a> </h3>
	)} else {
	return (
	<h3 className="team_name"> {this.props.username} </h3>
	)
	}
	}

}


class TeamJoin extends React.Component {
	constructor(props){
	super(props);
	console.log(this.props);
	}

	inviteFriend(friendname){
		console.log("friendname is"+friendname);
		$.post("/invite_friend.json", {friendname: friendname}, function(result){
			if (result){
				$("#addfriendModal").html("<p>"+result+"</p>");
			}
		});
	}

	
	render () {
		if (this.props.teamname !== this.props.teamname_view) {
			return (
				<div>
				<h1> {this.props.teamname_view} </h1>
				</div>
			)
		}
		else if (this.props.teamname !== "" ){
			return (
				<div>
				<h1> {this.props.teamname_view} </h1>
				<div className="btn btn-default" onClick={this.props.leaveTeam}>
					Leave Team
				</div>
				
				<a href="#myModal" role="button" className="btn btn-large btn-primary" data-toggle="modal">Invite Friends</a>
				<div id="myModal" className="modal fade">

    			<div className="modal-dialog">

				        <div className="modal-content">

				            <div className="modal-header">

				                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>

				                <h4 className="modal-title">Add Friends</h4>

				            </div>

				            <div  className="modal-body">

				            {this.props.friends.map( function(friendname){
				            	return <button type="button" className="btn btn-primary" onClick={this.inviteFriend.bind(this,friendname)}>{friendname}</button>
				            }.bind(this))
				        	}
				            	
				            <div id="addfriendModal">

				            </div>  
				            </div>

				        </div>

				    </div>

				</div>
			</div>
			)
		} else return null; 
	}

}



ReactDOM.render(
    <ContentBox />,
    document.getElementById("content")
);