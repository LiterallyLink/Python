import os
import pickle

file_path = "data/counter_data.pickle"

def get_counter_data():
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    if not os.path.exists(file_path):
        counter_dict = {}

        with open(file_path, "wb") as file:
            pickle.dump(counter_dict, file)
        return counter_dict
    else:
        with open(file_path, "rb") as file:
            return pickle.load(file)

def save_counter_data(updated_counter_dict):    
    with open("data/counter_data.pickle", "wb") as file:
        pickle.dump(updated_counter_dict, file)

def create_initial_counter(manager):
    counter_dict_length = manager.get_counter_dict_length()

    if counter_dict_length == 0:
        manager.create_new_counter()
