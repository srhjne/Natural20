// import React from 'react';
// import ReactDOM from "react-dom";
"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var ContentBox = function (_React$Component) {
	_inherits(ContentBox, _React$Component);

	function ContentBox(props) {
		_classCallCheck(this, ContentBox);

		var _this = _possibleConstructorReturn(this, (ContentBox.__proto__ || Object.getPrototypeOf(ContentBox)).call(this, props));

		_this.state = {
			team_members: {},
			teams: [],
			teamname: "",
			teamname_view: "",
			friends: [],
			team_requests: []
		};

		_this.getLeaderboard = _this.getLeaderboard.bind(_this);
		_this.getFriends = _this.getFriends.bind(_this);
		_this.getTeam = _this.getTeam.bind(_this);
		_this.leaveTeam = _this.leaveTeam.bind(_this);
		_this.getTeamRequests = _this.getTeamRequests.bind(_this);
		_this.joinTeam = _this.joinTeam.bind(_this);
		_this.createTeam = _this.createTeam.bind(_this);
		console.log(_this.state);

		return _this;
	}

	_createClass(ContentBox, [{
		key: "componentDidMount",
		value: function componentDidMount() {
			this.getLeaderboard();
			this.getFriends();
			this.getTeam(this.state.teamname);
			this.setState({ teamname: this.state.teamname_view });
			this.getTeamRequests();
			console.log("component did mount");
			console.log(this.state);
		}
	}, {
		key: "leaveTeam",
		value: function leaveTeam(teamname) {
			var retVal = confirm("Are you sure you want to leave this team?");
			if (retVal == true) {
				$.post("/leave_team.json", { teamname: teamname }, function (result) {
					if (result) {
						this.setState({ teamname: "" });
						this.getTeam(this.state.teamname);
					}
					console.log("This is leave team");
					console.log(result);
					console.log(this.state);
				}.bind(this));
			}
		}
	}, {
		key: "getLeaderboard",
		value: function getLeaderboard() {
			$.get("/get_leaderboard.json", function (result) {
				this.setState({ teams: result });
			}.bind(this));
		}
	}, {
		key: "getTeam",
		value: function getTeam(teamname) {
			$.get("/get_team.json", { teamname: teamname }, function (result) {
				if (result.length !== 0) {
					console.log(result);
					this.setState({ team_members: result[1] });
					this.setState({ teamname_view: result[0] });
					if (this.state.teamname === teamname) {
						this.setState({ teamname: result[0] });
					}
				}
			}.bind(this));
		}
	}, {
		key: "getFriends",
		value: function getFriends() {
			$.get("/get_friends.json", function (result) {
				console.log("friends json");
				console.log(result);
				this.setState({ friends: result });
				console.log("friends state");
				console.log(this.state.friends);
			}.bind(this));
		}
	}, {
		key: "getTeamRequests",
		value: function getTeamRequests() {
			$.get("/get_team_requests.json", function (result) {
				if (result) {
					this.setState({ team_requests: result });
				}
			}.bind(this));
		}
	}, {
		key: "joinTeam",
		value: function joinTeam(team_request) {
			var retVal = confirm("Joining a new team will cause you to leave your current team. Are you sure you want to leave this team?");
			if (retVal) {
				$.post("/join_team.json", team_request, function (result) {
					console.log(result);
					if (result) {
						console.log("inside jointeam");
						console.log(this);
						this.setState({ teamname: result.teamname });
						this.getTeam(this.state.teamname);
						this.getTeamRequests();
					}
				}.bind(this));
			}
		}
	}, {
		key: "createTeam",
		value: function createTeam() {
			var teamname = $("#new_teamname").val();
			if (teamname === "") {
				alert("You need to fill in a team name");
			} else {
				var retVal = confirm("Forming a new team will cause you to leave your current team. Are you sure you want to leave this team?");
				if (retVal) {
					console.log("new teamname is " + teamname);
					$.post("/make_new_team.json", { teamname: teamname }, function (result) {
						console.log(result);
						console.log("testing");
						if (result) {
							this.setState({ teamname: result["teamname"] });
							this.getTeam(this.state.teamname);
							this.getLeaderboard();
						} else {
							alert("That team name is already taken");
						}
					}.bind(this));
				}
			}
		}
	}, {
		key: "render",
		value: function render() {
			return React.createElement(
				"div",
				{ className: "container-fluid" },
				React.createElement(
					"div",
					{ className: "row" },
					React.createElement(
						"div",
						{ className: "col-sm-3 col-xs-12 teams" },
						React.createElement(
							TeamList,
							{ teams: this.state.teams, teamChange: this.getTeam },
							" "
						),
						React.createElement(NewTeam, { createTeam: this.createTeam })
					),
					React.createElement(
						"div",
						{ className: "col-sm-9 col-xs-12 my-team" },
						React.createElement(
							"h1",
							null,
							" Team Detail "
						),
						this.state.team_requests.map(function (team_request) {
							return React.createElement(TeamRequest, { team_request: team_request, joinTeam: this.joinTeam.bind(this, team_request) });
						}.bind(this)),
						React.createElement(
							TeamDetail,
							{ teamname: this.state.teamname,
								teamname_view: this.state.teamname_view, team_members: this.state.team_members, friends: this.state.friends, leaveTeam: this.leaveTeam.bind(this, this.state.teamname) },
							" "
						)
					)
				)
			);
		}
	}]);

	return ContentBox;
}(React.Component);

var NewTeam = function (_React$Component2) {
	_inherits(NewTeam, _React$Component2);

	function NewTeam(props) {
		_classCallCheck(this, NewTeam);

		return _possibleConstructorReturn(this, (NewTeam.__proto__ || Object.getPrototypeOf(NewTeam)).call(this, props));
	}

	_createClass(NewTeam, [{
		key: "render",
		value: function render() {
			return React.createElement(
				"div",
				{ id: "new-team-div" },
				React.createElement(
					"h1",
					null,
					" Create new team "
				),
				React.createElement(
					"table",
					null,
					React.createElement(
						"tr",
						null,
						React.createElement(
							"td",
							null,
							"Team name"
						)
					),
					React.createElement(
						"tr",
						null,
						React.createElement(
							"td",
							null,
							React.createElement("input", { id: "new_teamname", type: "text", name: "teamname" })
						)
					),
					React.createElement(
						"tr",
						null,
						React.createElement(
							"td",
							null,
							React.createElement(
								"button",
								{ onClick: this.props.createTeam },
								" Create Team "
							)
						)
					)
				)
			);
		}
	}]);

	return NewTeam;
}(React.Component);

var TeamRequest = function (_React$Component3) {
	_inherits(TeamRequest, _React$Component3);

	function TeamRequest(props) {
		_classCallCheck(this, TeamRequest);

		var _this3 = _possibleConstructorReturn(this, (TeamRequest.__proto__ || Object.getPrototypeOf(TeamRequest)).call(this, props));

		console.log(_this3.props);

		return _this3;
	}

	_createClass(TeamRequest, [{
		key: "render",
		value: function render() {

			return React.createElement(
				"div",
				null,
				"Stories of your adventuring have reached across the kingdom",
				React.createElement("br", null),
				React.createElement("br", null),
				this.props.team_request.inviter_name,
				" wants you to join the ",
				this.props.team_request.teamname,
				" Guild",
				React.createElement(
					"button",
					{ className: "btn btn-default", onClick: this.props.joinTeam },
					"Join team "
				)
			);
		}
	}]);

	return TeamRequest;
}(React.Component);

var TeamList = function (_React$Component4) {
	_inherits(TeamList, _React$Component4);

	function TeamList(props) {
		_classCallCheck(this, TeamList);

		var _this4 = _possibleConstructorReturn(this, (TeamList.__proto__ || Object.getPrototypeOf(TeamList)).call(this, props));

		console.log(_this4.props);

		return _this4;
	}

	_createClass(TeamList, [{
		key: "teamChanger",
		value: function teamChanger(teamname) {
			this.props.teamChange(teamname);
		}
	}, {
		key: "render",
		value: function render() {
			return React.createElement(
				"div",
				null,
				React.createElement(
					"h1",
					null,
					" Team List "
				),
				this.props.teams.map(function (team) {
					return React.createElement(TeamListItem, { team: team, onClick: this.teamChanger.bind(this, team.teamname) });
				}.bind(this))
			);
		}
	}]);

	return TeamList;
}(React.Component);

var TeamListItem = function (_React$Component5) {
	_inherits(TeamListItem, _React$Component5);

	function TeamListItem(props) {
		_classCallCheck(this, TeamListItem);

		var _this5 = _possibleConstructorReturn(this, (TeamListItem.__proto__ || Object.getPrototypeOf(TeamListItem)).call(this, props));

		console.log(_this5.props);
		return _this5;
	}

	_createClass(TeamListItem, [{
		key: "render",
		value: function render() {
			return React.createElement(
				"div",
				{ className: "btn btn-default leaderboard-element", onClick: this.props.onClick },
				React.createElement(
					"div",
					{ className: "leaderboard-element-name" },
					this.props.team.teamname
				),
				React.createElement(
					"div",
					{ className: "leaderboard-element-xp" },
					this.props.team.avg_xp
				)
			);
		}
	}]);

	return TeamListItem;
}(React.Component);

var TeamDetail = function (_React$Component6) {
	_inherits(TeamDetail, _React$Component6);

	function TeamDetail(props) {
		_classCallCheck(this, TeamDetail);

		var _this6 = _possibleConstructorReturn(this, (TeamDetail.__proto__ || Object.getPrototypeOf(TeamDetail)).call(this, props));

		console.log(_this6);
		//this.props.getTeam(this.props.teamname);
		_this6.isFriend = _this6.isFriend.bind(_this6);
		return _this6;
	}

	_createClass(TeamDetail, [{
		key: "isFriend",
		value: function isFriend(username) {
			if (this.props.friends.includes(username)) {

				return true;
			} else {

				return false;
			}
		}
	}, {
		key: "render",
		value: function render() {
			return React.createElement(
				"div",
				null,
				React.createElement(TeamJoin, { teamname: this.props.teamname, teamname_view: this.props.teamname_view, leaveTeam: this.props.leaveTeam, friends: this.props.friends }),
				Object.keys(this.props.team_members).map(function (player_id) {
					return React.createElement(PlayerDetail, { player_id: player_id, team_member: this.props.team_members[player_id], friend: this.isFriend(this.props.team_members[player_id]['username']) });
				}.bind(this))
			);
		}
	}]);

	return TeamDetail;
}(React.Component);

var PlayerDetail = function (_React$Component7) {
	_inherits(PlayerDetail, _React$Component7);

	function PlayerDetail(props) {
		_classCallCheck(this, PlayerDetail);

		return _possibleConstructorReturn(this, (PlayerDetail.__proto__ || Object.getPrototypeOf(PlayerDetail)).call(this, props));
	}

	_createClass(PlayerDetail, [{
		key: "render",
		value: function render() {

			return React.createElement(
				"div",
				{ className: "player-overview" },
				React.createElement(PlayerLink, { username: this.props.team_member.username, friend: this.props.friend }),
				React.createElement(
					"table",
					null,
					React.createElement(
						"tr",
						null,
						React.createElement(
							"td",
							null,
							"Level"
						),
						React.createElement(
							"td",
							null,
							this.props.team_member.level
						)
					),
					React.createElement(
						"tr",
						null,
						React.createElement(
							"td",
							null,
							"XP"
						),
						React.createElement(
							"td",
							null,
							this.props.team_member.xp
						)
					),
					React.createElement(
						"tr",
						null,
						React.createElement(
							"td",
							null,
							"HP"
						),
						React.createElement(
							"td",
							null,
							this.props.team_member.hp
						)
					)
				)
			);
		}
	}]);

	return PlayerDetail;
}(React.Component);

var PlayerLink = function (_React$Component8) {
	_inherits(PlayerLink, _React$Component8);

	function PlayerLink(props) {
		_classCallCheck(this, PlayerLink);

		var _this8 = _possibleConstructorReturn(this, (PlayerLink.__proto__ || Object.getPrototypeOf(PlayerLink)).call(this, props));

		console.log(_this8.props);
		_this8.makeHref = _this8.makeHref.bind(_this8);
		return _this8;
	}

	_createClass(PlayerLink, [{
		key: "makeHref",
		value: function makeHref() {
			return "/user/" + this.props.username;
		}
	}, {
		key: "render",
		value: function render() {
			if (this.props.friend) {
				return React.createElement(
					"h3",
					{ className: "team_name" },
					" ",
					React.createElement(
						"a",
						{ href: this.makeHref() },
						" ",
						this.props.username,
						" "
					),
					" "
				);
			} else {
				return React.createElement(
					"h3",
					{ className: "team_name" },
					" ",
					this.props.username,
					" "
				);
			}
		}
	}]);

	return PlayerLink;
}(React.Component);

var TeamJoin = function (_React$Component9) {
	_inherits(TeamJoin, _React$Component9);

	function TeamJoin(props) {
		_classCallCheck(this, TeamJoin);

		var _this9 = _possibleConstructorReturn(this, (TeamJoin.__proto__ || Object.getPrototypeOf(TeamJoin)).call(this, props));

		console.log(_this9.props);
		return _this9;
	}

	_createClass(TeamJoin, [{
		key: "inviteFriend",
		value: function inviteFriend(friendname) {
			console.log("friendname is" + friendname);
			$.post("/invite_friend.json", { friendname: friendname }, function (result) {
				if (result) {
					$("#addfriendModal").html("<p>" + result + "</p>");
				}
			});
		}
	}, {
		key: "render",
		value: function render() {
			if (this.props.teamname !== this.props.teamname_view) {
				return React.createElement(
					"div",
					null,
					React.createElement(
						"h1",
						null,
						" ",
						this.props.teamname_view,
						" "
					)
				);
			} else if (this.props.teamname !== "") {
				return React.createElement(
					"div",
					null,
					React.createElement(
						"h1",
						null,
						" ",
						this.props.teamname_view,
						" "
					),
					React.createElement(
						"div",
						{ className: "btn btn-default", onClick: this.props.leaveTeam },
						"Leave Team"
					),
					React.createElement(
						"a",
						{ href: "#myModal", role: "button", className: "btn btn-large btn-primary", "data-toggle": "modal" },
						"Invite Friends"
					),
					React.createElement(
						"div",
						{ id: "myModal", className: "modal fade" },
						React.createElement(
							"div",
							{ className: "modal-dialog" },
							React.createElement(
								"div",
								{ className: "modal-content" },
								React.createElement(
									"div",
									{ className: "modal-header" },
									React.createElement(
										"button",
										{ type: "button", "class": "close", "data-dismiss": "modal", "aria-hidden": "true" },
										"\xD7"
									),
									React.createElement(
										"h4",
										{ className: "modal-title" },
										"Add Friends"
									)
								),
								React.createElement(
									"div",
									{ className: "modal-body" },
									this.props.friends.map(function (friendname) {
										return React.createElement(
											"button",
											{ type: "button", className: "btn btn-primary", onClick: this.inviteFriend.bind(this, friendname) },
											friendname
										);
									}.bind(this)),
									React.createElement("div", { id: "addfriendModal" })
								)
							)
						)
					)
				);
			} else return null;
		}
	}]);

	return TeamJoin;
}(React.Component);

ReactDOM.render(React.createElement(ContentBox, null), document.getElementById("content"));

