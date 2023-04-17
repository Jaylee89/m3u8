import sys

from util.log import get_logging

class Flow:
    data: list

    def __init__(self, data):
        self.data = data

    def select_option(self):
        for k, v in enumerate(self.data):
            print(f"{k}. {v.name}")

        if "unittest" in sys.modules.keys():
            manual_input = 0
        else:
            manual_input = input("\nYour input is [index]: ")

        try:
            option = self.data[int(manual_input)]
            get_logging().debug(f"You selected {manual_input}. {option.name}\n")
            return option
        except Exception:
            get_logging().debug("You input a not existing value!")
            sys.exit()
