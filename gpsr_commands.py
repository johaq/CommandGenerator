import random
import re
import itertools
import warnings


class CommandGenerator:

    def __init__(self, person_names, location_names, placement_location_names, room_names, object_names,
                 object_categories_plural, object_categories_singular):
        self.person_names = person_names
        self.location_names = location_names
        self.placement_location_names = placement_location_names
        self.room_names = room_names
        self.object_names = object_names
        self.object_categories_plural = object_categories_plural
        self.object_categories_singular = object_categories_singular

    verb_dict = {
        "take": ["take", "get", "grasp", "fetch"],
        "place": ["put", "place"],
        "deliver": ["bring", "give", "deliver"],
        "bring": ["bring", "give"],
        "go": ["go", "navigate"],
        "find": ["find", "locate", "look for"],
        "talk": ["tell", "say"],
        "answer": ["answer"],
        "meet": ["meet"],
        "tell": ["tell"],
        "greet": ["greet", "salute", "say hello to", "introduce yourself to"],
        "remember": ["meet", "contact", "get to know", "get acquainted with"],
        "count": ["tell me how many"],
        "describe": ["tell me how", "describe"],
        "offer": ["offer"],
        "follow": ["follow"],
        "guide": ["guide", "escort", "take", "lead"],
        "accompany": ["accompany"]
    }

    prep_dict = {
        "deliverPrep": ["to"],
        "placePrep": ["on"],
        "inLocPrep": ["in"],
        "fromLocPrep": ["from"],
        "toLocPrep": ["to"],
        "atLocPrep": ["at"],
        "talkPrep": ["to"],
        "locPrep": ["in", "at"],
        "onLocPrep": ["on"],
        "arePrep": ["are"],
        "ofPrsPrep": ["of"]
    }

    connector_list = ["and"]
    gesture_person_list = ["waving person", "person raising their left arm", "person raising their right arm",
                           "person pointing to the left", "person pointing to the right"]
    pose_person_list = ["sitting person", "standing person", "lying person"]
    # Ugly...
    gesture_person_plural_list = ["waving persons", "persons raising their left arm", "persons raising their right arm",
                                  "persons pointing to the left", "persons pointing to the right"]
    pose_person_plural_list = ["sitting persons", "standing persons", "lying persons"]

    person_info_list = ["name", "pose", "gesture"]
    object_comp_list = ["biggest", "largest", "smallest", "heaviest", "lightest", "thinnest"]

    talk_list = ["something about yourself", "the time", "what day is today", "what day is tomorrow", "your teams name",
                 "your teams country", "your teams affiliation", "the day of the week", "the day of the month"]
    question_list = ["question", "quiz"]

    color_list = ["blue", "yellow", "black", "white", "red", "orange", "gray"]
    clothe_list = ["t shirt", "shirt", "blouse", "sweater", "coat", "jacket"]
    clothes_list = ["t shirts", "shirts", "blouses", "sweaters", "coats", "jackets"]
    color_clothe_list = []
    for (a, b) in list(itertools.product(color_list, clothe_list)):
        color_clothe_list = color_clothe_list + [a + " " + b]
    color_clothes_list = []
    for (a, b) in list(itertools.product(color_list, clothes_list)):
        color_clothes_list = color_clothes_list + [a + " " + b]

    def generate_command_start(self, cmd_category="", difficulty=0):
        cmd_list = []
        # cmd_list = ["goToLoc", "takeObjFromPlcmt", "findPrsInRoom", "findObjInRoom", "meetPrsAtBeac", "countObjOnPlcmt",
        #             "countPrsInRoom", "tellPrsInfoInLoc", "tellObjPropOnPlcmt", "talkInfoToGestPrsInRoom",
        #             "answerToGestPrsInRoom", "followNameFromBeacToRoom", "guideNameFromBeacToBeac",
        #             "guidePrsFromBeacToBeac", "guideClothPrsFromBeacToBeac", "bringMeObjFromPlcmt",
        #             "tellCatPropOnPlcmt", "greetClothDscInRm", "greetNameInRm", "meetNameAtLocThenFindInRm",
        #             "countClothPrsInRoom", "countClothPrsInRoom", "tellPrsInfoAtLocToPrsAtLoc", "followPrsAtLoc"]

        # HRI and people perception commands
        person_cmd_list = ["goToLoc", "findPrsInRoom", "meetPrsAtBeac", "countPrsInRoom", "tellPrsInfoInLoc",
                           "talkInfoToGestPrsInRoom", "answerToGestPrsInRoom", "followNameFromBeacToRoom",
                           "guideNameFromBeacToBeac", "guidePrsFromBeacToBeac", "guideClothPrsFromBeacToBeac",
                           "greetClothDscInRm", "greetNameInRm", "meetNameAtLocThenFindInRm", "countClothPrsInRoom",
                           "countClothPrsInRoom", "tellPrsInfoAtLocToPrsAtLoc", "followPrsAtLoc"]
        # Object manipulation and perception commands
        object_cmd_list = ["goToLoc", "takeObjFromPlcmt", "findObjInRoom", "countObjOnPlcmt", "tellObjPropOnPlcmt",
                           "bringMeObjFromPlcmt", "tellCatPropOnPlcmt"]

        if cmd_category == "people":
            cmd_list = person_cmd_list
        elif cmd_category == "objects":
            cmd_list = object_cmd_list
        else:
            cmd_list = person_cmd_list if random.random() > 0.5 else object_cmd_list

        command = random.choice(cmd_list)
        # command = "" # To debug commands
        command_string = ""
        if command == "goToLoc":
            command_string = "{goVerb} {toLocPrep} the {loc_room} then " + \
                             self.generate_command_followup("atLoc", cmd_category, difficulty)
        elif command == "takeObjFromPlcmt":
            command_string = "{takeVerb} {art} {obj_singCat} {fromLocPrep} the {plcmtLoc} and " + \
                             self.generate_command_followup("hasObj", cmd_category, difficulty)
        elif command == "findPrsInRoom":
            command_string = "{findVerb} a {gestPers_posePers} {inLocPrep} the {room} and " + \
                             self.generate_command_followup("foundPers", cmd_category, difficulty)
        elif command == "findObjInRoom":
            command_string = "{findVerb} {art} {obj_singCat} {inLocPrep} the {room} then " + \
                             self.generate_command_followup("foundObj", cmd_category, difficulty)
        elif command == "meetPrsAtBeac":
            command_string = "{meetVerb} {name} {inLocPrep} the {room} and " + \
                             self.generate_command_followup("foundPers", cmd_category, difficulty)
        elif command == "countObjOnPlcmt":
            command_string = "{countVerb} {plurCat} there are {onLocPrep} the {plcmtLoc}"
        elif command == "countPrsInRoom":
            command_string = "{countVerb} {gestPersPlur_posePersPlur} are {inLocPrep} the {room}"
        elif command == "tellPrsInfoInLoc":
            command_string = "{tellVerb} me the {persInfo} of the person {inRoom_atLoc}"
        elif command == "tellObjPropOnPlcmt":
            command_string = "{tellVerb} me what is the {objComp} object {onLocPrep} the {plcmtLoc}"
        elif command == "talkInfoToGestPrsInRoom":
            command_string = "{talkVerb} {talk} {talkPrep} the {gestPers} {inLocPrep} the {room}"
        elif command == "answerToGestPrsInRoom":
            command_string = "{answerVerb} the {question} {ofPrsPrep} the {gestPers} {inLocPrep} the {room}"
        elif command == "followNameFromBeacToRoom":
            command_string = "{followVerb} {name} {fromLocPrep} the {loc} {toLocPrep} the {room}"
        elif command == "guideNameFromBeacToBeac":
            command_string = "{guideVerb} {name} {fromLocPrep} the {loc} {toLocPrep} the {loc_room}"
        elif command == "guidePrsFromBeacToBeac":
            command_string = "{guideVerb} the {gestPers_posePers} {fromLocPrep} the {loc} {toLocPrep} the {loc_room}"
        elif command == "guideClothPrsFromBeacToBeac":
            command_string = "{guideVerb} the person wearing a {colorClothe} {fromLocPrep} the {loc} {toLocPrep} the {loc_room}"
        elif command == "bringMeObjFromPlcmt":
            command_string = "{bringVerb} me {art} {obj} {fromLocPrep} the {plcmtLoc}"
        elif command == "tellCatPropOnPlcmt":
            command_string = "{tellVerb} me what is the {objComp} {singCat} {onLocPrep} the {plcmtLoc}"
        elif command == "greetClothDscInRm":
            command_string = "{greetVerb} the person wearing {art} {colorClothe} {inLocPrep} the {room} and " + \
                             self.generate_command_followup("foundPers", cmd_category, difficulty)
        elif command == "greetNameInRm":
            command_string = "{greetVerb} {name} {inLocPrep} the {room} and " + \
                             self.generate_command_followup("foundPers", cmd_category, difficulty)
        elif command == "meetNameAtLocThenFindInRm":
            command_string = "{meetVerb} {name} {atLocPrep} the {loc} then {findVerb} them {inLocPrep} the {room}"
        elif command == "countClothPrsInRoom":
            command_string = "{countVerb} people {inLocPrep} the {room} are wearing {colorClothes}"
        elif command == "countClothPrsInRoom":
            command_string = "{countVerb} people {inLocPrep} the {room} are wearing {colorClothes}"
        elif command == "tellPrsInfoAtLocToPrsAtLoc":
            command_string = "{tellVerb} the {persInfo} of the person {atLocPrep} the {loc} to the person {atLocPrep} the {loc2}"
        elif command == "followPrsAtLoc":
            command_string = "{followVerb} the {gestPers_posePers} {inRoom_atLoc}"
        else:
            warnings.warn("Command type not covered: " + command)
            return "WARNING"

        for ph in re.findall(r'(\{\w+\})', command_string, re.DOTALL):
            command_string = command_string.replace(ph, self.insert_placeholders(ph))

        # TODO allow multiple articles
        art_ph = re.findall(r'\{(art)\}\s*([A-Za-z])', command_string, re.DOTALL)
        if art_ph:
            command_string = command_string.replace("art",
                                                    "an" if art_ph[0][1].lower() in ["a", "e", "i", "o", "u"] else "a")
        # TODO eliminate double mentions of location
        if "loc2" in command_string:
            command_string = command_string.replace("loc2", random.choice(
                [x for x in self.location_names if x not in command_string]))
        elif "room2" in command_string:
            command_string = command_string.replace("room2", random.choice(
                [x for x in self.room_names if x not in command_string]))
        elif "plcmtLoc2" in command_string:
            command_string = command_string.replace("plcmtLoc2", random.choice(
                [x for x in self.placement_location_names if x not in command_string]))
        return command_string.replace('{', '').replace('}', '')

    def generate_command_followup(self, type, cmd_category="", difficulty=0):
        if type == "atLoc":
            person_cmd_list = ["findPrs", "meetName"]
            object_cmd_list = ["findObj"]
            if cmd_category == "people":
                cmd_list = person_cmd_list
            elif cmd_category == "objects":
                cmd_list = object_cmd_list
            else:
                cmd_list = person_cmd_list if random.random() > 0.5 else object_cmd_list
        elif type == "hasObj":
            cmd_list = ["placeObjOnPlcmt", "deliverObjToMe", "deliverObjToPrsInRoom", "deliverObjToNameAtBeac"]
        elif type == "foundPers":
            cmd_list = ["talkInfo", "answerQuestion", "followPrs", "followPrsToRoom", "guidePrsToBeacon"]
        elif type == "foundObj":
            cmd_list = ["takeObj"]

        command = random.choice(cmd_list)
        command_string = ""
        if command == "findObj":
            command_string = "{findVerb} {art} {obj_singCat} and " + \
                             self.generate_command_followup("foundObj")
        elif command == "findPrs":
            command_string = "{findVerb} the {gestPers_posePers} and " + \
                             self.generate_command_followup("foundPers")
        elif command == "meetName":
            command_string = "{meetVerb} {name} and " + \
                             self.generate_command_followup("foundPers")
        elif command == "placeObjOnPlcmt":
            command_string = "{placeVerb} it {onLocPrep} the {plcmtLoc2}"
        elif command == "deliverObjToMe":
            command_string = "{deliverVerb} it to me"
        elif command == "deliverObjToPrsInRoom":
            command_string = "{deliverVerb} it {deliverPrep} the {gestPers_posePers} {inLocPrep} the {room}"
        elif command == "deliverObjToNameAtBeac":
            command_string = "{deliverVerb} it {deliverPrep} {name} {inLocPrep} the {room}"
        elif command == "talkInfo":
            command_string = "{talkVerb} {talk}}"
        elif command == "answerQuestion":
            command_string = "{answerVerb} a {question}"
        elif command == "followPrs":
            command_string = "{followVerb} them"
        elif command == "followPrsToRoom":
            command_string = "{followVerb} them {toLocPrep} the {loc2_room2}"
        elif command == "guidePrsToBeacon":
            command_string = "{guideVerb} them {toLocPrep} the {loc2_room2}"
        elif command == "takeObj":
            command_string = "{takeVerb} it and " + \
                             self.generate_command_followup("hasObj")
        else:
            warnings.warn("Command type not covered: " + command)
            return "WARNING"
        return command_string

    def insert_placeholders(self, ph):
        ph = ph.replace('{', '').replace('}', '')
        if len(ph.split('_')) > 1:
            ph = random.choice(ph.split('_'))
        if ph == "goVerb":
            return random.choice(self.verb_dict["go"])
        elif ph == "takeVerb":
            return random.choice(self.verb_dict["take"])
        elif ph == "findVerb":
            return random.choice(self.verb_dict["find"])
        elif ph == "meetVerb":
            return random.choice(self.verb_dict["meet"])
        elif ph == "countVerb":
            return random.choice(self.verb_dict["count"])
        elif ph == "tellVerb":
            return random.choice(self.verb_dict["tell"])
        elif ph == "deliverVerb":
            return random.choice(self.verb_dict["deliver"])
        elif ph == "talkVerb":
            return random.choice(self.verb_dict["talk"])
        elif ph == "answerVerb":
            return random.choice(self.verb_dict["answer"])
        elif ph == "followVerb":
            return random.choice(self.verb_dict["follow"])
        elif ph == "placeVerb":
            return random.choice(self.verb_dict["place"])
        elif ph == "guideVerb":
            return random.choice(self.verb_dict["guide"])
        elif ph == "greetVerb":
            return random.choice(self.verb_dict["greet"])
        elif ph == "bringVerb":
            return random.choice(self.verb_dict["bring"])

        elif ph == "toLocPrep":
            return random.choice(self.prep_dict["toLocPrep"])
        elif ph == "fromLocPrep":
            return random.choice(self.prep_dict["fromLocPrep"])
        elif ph == "inLocPrep":
            return random.choice(self.prep_dict["inLocPrep"])
        elif ph == "onLocPrep":
            return random.choice(self.prep_dict["onLocPrep"])
        elif ph == "atLocPrep":
            return random.choice(self.prep_dict["atLocPrep"])
        elif ph == "deliverPrep":
            return random.choice(self.prep_dict["deliverPrep"])
        elif ph == "talkPrep":
            return random.choice(self.prep_dict["talkPrep"])
        elif ph == "ofPrsPrep":
            return random.choice(self.prep_dict["ofPrsPrep"])

        elif ph == "connector":
            return random.choice(self.connector_list)

        elif ph == "plcmtLoc2":
            return "plcmtLoc2"
        elif ph == "plcmtLoc":
            return random.choice(self.placement_location_names)
        elif ph == "room2":
            return "room2"
        elif ph == "room":
            return random.choice(self.room_names)
        elif ph == "loc2":
            return "loc2"
        elif ph == "loc":
            return random.choice(self.location_names)
        elif ph == "inRoom":
            return random.choice(self.prep_dict["inLocPrep"]) + " the " + random.choice(self.room_names)
        elif ph == "atLoc":
            return random.choice(self.prep_dict["atLocPrep"]) + " the " + random.choice(self.location_names)

        elif ph == "gestPers":
            return random.choice(self.gesture_person_list)
        elif ph == "posePers":
            return random.choice(self.pose_person_list)
        elif ph == "name":
            return random.choice(self.person_names)
        elif ph == "gestPersPlur":
            return random.choice(self.gesture_person_plural_list)
        elif ph == "posePersPlur":
            return random.choice(self.pose_person_plural_list)
        elif ph == "persInfo":
            return random.choice(self.person_info_list)

        elif ph == "obj":
            return random.choice(self.object_names)
        elif ph == "singCat":
            return random.choice(self.object_categories_singular)
        elif ph == "plurCat":
            return random.choice(self.object_categories_plural)
        elif ph == "objComp":
            return random.choice(self.object_comp_list)

        elif ph == "talk":
            return random.choice(self.talk_list)
        elif ph == "question":
            return random.choice(self.question_list)

        elif ph == "colorClothe":
            return random.choice(self.color_clothe_list)
        elif ph == "colorClothes":
            return random.choice(self.color_clothes_list)

        # replace article later
        elif ph == "art":
            return "{art}"
        else:
            warnings.warn("Placeholder not covered: " + ph)
            return "WARNING"
