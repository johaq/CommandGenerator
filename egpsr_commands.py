import random
import re
import itertools
import warnings
from gpsr_commands import CommandGenerator


class EgpsrCommandGenerator:

    def __init__(self, gpsr_generator):
        self.gpsr_generator = gpsr_generator

    def generate_setup(self):
        setup_string = ""
        setup_string += self.generate_misplaced_objects()
        setup_string += "\n" + self.generator_person_requests()
        return setup_string

    def generate_misplaced_objects(self):
        misplaced_objects_string = "1. The {obj} is at the {plcmtLoc} instead of at the {plcmtLoc2}" \
                                    "\n2. Put an object on the floor {inRoom}"
        for ph in re.findall(r'(\{\w+\})', misplaced_objects_string, re.DOTALL):
            misplaced_objects_string = misplaced_objects_string.replace(ph, self.gpsr_generator.insert_placeholders(ph))
        misplaced_objects_string = misplaced_objects_string.replace("plcmtLoc2", random.choice(
                [x for x in self.gpsr_generator.placement_location_names if x not in misplaced_objects_string]))
        return misplaced_objects_string

    def generator_person_requests(self):
        person_requests_string = "3. There is a person at the {loc}, their request is:" \
                                    "\n\t" + self.gpsr_generator.generate_command_start(cmd_category="people") + \
                                    "\n4. There is a person at the {loc2}, their request is:" \
                                    "\n\t" + self.gpsr_generator.generate_command_start(cmd_category="objects")
        for ph in re.findall(r'(\{\w+\})', person_requests_string, re.DOTALL):
            person_requests_string = person_requests_string.replace(ph, self.gpsr_generator.insert_placeholders(ph))
        person_requests_string = person_requests_string.replace("loc2", random.choice(
                [x for x in self.gpsr_generator.location_names if x not in person_requests_string]))

        return person_requests_string