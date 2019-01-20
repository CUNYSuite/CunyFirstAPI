import ast
from collections import defaultdict 

file_path = "./cunyfirstapi/cunyfirstapi.py"

f = open(file_path, 'r')
source = f.read()
f.close()




class AstGraphGenerator(object):

    def __init__(self, source):
        self.graph = defaultdict(lambda: [])
        self.source = source  # lines of the source code

    def __str__(self):
        return str(self.graph)

    def _getid(self, node):
        try:
            lineno = node.lineno - 1
            return "%s: %s" % (type(node), self.source[lineno].strip())

        except AttributeError:
            return type(node)

    def visit(self, node):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        for _, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)

            elif isinstance(value, ast.AST):
                node_source = self._getid(node)
                value_source = self._getid(value)
                self.graph[node_source].append(value_source)
                # self.graph[type(node)].append(type(value))
                self.visit(value)



tree = ast.parse(source)
astY = AstGraphGenerator(source)

print(astY.visit(tree))
# from collections import defaultdict 
  
# class Graph(): 
#     def __init__(self, vertices): 
#         self.graph = defaultdict(list) 
#         self.V = vertices 
  
#     def addEdge(self, u, v): 
#         self.graph[u].append(v) 
  
#     def isCyclicUtil(self, v, visited, recStack): 
  
#         visited.append(v)
#         recStack.append(v)
  
#         for neighbour in self.graph[v]: 
#             if neighbour not in visited: 
#                 if self.isCyclicUtil(neighbour, visited, recStack): 
#                     return True
#             elif neighbour in recStack: 
#                 return True
#         recStack.remove(v)
#         return False
  
#     def isCyclic(self): 
#         visited = [False] * len(list(self.V))
#         recStack = [False] * len(list(self.V))
#         for node in self.V: 
#             if node not in visited: 
#                 if self.isCyclicUtil(node,visited,recStack): 
#                     return True
#         return False

# class Call:

#     def __init__(self, call_class, call_name):
#         self.call_class = call_class
#         self.call_name = call_name

#     @staticmethod
#     def get_id(call):
#         return f"class({call.call_class})-name({call.call_name})"

#     def create_call_from_decl(decl):
#         pass

#     def __hash__(self):
#         return hash(Call.get_id(self)) 

#     def __eq__(self, other):
#         return Call.get_id(self) == Call.get_id(other)

# tree = ast.parse(source)

# callers = {}
# look_up = {}

# def dump_adjlist(dct):
#     print("AST:")
#     for caller, calleee in dct.items():
#         callee_ids = []
#         for call in calleee:
#             callee_ids += [call]
#         print("{}: [{}]".format(caller, callee_ids))

# def walk_assign(tree):
#     global look_up
#     for node in tree:
#         if isinstance(node, ast.Assign):
#             for target in node.targets:
#                 try:
#                     look_up[target.id] = node.value.func.id
#                 except AttributeError:
#                     pass
#         elif isinstance(node, ast.ClassDef):
#             walk_assign(node.body)

# def walk(class_name, tree):
#     global callers
#     for node in tree:
#         if isinstance(node, ast.ClassDef):
#             walk(node.name, node.body)
#         elif isinstance(node, ast.FunctionDef):
#             call = Call(class_name, node.name)
#             callers[Call.get_id(call)] = []
#             body = node.body
#             for exp in body:
#                 try:
#                     if isinstance(exp.value, ast.Call):
#                         if isinstance(exp.value.func, ast.Attribute):
#                             try:
#                                 attr_name = exp.value.func.value.id
#                                 if attr_name in look_up:
#                                     attr_name = look_up[attr_name]
#                                 callers[Call.get_id(call)] += [Call.get_id(Call(attr_name, exp.value.func.attr))]
#                             except AttributeError:
#                                 try:
#                                     attr_name = exp.value.func.value.value.id
#                                     print(ast.dump(exp.value))
#                                     if attr_name in look_up:
#                                         attr_name = look_up[attr_name]
#                                     callers[Call.get_id(call)] += [Call.get_id(Call(attr_name, exp.value.func.attr))]
#                                 except AttributeError:
#                                     pass
#                         else:
#                             callers[Call.get_id(call)] += [Call.get_id(Call("", exp.value.func.id))]
#                 except AttributeError:
#                     pass

                
# walk_assign(ast.walk(tree))
# walk("", ast.walk(tree))

# graph = Graph(callers.keys())
# for caller, calleee in callers.items():
#         for call in calleee:
#             print(f"{caller} => {call}")
#             graph.addEdge(caller, call)

# print(graph.isCyclic())
