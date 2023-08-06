import dis
import examples.adding_example as example

# print(example)

def list_func_calls(fn):
    funcs = []
    bytecode = dis.Bytecode(fn)
    instrs = list(reversed([instr for instr in bytecode]))
    for (ix, instr) in enumerate(instrs):
        if instr.opname=="CALL_FUNCTION":
            load_func_instr = instrs[ix + instr.arg + 1]
            funcs.append(load_func_instr.argval)

    return ["%d. %s" % (ix, funcname) for (ix, funcname) in enumerate(reversed(funcs), 1)]

# byte_code = compile(source_code, source_py, "exec")
# print(list_func_calls(example))

# dis.dis(example)

source_py = "examples/adding_example.py"

with open(source_py) as f_source:
    source_code = f_source.read()
    source_code.find("if __name__ == \"__main__\"")

byte_code = compile(source_code, source_py, "exec")
for item in list(dis.get_instructions(byte_code)):
    print(item)

# dis(byte_code)

# print(source_code)