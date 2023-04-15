import sys, logging

class Flow:
    data: list

    def __init__(self, data):
        self.data = data

    def select_option(self):
        for k, v in enumerate(self.data):
            print(f"{k}. {v.name}")
        
        manual_input = input("your input is [index]: ")

        try:
            option = self.data[int(manual_input)]
            return option
        except Exception:
            logging.debug("You input a not existing value!")
            sys.exit()
