from model import UserStatus, db, User, Team, UserTeamEffect
import random
import datetime

def get_outcome_dict(user):
	
	most_recent_status = user.get_current_status() # this works because I applied ordering in model.py
	goal_list = []

	new_xp = most_recent_status.current_xp
	new_hp = most_recent_status.current_hp

	num_wins = 0
	num_losses = 0

	goals = user.get_unresolved_overdue_goals()
	print "overdue goals are", goals
	for goal in goals:
		if goal.frequency != "Daily":
			current_status = goal.get_current_status()
			comp_value = current_status.value
		else:
			comp_value = goal.get_mean_value_daily()
		print "my value", comp_value
		print "goal value", goal.value
		if comp_value >= goal.value:
			# good things happen
			print "I am in the good space"
			goal_info_dict = goal.make_goal_info_dictionary()
			goal_info_dict["achieved"] = True
			goal_list.append(goal_info_dict)
			new_xp += goal.xp
			goal.resolved = "Y"
			num_wins +=1
		else:
			# bad things happen
			monster_list = most_recent_status.levellookup.get_suitable_monsters()
			monster = random.choice(monster_list)
			attack = random.choice(monster.attack)
			damage_val = attack.get_damage()
			goal_info_dict = goal.make_goal_info_dictionary()
			goal_info_dict['monster'] = monster.name
			goal_info_dict['attack'] = {"name": attack.name,
						                "damage_type": attack.damage_type,
						                "damage_val": damage_val
						                }
			goal_info_dict["achieved"] = False			                
			goal_list.append(goal_info_dict)
			new_hp -= damage_val

			goal.resolved = "Y"
			num_losses+=1

	UserStatus.create_save_updated_status(user=user, new_xp=new_xp, new_hp=new_hp, current_status=most_recent_status)
	team = user.get_current_team()
	if team:
		for userteam in team.userteam:
			if userteam.user_id == user.user_id:
				continue
			xp_gain = num_wins*20
			hp_loss = num_losses
			ute = UserTeamEffect(user_id=userteam.user_id, teammate_id=user.user_id, xp_gain=xp_gain, hp_loss=hp_loss, resolved=False)
			db.session.add(ute)
			db.session.commit()
			teammate = User.query.get(userteam.user_id)
			teammate_status = teammate.get_current_status()
			teammate_new_xp = teammate_status.current_xp+xp_gain
			teammate_new_hp = teammate_status.current_hp-hp_loss
			UserStatus.create_save_updated_status(user=teammate, new_xp=teammate_new_xp, new_hp=teammate_new_hp, current_status=teammate_status)

	return goal_list


def get_team_rankings(dictionary=False):
	""" returns a list of tuples of form (xp, team)"""
	teams = Team.query.all()
	xp_team = []
	for team in teams:
		team_xp = 0
		print team
		print team.userteam
		team_size = len(team.get_current_team_members())
		if team_size == 0:
			continue
		for user in team.get_current_team_members():
			print user
			print user.get_current_status()
			user_xp = user.get_current_status().current_xp
			team_xp+=user_xp
		if dictionary:
			xp_team.append({"xp":team_xp,"avg_xp": round(team_xp/float(team_size),0), "teamname":team.teamname, "team_id": team.team_id})
		else:
			xp_team.append((team_xp, team))
	if dictionary:
		return sorted(xp_team, key=lambda a: a["avg_xp"], reverse=True)
	else:
		return sorted(xp_team, key=lambda a: a[0], reverse=True)