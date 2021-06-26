import json
from PIL import Image, ImageDraw, ImageFont
import os
import requests
import sys
import math
import shutil
import datetime
import logging
# TODO:
# Known image issue notice

logging.basicConfig(filename='infographic.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s')

with open('herodata.json', 'r') as hero_file:
    hero_data = json.load(hero_file)
with open('autosave.json', 'r') as player_file:
    player_data = json.load(player_file)
with open('artifactdata.json', 'r') as artifact_file:
    artifact_data = json.load(artifact_file)

stat_lookup_table = {
    'CriticalHitDamagePercent': 'CD%:',
    'CriticalHitChancePercent': 'CC%:',
    'Speed': 'Speed:',
    'EffectivenessPercent': 'Eff:',
    'EffectResistancePercent': 'Res:',
    'Health': 'Health:',
    'HealthPercent': 'Health%:',
    'DefensePercent': 'Def%:',
    'Defense': 'Def:',
    'Attack': 'Attack:',
    'AttackPercent': 'Attack%:'
}

set_lookup = {
    0: {'set':'health', 'size':2},
    1: {'set':'defense', 'size':2},
    2: {'set':'attack', 'size':4},
    3: {'set':'speed', 'size':4},
    4: {'set':'critical', 'size':2},
    5: {'set':'hit', 'size':2},
    6: {'set':'destruction', 'size':4},
    7: {'set':'lifesteal', 'size':4},
    8: {'set':'counter', 'size':4},
    9: {'set':'resistance', 'size':2},
    10: {'set':'unity', 'size':2},
    11: {'set':'rage', 'size':4},
    12: {'set':'immunity', 'size':2},
    13: {'set':'penetration', 'size':2},
    14: {'set':'revenge', 'size':4},
    15: {'set':'injury', 'size':4},
}

rarity_lookup = {
    'Epic':(255, 0, 0),
    'Heroic':(106, 13, 173),
    'Rare':(0, 0, 255),
    'Good':(144,238,144),
    'Normal':(128,128,128)
}

element_lookup = {
    'dark': (183,71,185),
    'earth': (141,208,44),
    'ice': (48,198,255),
    'fire': (230, 67, 50),
    'light': (255, 202, 53)
}

# Image Size
item_set_image = (20,20)

# Order of equipment
equip_list = ['Weapon', 'Helmet', 'Armor', 'Necklace', 'Ring', 'Boots']

def find_character_image_id(name):
    """Return the id for a character on epicsevendb when provided their name """
    for character in hero_data:
        if character == name:
            return hero_data[character]['assets']
    return -1;

def find_character_in_player_data(name):
    """Return the index within the player_data json for a character when provided their name """
    index = 0
    for character in player_data['heroes']:
        if character['name'] == name:
            return index
        index = index + 1
    return -1

def find_artifact_in_artifact_data(name):
    """Return the index within the artifact json for a artifact when provided their name """
    index = 0
    for artifact in artifact_data:
        if artifact == name:
            return index
        index = index + 1
    return -1

def get_character_data(name, artifact_name="Demon's Pistol", artifact_level=-1, skill_levels=['?', '?', '?']):
    """Build character data from within the herodata / autosave json, and return a json with relevant data for image"""
    logging.info("Looking for " + name)
    character_data = {}
    for character in hero_data:
        if character == name:
            logging.info('Getting data for ' + character + ' from hero data')
            base_rarity = hero_data[character]['rarity']
            devotion = hero_data[character]['devotion']
            self_devotion = hero_data[character]['self_devotion']
            assets = hero_data[character]['assets']
            db_api_id = hero_data[character]['assets']['thumbnail'].removeprefix(
                'https://assets.epicsevendb.com/_source/face/').removeprefix("https://raw.githubusercontent.com/fribbels/Fribbels-Epic-7-Optimizer/main/data/cachedimages/")[:-6]
            if db_api_id[:44] == 'https://assets.epicsevendb.com/_source/face/':
                source_site="epicsevendb"
            if db_api_id[:43] == 'https://raw.githubusercontent.com/fribbels/':
                source_site="fribbels"

            logging.info('Getting data for ' + character + ' from player data')
            player_data_id = find_character_in_player_data(name)
            atk = player_data['heroes'][player_data_id]['atk']
            hp = player_data['heroes'][player_data_id]['hp']
            defence = player_data['heroes'][player_data_id]['def']
            cr = player_data['heroes'][player_data_id]['cr']
            cd = player_data['heroes'][player_data_id]['cd']
            eff = player_data['heroes'][player_data_id]['eff']
            res = player_data['heroes'][player_data_id]['res']
            dac = player_data['heroes'][player_data_id]['dac']
            spd = player_data['heroes'][player_data_id]['spd']
            ehp = player_data['heroes'][player_data_id]['ehp']
            dmg = player_data['heroes'][player_data_id]['dmg']
            dmgH = player_data['heroes'][player_data_id]['dmgh']
            score = player_data['heroes'][player_data_id]['score']
            hero_class = player_data['heroes'][player_data_id]['role']
            attribute = player_data['heroes'][player_data_id]['attribute']
            # artifact = '0008'
            artifact = artifact_data[artifact_name]
            artifact_image = artifact['assets']['icon']
            if attribute == 'wind':
                attribute = 'earth'
            artifact_id = artifact['assets']['thumbnail'].removeprefix(
                'https://assets.epicsevendb.com/_source/item_arti/art').removeprefix(
                "https://raw.githubusercontent.com/fribbels/Fribbels-Epic-7-Optimizer/main/data/cachedimages/")[:-6]

            cp = player_data['heroes'][player_data_id]['cp']
            equipment = player_data['heroes'][player_data_id]['equipment']
            sets = player_data['heroes'][player_data_id]['sets']
            character_data = {
                'name':name,
                'atk':atk,
                'defence':defence,
                'hp':hp,
                'cr':cr,
                'cd':cd,
                'eff':eff,
                'res':res,
                'dac':dac,
                'spd':spd,
                'ehp':ehp,
                'dmg':dmg,
                'dmgH':dmgH,
                'score':score,
                'hero_class':hero_class,
                'attribute':attribute,
                'cp':cp,
                'equipment':equipment,
                'sets':sets,
                'base_rarity':base_rarity,
                'devotion':devotion,
                'self_devotion':self_devotion,
                'assets':assets,
                'db_api_id':db_api_id,
                'artifact':artifact,
                'artifact_image':artifact_image,
                'artifact_id':artifact_id,
                'artifact_level':artifact_level,
                'skill_levels':skill_levels
                      }
            logging.info("Found " + name)
    if character_data != {}:
        return character_data
    else:
        logging.error("Couldn't find " + name + " in autosave.json")
        raise MissingHeroError("Couldn't find "+name+" in autosave.json. Please verify you have autosave.json in the "
                                    "e7-infographic folder, or that you have the correct character name. "
                                    "Don't forget to use quotes if the name is multiple words!")

class MissingHeroError(Exception):
    """Could not find the hero requested in the data files"""
    pass

class NoHeroError(Exception):
    """Could not find the hero requested in the data files"""
    sys.tracebacklimit = 0
    pass

def confirm_image(filename, url):
    """Check if file exists, if not download from url and save in correct location"""
    logging.info("Confirming if {} exists".format(filename))
    if not os.path.exists(filename):
        logging.info("Downloading {}".format(url))
        r = requests.get(url)
        if r.status_code == 200:
            open(filename, 'wb').write(r.content)
        else:
            shutil.copy('assets/qm.png',filename)
            # open(filename, 'wb').write(broken_image)

def colour_image(img, colour):
    """Replace white-shades with RGB Colour provided"""
    recolour_image_data = []
    img_data = img.getdata()
    # Slow way of doing things for now - finds all pixels that are "white" and changes them to the identified colour
    for item in img_data:
        if item[0] in list(range(190, 256)):
            recolour_image_data.append(colour)
        else:
            recolour_image_data.append(item)
    img.putdata(recolour_image_data)
    return img

def make_character_image(character_data):
    """Build image for a character when provided a character_data json"""
    logging.info('Building image for ' + character_data['name'])

    # Define text/font size
    font_file = 'assets\Fira_Sans_Condensed\FiraSansCondensed-Regular.ttf'
    fnt = ImageFont.truetype(font_file, 12)
    fnt2 = ImageFont.truetype(font_file, 28)
    fnt2small = ImageFont.truetype(font_file, 18)
    fnt2vsmall = ImageFont.truetype(font_file, 14)
    fnt3 = ImageFont.truetype(font_file, 16)
    fnt4 = ImageFont.truetype(font_file, 12)

    # Create base image
    img = Image.new(mode='RGBA', size=(920, 175), color=(33, 37, 41, 255))
    d1 = ImageDraw.Draw(img)

    # Hero image
    hero_image_file = character_data['assets']['thumbnail'].removeprefix('https://assets.epicsevendb.com/_source/face/')
    # print(hero_image_file)
    hero_image_file = hero_image_file.removeprefix('https://raw.githubusercontent.com/fribbels/Fribbels-Epic-7-Optimizer/main/data/cachedimages/')
    hero_image_file = 'images//' + hero_image_file
    confirm_image(hero_image_file, character_data['assets']['thumbnail'])
    im1 = Image.open(hero_image_file).convert("RGBA")
    img.paste(im1, (0, 35), im1)

    # Hero Skill Image Names
    hero_s1_image_file = 'images\\sk_' + character_data['db_api_id'] + '_1.png'
    hero_s2_image_file = 'images\\sk_' + character_data['db_api_id'] + '_2.png'
    hero_s3_image_file = 'images\\sk_' + character_data['db_api_id'] + '_3.png'
    hero_s1_url = 'https://assets.epicsevendb.com/_source/skill/sk_' + character_data['db_api_id'] + '_1.png'
    hero_s2_url = 'https://assets.epicsevendb.com/_source/skill/sk_' + character_data['db_api_id'] + '_2.png'
    hero_s3_url = 'https://assets.epicsevendb.com/_source/skill/sk_' + character_data['db_api_id'] + '_3.png'
    # Verify images are available
    confirm_image(hero_s1_image_file, hero_s1_url)
    confirm_image(hero_s2_image_file, hero_s2_url)
    confirm_image(hero_s3_image_file, hero_s3_url)
    skill_image_list = [hero_s1_image_file, hero_s2_image_file, hero_s3_image_file]

    for index, skill_image in enumerate(skill_image_list):
        im1 = Image.open(skill_image).convert("RGBA")
        im1 = im1.resize((30, 30))
        img.paste(im1, (20+35*index, 140), mask=im1)
        d1.text((30+35*index,130), str(character_data['skill_levels'][index]), font=fnt4, fill=(255, 255, 255))

    # Hero Artifact Images
    hero_artifact_image_file = 'images\\icon_art' + character_data['artifact_id'] + '.png'
    hero_artifact_image_url = character_data['artifact_image']
    confirm_image(hero_artifact_image_file, hero_artifact_image_url)
    im1 = Image.open(hero_artifact_image_file).convert("RGBA")
    im1 = im1.resize((30, 30))
    d1.text((330,135), "Artifact:", font=fnt3, fill=(255, 255, 255))
    img.paste(im1, (390, 129), mask=im1)
    d1.text((400 ,160), str(character_data['artifact_level']), font=fnt4, fill=(255, 255, 255))

    # Hero Name - different size font for longer names
    if len(character_data['name']) < 14:
        d1.text((35, 0), character_data['name'], font=fnt2, fill=(255, 255, 255))
    elif len(character_data['name']) < 20:
        d1.text((35, 10), character_data['name'], font=fnt2small, fill=(255, 255, 255))
    else:
        d1.text((35, 10), character_data['name'], font=fnt2vsmall, fill=(255, 255, 255))

    # Values used for easier adjustment/positioning
    data_height = 15
    start_height = 10
    stat_name_x = 210
    stat_value_x = 290
    panel_width = 150

    # Hero Stat Panel
    d1.text((stat_name_x, start_height), "Atk:", font=fnt, fill=(255, 255, 255))
    d1.text((stat_value_x, start_height), str(character_data['atk']), font=fnt, fill=(255, 255, 255), anchor="ra")
    d1.text((stat_name_x, start_height + 1 * data_height), "Def:", font=fnt, fill=(255, 255, 255))
    d1.text((stat_value_x, start_height + 1 * data_height), str(character_data['defence']), font=fnt, fill=(255, 255, 255) , anchor="ra")
    d1.text((stat_name_x, start_height + 2 * data_height), "HP:", font=fnt, fill=(255, 255, 255))
    d1.text((stat_value_x, start_height + 2 * data_height), str(character_data['hp']), font=fnt, fill=(255, 255, 255), anchor="ra")
    d1.text((stat_name_x, start_height + 3 * data_height), "Spd:", font=fnt, fill=(255, 255, 255))
    d1.text((stat_value_x, start_height + 3 * data_height), str(character_data['spd']), font=fnt, fill=(255, 255, 255), anchor="ra")
    d1.text((stat_name_x, start_height + 4 * data_height), "Crit:", font=fnt, fill=(255, 255, 255))
    d1.text((stat_value_x, start_height + 4 * data_height), str(character_data['cr']) + '%/ ' + str(character_data['cd'])+ '%', font=fnt, fill=(255, 255, 255), anchor="ra")
    d1.text((stat_name_x, start_height + 5 * data_height), "Eff:", font=fnt, fill=(255, 255, 255))
    d1.text((stat_value_x, start_height + 5 * data_height), str(character_data['eff'])+'%', font=fnt, fill=(255, 255, 255), anchor="ra")
    d1.text((stat_name_x, start_height + 6 * data_height), "Res:", font=fnt, fill=(255, 255, 255))
    d1.text((stat_value_x, start_height + 6 * data_height), str(character_data['res'])+'%', font=fnt, fill=(255, 255, 255), anchor="ra")
    d1.text((stat_name_x, start_height + 7 * data_height), "Dual:", font=fnt, fill=(255, 255, 255))
    d1.text((stat_value_x, start_height + 7 * data_height), str(character_data['dac']+5)+'%', font=fnt, fill=(255, 255, 255), anchor="ra")
    # d1.text((stat_name_x+390, start_height + 8.5 * data_height), "CP:", font=fnt3, fill=(255, 255, 255))
    # d1.text((stat_value_x+400, start_height + 8.5 * data_height), str(character_data['cp']), font=fnt3,
    #         fill=(255, 255, 255))


    # WIP Overall Data
    d1.text((430, start_height + 7.25 * data_height + 15), "EHP:", font=fnt3, fill=(255, 255, 255))
    d1.text((470, start_height + 7.25 * data_height + 15), "{:,}".format(character_data['ehp']), font=fnt3,
            fill=(255, 255, 255))
    d1.text((530, start_height + 7.25 * data_height + 15), "DMG:", font=fnt3, fill=(255, 255, 255))
    d1.text((575, start_height + 7.25 * data_height + 15), "{:,}".format(character_data['dmg']), font=fnt3,
             fill=(255, 255, 255))
    d1.text((630, start_height + 7.25 * data_height + 15), "DMGH:", font=fnt3, fill=(255, 255, 255))
    d1.text((675, start_height + 7.25 * data_height + 15), "{:,}".format(character_data['dmgH']), font=fnt3,
            fill=(255, 255, 255))
    d1.text((stat_name_x+520, start_height + 7.25 * data_height + 15), "Total Gearscore:", font=fnt3, fill=(255, 255, 255))
    d1.text((stat_value_x+600, start_height + 7.25 * data_height + 15), str(character_data['score']), font=fnt3, fill=(255, 255, 255), anchor="ra")

    # Identify Hero Sets
    completed_sets = []
    for index, set_num in enumerate(character_data['sets']):
        if set_lookup[index]['size'] <= set_num:
            completed_sets.append('assets\set'+set_lookup[index]['set']+'.png' )
            if set_lookup[index]['size'] * 2 <= set_num:
                completed_sets.append('assets\set' + set_lookup[index]['set'] + '.png')
    # Place Hero Sets
    d1.text((170, start_height + 7.25 * data_height + 25), 'Sets:', font=fnt3, fill=(255, 255, 255))
    for index, set_image in enumerate(completed_sets):
        hero_set_image_x = 205 + index * 30
        hero_set_image_y = 140
        im1 = Image.open(set_image).convert("RGBA")
        im1 = im1.resize((30,30))
        img.paste(im1, ((hero_set_image_x, hero_set_image_y )), mask=im1)

    # Recolour of Class Image with Element
    class_image = 'assets/class'+character_data['hero_class']+'.png'
    im1 = Image.open(class_image).convert("RGBA")
    elemental_colour = element_lookup[character_data['attribute']]
    im1 = colour_image(im1, elemental_colour)

    im1 = im1.resize((30, 30))
    img.paste(im1, (0,3), im1)

    # Item Stat Panels
    item_panel_start_x = 330
    item_panel_start_y = 10
    item_count = 0
    d1.line((item_panel_start_x + 100 * item_count, item_panel_start_y + 1 * data_height,
             item_panel_start_x + 100 * item_count + 700, item_panel_start_y + 1 * data_height))
    d1.line((item_panel_start_x + 100 * item_count, item_panel_start_y + 2.1 * data_height,
             item_panel_start_x + 100 * item_count + 700, item_panel_start_y + 2.1 * data_height))
    d1.line((item_panel_start_x + 100 * item_count, item_panel_start_y + 6.4 * data_height,
             item_panel_start_x + 100 * item_count + 700, item_panel_start_y + 6.4 * data_height))

    for slot in equip_list:
        set_image = ('assets\\' + character_data['equipment'][slot]['set'][-3:] + character_data['equipment'][slot]['set'][:-3] + '.png').lower()
        im1 = Image.open(set_image).convert("RGBA")
        im1 = im1.resize(item_set_image)
        img.paste(im1, (item_panel_start_x + 15 + 100 * item_count + 20, item_panel_start_y-5), im1)
        level = character_data['equipment'][slot]['level']
        enhance = character_data['equipment'][slot]['enhance']
        rarity = character_data['equipment'][slot]['rank']
        rarity_colour = rarity_lookup[rarity]
        slot_name = slot
        main_stat_type = character_data['equipment'][slot]['main']['type']
        main_stat_type = stat_lookup_table[main_stat_type]
        main_stat_value = character_data['equipment'][slot]['main']['value']

        # Equip Slot Images
        slot_image = 'assets\\gear' + slot + '.png'
        im1 = Image.open(slot_image).convert("RGBA")
        # Recolor Equipment Slot Image for Rarity
        im1 = im1.resize((20, 20))
        im1 = colour_image(im1, rarity_colour)
        img.paste(im1, (item_panel_start_x + 15 + 100 * item_count, item_panel_start_y-5), im1)

        # Item Level / Enhancement Level
        d1.text((item_panel_start_x + 100 * item_count, item_panel_start_y), str(level), font=fnt, fill=(255, 255, 255))
        d1.text((item_panel_start_x + 60 + 100 * item_count, item_panel_start_y), '+'+str(enhance), font=fnt, fill=(255, 255, 255))

        # Add % to mainstat string if necessary
        if "Percent" in str(character_data['equipment'][slot]['main']['type']):
            main_stat_value = str(main_stat_value) + '%'

        d1.text((item_panel_start_x + 100 * item_count, item_panel_start_y + 1 * data_height), str(main_stat_type), font=fnt, fill=(255, 255, 255))
        d1.text((item_panel_start_x + 80 + 100 * item_count, item_panel_start_y + 1 * data_height), str(main_stat_value), font=fnt, fill=(255, 255, 255), anchor="ra")

        # Iterate over substats in order
        substat_count = 0
        for substat in character_data['equipment'][slot]['substats']:
            substat_type = stat_lookup_table[substat['type']]
            if 'modified' in substat:
                substat_type = 'Ф'+stat_lookup_table[substat['type']]
            substat_rolls = substat['rolls']
            substat_value = substat['value']
            if "Percent" in str(substat['type']):
                substat_value = str(substat_value)+'%'
            d1.text((item_panel_start_x + 100 * item_count, item_panel_start_y + (2.3 + substat_count) * data_height),
                    str(substat_type), font=fnt, fill=(255, 255, 255))
            d1.text((item_panel_start_x + 80 + 100 * item_count, item_panel_start_y + (2.3 + substat_count) * data_height),
                    str(substat_value), font=fnt, fill=(255, 255, 255), anchor="ra")
            substat_count = substat_count + 1

        d1.text((item_panel_start_x + 100 * item_count, item_panel_start_y + 6.4 * data_height),
            'Gear Score:', font=fnt, fill=(255, 255, 255))
        d1.text((item_panel_start_x + 80 + 100 * item_count, item_panel_start_y + 6.4 * data_height),str(character_data['equipment'][slot]['wss']), font=fnt, fill=(255, 255, 255), anchor="ra")
        item_count = item_count + 1
    return img

def make_multichar(character_list, filename):
    """Iteratively build and stack images using names from character_list and save into filename"""
    img = Image.new(mode='RGBA', size=(920, 175 * (len(character_list))), color=(33, 37, 41))
    logging.info('Building image for ' + str(character_list))
    for index, character  in enumerate(character_list):
        character_data = get_character_data(character)
        temp_image = make_character_image(character_data)
        temp_image.save('output/'+character+'.png')
        img.paste(temp_image, (0, index * 175), temp_image)
    # img.show()
    img.save(filename)

def main(argv):
    # character_list = ['Basar', 'Elphelt', 'Arbiter Vildred', 'Researcher Carrot' ]
    # character_list = ['Cidd', 'Roana', 'Righteous Thief Roozid', 'Mercenary Helga']
    # character_list = ['Cerise', 'Tamarinne', 'Landy', 'Falconer Kluri']
    # character_list = ['Commander Lorina', 'Tamarinne', 'Landy', 'Angelic Montmorancy']
    # character_list = ['Martial Artist Ken', 'Elena', 'Seaside Bellona', 'Charles']
    #character_list = ['Kitty Clarissa']
    character_list = []
    for arg in argv[1:]:
        character_list.append(arg)
    output_time_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    make_multichar(character_list, 'output/multi-'+output_time_name+'.png')


def file_run(filename):
    """Beta processing through json file instead of command line"""
    with open(filename, 'r') as file_input:
        input_data = json.load(file_input)
    img = Image.new(mode='RGBA', size=(920, 175 * (len(input_data))), color=(33, 37, 41))
    index = 0
    for character in input_data:
        # for index, character in enumerate(character_list):
        character_data = get_character_data(character['name'], artifact_level = character['artifact_level'], skill_levels=character['skill_levels'], artifact_name = character['artifact'])
        temp_image = make_character_image(character_data)
        logging.info('Saving {character} image to "{file}"'.format(character = character['name'], file ='output/'+character['name'] + '.png'))
        temp_image.save('output/'+character['name'] + '.png')
        logging.info('Added {character} image to group image'.format(character=character['name']))
        img.paste(temp_image, (0, index * 175), temp_image)
        # img.show()
        index = index + 1

    logging.info('Outputting group image to output/filebased-output.png')
    img.save('output/filebased-output.png')

if __name__ == "__main__":
    logging.info('Starting run')
    if len(sys.argv) > 1:
        if sys.argv[1] == 'file':
            logging.info('Running Alpha file config')
            logging.info(sys.argv)
            file_run(sys.argv[2])
        else:
            logging.info('Running standard command line list')
            logging.info(sys.argv)
            main(sys.argv)
    else:
            logging.info("Couldn't find any character mentions in command line list")
            raise NoHeroError(
                "\ne7-infographic couldn't find any character mentions in your command. \n \n" 
                'Please add the names of any number of characters you want to make an infographic after the executable. Make sure to use quotes for any character names with spaces. For example: e7-infographic "Seaside Bellona" Clarissa "General Purrgis" Sigret')