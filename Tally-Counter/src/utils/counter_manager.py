from utils.counter import Counter
from util import save_counter_data
import atexit

class CounterManager():
    def __init__(self, counter_dict):
        self.counter_dict = counter_dict
        atexit.register(self.save_on_exit)

    def create_new_counter(self, counter_name="Unnamed Counter", starting_count=0, increment_value=1, decrement_value=1, symbol=None):
        counter_name = self.validate_unique_counter_name(counter_name)
        self.counter_dict[counter_name] = Counter(starting_count, increment_value, decrement_value, symbol)

    def remove_counter(self, counter_name):
        del self.counter_dict[counter_name]

    def get_counter_names(self):
        all_counter_names = self.counter_dict.keys()
        return list(all_counter_names)
    
    def get_counter_dict_length(self):
        return len(self.counter_dict)
    
    def get_counter(self, counter_name):
        return self.counter_dict[counter_name]

    def save_on_exit(self):
        save_counter_data(self.counter_dict)

    def validate_unique_counter_name(self, name):
        if name not in self.counter_dict:
            return name
        else:
            i = 2
        while True:
            new_name = f"{name} {i}"
            if new_name not in self.counter_dict:
                return new_name
            i += 1
        