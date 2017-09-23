import requests


with open("weapons.dat", "w") as f:
	for i in range(1, 257):
		e = requests.get("http://www.dnd5eapi.co/api/equipment/%d" % i)
		equipment = e.json()
		if equipment["equipment_category"] == "Weapon":
			print equipment["damage"]["dice_count"]
			f.write(equipment["name"]+"|"+equipment["weapon_category:"]+
				    "|"+str(equipment["damage"]["dice_value"])+"|"+
				      str(equipment["damage"]["dice_count"])+"\n")

