from model import UserStatus, db
import random
import datetime

def get_outcome_dict(user):
	
	most_recent_status = user.get_current_status() # this works because I applied ordering in model.py
	goal_list = []

	new_xp = most_recent_status.current_xp
	new_hp = most_recent_status.current_hp

	goals = user.get_unresolved_overdue_goals()
	for goal in goals:
		if goal.frequency != "Daily":
			current_status = goal.get_current_status()
			comp_value = current_status.value
		else:
			comp_value = goal.get_mean_value_daily()
		if comp_value >= goal.value:
			# good things happen
			goal_info_dict = goal.make_goal_info_dictionary()
			goal_info_dict["achieved"] = True
			goal_list.append(goal.make_goal_info_dictionary())
			new_xp += goal.xp
			goal.resolved = "Y"
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

	UserStatus.create_save_updated_status(user=user, new_xp=new_xp, new_hp=new_hp, current_status=most_recent_status)
	return goal_list