from model import Monster, Attack
from model import connect_to_db, db
from server import app



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







if __name__ == "__main__":
    connect_to_db(app)

	# In case tables haven't been created, create them
    db.create_all()

    load_monsters()
    load_attacks()
