#!/usr/bin/python3
"""defines HBnB console"""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curlyBraces = re.search(r"\{(.*?)\}", arg)
    squareBrackets = re.search(r"\[(.*?)\]", arg)
    if curlyBraces is None:
        if squareBrackets is None:
            return [o.strip(",") for o in split(arg)]
        else:
            lexer = split(arg[:squareBrackets.span()[0]])
            retList = [o.strip(",") for o in lexer]
            retList.append(squareBrackets.group())
            return retList
    else:
        lexer = split(arg[:curlyBraces.span()[0]])
        retList = [o.strip(",") for o in lexer]
        retList.append(curlyBraces.group())
        return retList


class HBNBCommand(cmd.Cmd):
    """defines HolbertonBnB command interpreter

    Attributes:
        prompt (str): command prompt
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """do nothing upon receiving empty line"""
        pass

    def default(self, arg):
        """default behavior of cmd module when input invalid"""
        arg_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        get_match = re.search(r"\.", arg)
        if get_match is not None:
            arg_list = [arg[:get_match.span()[0]], arg[get_match.span()[1]:]]
            get_match = re.search(r"\((.*?)\)", arg_list[1])
            if get_match is not None:
                command = [arg_list[1][:get_match.span()[0]], get_match.group()[1:-1]]
                if command[0] in arg_dict.keys():
                    call = "{} {}".format(arg_list[0], command[1])
                    return arg_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """quit command to exit program"""
        return True

    def do_EOF(self, arg):
        """EOF to exit program"""
        print("")
        return True

    def do_create(self, arg):
        """usage: create <class>
        creates new class instance and print its id
        """
        arg_list = parse(arg)
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg_list[0])().id)
            storage.save()

    def do_show(self, arg):
        """usage: show <class> <id> or <class>.show(<id>)
        display str repre of class instance of given id
        """
        arg_list = parse(arg)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg_list[0], arg_list[1])])

    def do_destroy(self, arg):
        """usage: destroy <class> <id> or <class>.destroy(<id>)
        delete class instance of given id"""
        arg_list = parse(arg)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            storage.save()

    def do_all(self, arg):
        """usage: all or all <class> or <class>.all()
        display str repre of all instances of given class
        If no class is specified, display all instantiated objects"""
        arg_list = parse(arg)
        if len(arg_list) > 0 and arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if len(arg_list) > 0 and arg_list[0] == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(arg_list) == 0:
                    obj_list.append(obj.__str__())
            print(obj_list)

    def do_count(self, arg):
        """usage: count <class> or <class>.count()
        retrieve number of instances of given class"""
        arg_list = parse(arg)
        counter = 0
        for obj in storage.all().values():
            if arg_list[0] == obj.__class__.__name__:
                counter += 1
        print(counter)

    def do_update(self, arg):
        """usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        update class instance of given id by adding or updating
        given attribute key/value pair or dictionary"""
        arg_list = parse(arg)
        obj_dict = storage.all()

        if len(arg_list) == 0:
            print("** class name missing **")
            return False
        if arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arg_list) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(arg_list) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_list) == 3:
            try:
                type(eval(arg_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg_list) == 4:
            obj = obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            if arg_list[2] in obj.__class__.__dict__.keys():
                value_type = type(obj.__class__.__dict__[arg_list[2]])
                obj.__dict__[arg_list[2]] = value_type(arg_list[3])
            else:
                obj.__dict__[arg_list[2]] = arg_list[3]
        elif type(eval(arg_list[2])) == dict:
            obj = obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            for key, value in eval(arg_list[2]).items():
                if (key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key]) in {str, int, float}):
                    value_type = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = value_type(value)
                else:
                    obj.__dict__[key] = value
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
