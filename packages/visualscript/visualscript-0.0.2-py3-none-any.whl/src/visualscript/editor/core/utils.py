def dumpException(e):
    import traceback
    print("%s EXCEPTION:" % e.__class__.__name__, e)
    traceback.print_tb(e.__traceback__)

def parse_signatures(docstring, cls):
    import re
    class_name = str(cls).split('.')[-1].split('\'')[0]
    pattern = fr"^{class_name}\("
    signatures = []
    for line in docstring.split("\n"):
        if re.match(pattern, line):
            signature = line.strip().split("->")[0]
            function_name, args_string = signature.split("(", 1)
            if args_string.strip() == ")":
                signatures.append([])
            else:
                args = args_string.strip("() ").split(", ")
                parameter_types = []
                for arg in args:
                    try:
                        # parameter_types.append(arg)
                        parameter_types.append(eval(arg))
                    except NameError:
                        if arg == class_name:
                            parameter_types.append(cls)
                        else:
                            parameter_types.append(None)
                signatures.append(parameter_types)
    return signatures
