import inspect
import dis

def list_func_calls(fn):
    funcs = []
    bytecode = dis.Bytecode(fn)
    instrs = list(reversed([instr for instr in bytecode]))
    for (ix, instr) in enumerate(instrs):
        if instr.opname=="CALL_FUNCTION":
            load_func_instr = instrs[ix + instr.arg + 1]
            if load_func_instr.argval in all_nodes:
                funcs.append(load_func_instr.argval)

    return funcs

all_nodes = []
edges = {}

def node(f):
    all_nodes.append(f.__name__)
    edges[f.__name__] = list_func_calls(f)
    inspect.currentframe().f_back.f_code.co_name
    def _wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return _wrapper