from model import Monster, Attack, LevelLookup, User, UserStatus, Goal, GoalStatus
from model import connect_to_db, db
from server import app
import datetime



def load_monsters():
	for line in open("dnd_data_gather/monsters.dat"):
		monster_id, cr_string, name = line.split("|")
		monster_id = int(monster_id.strip())
		cr_string = cr_string.strip()
		if "/" in cr_string:
			numerator, denominator = cr_string.split("/")
			cr = float(numerator)/float(denominator)
		else:
			cr = float(cr_string)
		name = name.strip()

		monster = Monster(monster_id = monster_id, cr=cr, name=name)
		db.session.add(monster)

	db.session.commit()


def load_attacks():
	for line in open("dnd_data_gather/attacks.dat"):
		info = line.split("|")
		monster_id = int(info[0].strip())
		name = info[1].strip()
		damage_type = info[2].strip()
		avg_damage = int(info[3].strip())
		if info[4].strip() != "None":
			num_dice = int(info[4].strip())
		if info[5].strip() != "None":
			type_dice = int(info[5].strip())
		if info[6].strip() != "None":
			dice_modifier = int(info[5].strip())

		attack = Attack(monster_id=monster_id, name=name, damage_type=damage_type,
		                avg_damage=avg_damage, num_dice=num_dice, type_dice=type_dice,
		                dice_modifier=dice_modifier)

		db.session.add(attack)

	db.session.commit()

def load_level_lookup():
	for line in open("dnd_data_gather/levels.dat"):
		xp, level, modifier = line.split("\t")
		# print level, len(level)
		# import pdb; pdb.set_trace()
		xp = int(xp.strip())
		level = int(level.strip())
		min_cr = (level-1.0)/4.0
		max_cr = (level)/4.0
		hp_max = 4+4*level

		level = LevelLookup(level=level, min_cr=min_cr, max_cr=max_cr,
							hit_point_max=hp_max, required_xp=xp)
		db.session.add(level)

	db.session.commit()


def make_first_user():
	username = "ToK"
	email = "sarahjaneiom@gmail.com"
	password = "1234"
	first_user = User(username=username, email=email, password=password)
	db.session.add(first_user)
	db.session.commit()

	user_id = User.query.filter(User.email == email).one().user_id
	goal_type = "Steps"
	valid_from = datetime.datetime.strptime("19-Sep-2017", "%d-%b-%Y")
	valid_to = datetime.datetime.strptime("25-Sep-2017","%d-%b-%Y")
	value = 15000
	xp = 300
	first_goal = Goal(user_id=user_id, goal_type=goal_type,valid_to=valid_to, 
					  valid_from=valid_from, value=value, xp=xp)
	db.session.add(first_goal)
	db.session.commit()


	goal_id = Goal.query.filter(Goal.user_id == user_id, Goal.goal_type == "Steps").one().goal_id
	date_recorded = datetime.datetime.strptime("24-Sep-2017","%d-%b-%Y")
	value = 1000
	first_status = GoalStatus(date_recorded=date_recorded, value=value, goal_id=goal_id)
	db.session.add(first_status)
	db.session.commit()


	level=1
	current_xp = 0
	current_hp = 12
	first_user_status = UserStatus(date_recorded=date_recorded,current_hp=current_hp,
								   current_xp=current_xp, level=level, user_id=user_id)
	db.session.add(first_user_status)
	db.session.commit()









if __name__ == "__main__":
    connect_to_db(app)

	# In case tables haven't been created, create them
    db.create_all()

    load_monsters()
    load_attacks()
    load_level_lookup()
    make_first_user()
