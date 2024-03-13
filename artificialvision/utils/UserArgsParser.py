import inspect
import sys, os
from ast import literal_eval

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import ImgClassification

def input_argument(arg):
    arg_types = {}
    arg_types[type({})] = ["Dictionary(multiple)", "{A:B, C:D, E:F...}", literal_eval]
    arg_types[type(())] = ["Tuple(multiple)", "(A, B, C, D...)", literal_eval]
    arg_types[type([])] = ["List(multiple)", "[A, B, C, D...]", literal_eval]
    arg_types[type(1)] = ["Integer(single)", "1, 1000, 12345", int]
    arg_types[type(0.1)] = ["Float(single)", "1.0, 0.1, 0.00123", float]
    arg_types[type("A")] = ["String(single)", "'ABCD', \"ABCD\"", str]

    print("Argument type - " + arg_types[type(arg)][0])
    print("Input example - " + arg_types[type(arg)][1])
    while True:
        user_input = input("Input argument: ")
        try:
            user_input = arg_types[type(arg)][2](user_input)
            break
        except:
            print("Invalid input")
    return user_input


def arg_parser(user_class):
    try:
        class_args = inspect.getargspec(user_class.__init__)
    except:
        print("Invaild Class")
    result = {}
    arg_names = [i for i in class_args[0] if i != 'self']
    arg_defaults = class_args[3]
    print("Total " + str(len(arg_names)) + " Argument in Class")
    for name, default in list(zip(arg_names, arg_defaults)):
        print("--------------------------------------")
        print("Argument Name: " + name)
        print("Default Argument - " + str(default))
        while True:
            user_input = input("Using default Argument? [y/n]: ")
            if user_input.lower() == 'y' or user_input.lower() == 'n':
                break
        if user_input.lower() == 'y':
            result[name] = default
        else:
            result[name] = input_argument(default)
        print(name + " value - " + str(result[name]))
    return result

arg_parser(ImgClassification.ImgClassification)