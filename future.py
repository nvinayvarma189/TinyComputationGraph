from graph import graph

class Future:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.state = "CREATED"
        self.result = None
        self.parent_future = None
        self.nested_future = None
        # self.all_args = args + kwargs # TODO - make it work with kwargs also
    
    def resolve(self):
        if self.state != "RESOLVED":
            resolved_args = []
            for arg in self.args:
                if isinstance(arg, Future):
                    resolved_args.append(arg.resolve())
                    graph.add_edge(self, arg, "inputs")
                else:
                    resolved_args.append(arg)

            if all(not isinstance(arg, Future) for arg in resolved_args):
                self.state = "ARGS_RESOLVED"
                self.result = self.func(*resolved_args)
                if isinstance(self.result, Future):
                    nested_future = self.result
                    self.nested_future = nested_future
                    nested_future.parent_future = self
                    graph.add_edge(nested_future, self, "parent_futures")
                    graph.add_edge(self, nested_future, "nested_futures")
                    self.result = self.result.resolve()
                self.state = "RESOLVED"
                graph.set_root_node(self)
                return self.result
            else:
                raise Exception("Not all args are resolved")

    def __repr__(self) -> str:
        a = f"{self.func.__name__}"
        b = f"{self.parent_future.func.__name__}" if self.parent_future else "None"
        c = f"{self.nested_future.func.__name__}" if self.nested_future else "None"
        return f"{a} -> {b} -> {c}"