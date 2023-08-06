from hashlib import blake2b

LISTBOX_MIMETYPE = "application/x-item"

class ConfException(Exception): pass
class InvalidNodeRegistration(Exception): pass
class OpCodeNotRegistered(ConfException): pass

CLASS_REGISTRY = {}

def register_node():
    def decorator(original_class):
        CLASS_REGISTRY[original_class.__name__] = original_class
        return original_class
    return decorator

def get_class_from_name(class_name):
    if class_name not in CLASS_REGISTRY: raise OpCodeNotRegistered("Class '%s' is not registered" % class_name)
    return CLASS_REGISTRY[class_name]

from editor.nodes import *