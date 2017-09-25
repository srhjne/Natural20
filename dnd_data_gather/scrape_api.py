import requests
from bs4 import BeautifulSoup
import re

# Use DnD api to search for weapon attacks
with open("weapons.dat", "w") as f:
	for i in range(1, 257):
		e = requests.get("http://www.dnd5eapi.co/api/equipment/%d" % i)
		equipment = e.json()
		if equipment["equipment_category"] == "Weapon":
			print equipment["damage"]["dice_count"]
			f.write(equipment["name"]+"|"+equipment["weapon_category:"]+
				    "|"+str(equipment["damage"]["dice_value"])+"|"+
				      str(equipment["damage"]["dice_count"])+"\n")



# Use DnD wiki pages to find all monsters and attacks
monster_page = requests.get("http://www.dandwiki.com/wiki/5e_SRD:Monsters")
with open("monsters.dat", "w") as g:
	with open("attacks.dat", "w") as f:
		cr = None
		creature_index = 0
		monster_soup = BeautifulSoup(monster_page.content, 'html.parser')
		monster_list_section = monster_soup.select("#mw-content-text table")
		#import pdb; pdb.set_trace()
		# for line in monster_list_section[1].get_text().split("\n"):
		# 	if 'class="mw-headline"' in line and "CR" in line:
		# 		cr = line[line.index("CR "):line.index("</")]
		# 		if cr == "CR 0":
		# 			continue
		monster_soup_th = monster_soup.select("th")
		links = monster_soup.find_all('a')
		for i in range(len(links)):
			link = links[i]
			if link.get('href') and link.get('title') and "5e SRD:" in link.get('title') :
				print link
				if ("Homunculus" in link.get('href') or
				   "Lemure" in link.get('href') or
				   "Shrieker" in link.get('href')):
					continue
				# if "<li" in line and "<a href=" in line and cr:
				monster_link = "http://www.dandwiki.com"+ link.get('href')
				monster = requests.get(monster_link)
				soup = BeautifulSoup(monster.content, 'html.parser')
				creature_name = soup.select("h2")[0].get_text()
				columns = soup.select("td")
				paras = columns[1].select("p")
				#import pdb; pdb.set_trace()
				challenge_para = [para.get_text() for para in paras if unicode("Challenge") in para.get_text()]
				cre = re.search("Challenge [0-9/]* ", challenge_para[0])#cp[cp.index("Challenge")+1]
				challenge = challenge_para[0][cre.start()+10:cre.end()]
				#import pdb; pdb.set_trace()
				text_atks = [para.get_text() for para in paras if ("Weapon Attack" in para.get_text()
					                                               and "damage" in para.get_text())]
				
				atk_names = [text_atk.split(" ")[0] for text_atk in text_atks]
				atk_desc = [text_atk[text_atk.index("Hit:")+4:] for text_atk in text_atks]
				atk_dsc_split =[desc.split(" ") for desc in atk_desc]
				for atk in text_atks:
					atk_split = atk.split(" ")
					atk_split = [atk.strip(" ,.\n") for atk in atk_split]
					atk_name = atk_split[0]
					# import pdb; pdb.set_trace()
					dmg_type = atk_split[atk_split.index("damage")-1]
					info_pos = atk_split.index("Hit:")+1
					try:
						avg_dmg = int(atk_split[info_pos])
					except ValueError:
						continue
					if atk_split[info_pos+1].startswith("("):
						dmg_roll = atk_split[info_pos+1].strip("() ")
						dmg_info = dmg_roll.split("d")
						num_dice = int(dmg_info[0])
						type_dice = int(dmg_info[1])
						if atk_split[info_pos+2].startswith("+"):
							dmg_mod = int(atk_split[info_pos+3].strip("),. "))
						else:
							dmg_mod = None
					else:
						num_dice = None
						type_dice = None
						dmg_mod = None
					f.write("%s|%s|%s|%s|%s|%s|%s \n" % (creature_index,atk_name,dmg_type,avg_dmg,num_dice,type_dice,dmg_mod))
				# import pdb; pdb.set_trace()
				g.write("%s | %s | %s \n" % (creature_index, challenge, creature_name))
				creature_index += 1
				if creature_name.strip() == "Pit Fiend":
					break

				




