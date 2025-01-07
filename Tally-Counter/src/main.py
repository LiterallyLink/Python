from util import get_counter_data, create_initial_counter
from utils.counter_manager import CounterManager
from gui.parent_gui import GUI

def main():
    counter_data = get_counter_data()

    manager = CounterManager(counter_data)
    if len(counter_data) == 0: create_initial_counter(manager)

    gui = GUI(manager)
    gui.run()

if __name__ == "__main__":
    main()