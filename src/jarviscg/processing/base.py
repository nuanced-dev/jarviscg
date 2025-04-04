# Copyright [pythonJaRvis] [name of copyright owner]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import ast
import os
from functools import reduce
from jarviscg import utils
from jarviscg.machinery.definitions import Definition



class ProcessingBase(ast.NodeVisitor):
    def __init__(self, filename, modname, modules_analyzed):
        self.modname = modname

        self.modules_analyzed = modules_analyzed
        self.modules_analyzed.add(self.modname)

        self.filename = os.path.abspath(filename)
        with open(filename, "rt",errors="ignore") as f:
            self.contents = f.read()
        self.name_stack = []
        self.method_stack = []
        self.last_called_names = None
        # self.callStack = [modname]
        self.callStack = []
    def pushStack(self, ns):
        self.callStack.append(ns)
        self.current_ns = self.callStack[-1]
        body = self.node_manager.get(ns)
        self.visit(body)
        pass

    def popStack(self):
        ns = self.callStack.pop()
        changeDict = self.change_manager.getChange(ns)
        pass
    def get_modules_analyzed(self):
        return self.modules_analyzed

    def merge_modules_analyzed(self, analyzed):
        self.modules_analyzed = self.modules_analyzed.union(analyzed)

    @property
    def current_ns(self):
        return self.callStack[-1] if self.callStack else ".".join(self.name_stack)

    @property
    def current_method(self):
        return ".".join(self.method_stack)

    def visit_Module(self, node):
        self.name_stack.append(self.modname)
        self.method_stack.append(self.modname)
        self.scope_manager.get_scope(self.modname).reset_counters()
        self.generic_visit(node)
        self.method_stack.pop()
        self.name_stack.pop()

    def visit_FunctionDef(self, node):
        self.name_stack.append(node.name)
        self.method_stack.append(node.name)
        for stmt in node.body:
            self.visit(stmt)
        self.method_stack.pop()
        self.name_stack.pop()

    def visit_Lambda(self, node, lambda_name=None):
        self.name_stack.append(lambda_name)
        self.method_stack.append(lambda_name)
        self.visit(node.body)
        self.method_stack.pop()
        self.name_stack.pop()

    def visit_If(self, node, if_name=None):
        self.name_stack.append(if_name)
        self.method_stack.append(if_name)
        for stmt in node.body:
            self.visit(stmt)
        self.method_stack.pop()
        self.name_stack.pop()

    def visit_With(self, node, if_name=None):
        self.name_stack.append(if_name)
        self.method_stack.append(if_name)
        for stmt in node.body:
            self.visit(stmt)
        self.method_stack.pop()
        self.name_stack.pop()

    def visit_While(self,node, while_name=None):
        self.name_stack.append(while_name)
        self.method_stack.append(while_name)
        for stmt in node.body:
            self.visit(stmt)
        self.method_stack.pop()
        self.name_stack.pop()

    def visit_else(self,node , else_name = None):
        self.name_stack.append(else_name)
        self.method_stack.append(else_name)
        for stmt in node.orelse:
            self.visit(stmt)
        self.method_stack.pop()
        self.name_stack.pop()

    def visit_while_else(self,node,else_name=None):
        self.visit_else(node,else_name)

    def visit_For(self, node):
        for item in node.body:
            self.visit(item)

    def visit_Dict(self, node,listNode = None):
        # if not self.scope_manager.get_scope(self.current_ns):
        #     return
        # counter = self.scope_manager.get_scope(self.current_ns).inc_dict_counter()
        # dict_name = utils.get_dict_name(counter)
        #
        # sc = self.scope_manager.get_scope(utils.join_ns(self.current_ns, dict_name))
        # if not sc:
        #     for key, val in zip(node.keys, node.values):
        #         if key:
        #             self.visit(key)
        #         if val:
        #             self.visit(val)
        #     return
        # self.name_stack.append(dict_name)
        # sc.reset_counters()
        for key, val in zip(node.keys, node.values):
            if key:
                self.visit(key)
            if val:
                self.visit(val)
        # self.name_stack.pop()

    def visit_List(self, node,listNode = None):
        # if not self.scope_manager.get_scope(self.current_ns):
        #     return
        # counter = self.scope_manager.get_scope(self.current_ns).inc_list_counter()
        # list_name = utils.get_list_name(counter)
        #
        # sc = self.scope_manager.get_scope(utils.join_ns(self.current_ns, list_name))
        # if not sc:
        #     return
        # self.name_stack.append(list_name)
        # sc.reset_counters()
        for elt in node.elts:
            self.visit(elt)
        # self.name_stack.pop()

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_ClassDef(self, node):
        self.name_stack.append(node.name)
        self.method_stack.append(node.name)
        curScope = self.scope_manager.get_scope(self.current_ns)

        if curScope:
            curScope.reset_counters()
        clsRetNs = utils.join_ns(self.current_ns, utils.constants.RETURN_NAME)
        clsRetDefi: Definition = self.def_manager.get(clsRetNs)
        if not clsRetDefi:
            clsRetDefi = self.def_manager.create(clsRetNs, utils.constants.NAME_DEF)
        clsSelfNs = utils.join_ns(self.current_ns, 'self')
        clsSelfDefi: Definition = self.def_manager.get(clsSelfNs)
        if not clsSelfDefi:
            clsSelfDefi = self.def_manager.create(clsSelfNs, utils.constants.NAME_DEF)
        clsRetDefi.add_value_point(node.lineno, [self.current_ns])
        clsSelfDefi.add_value_point(node.lineno, [self.current_ns])
        for stmt in node.body:
            self.visit(stmt)
        self.method_stack.pop()
        self.name_stack.pop()

    def visit_Tuple(self, node):
        for elt in node.elts:
            self.visit(elt)

    def _handle_assign(self, targetns, decoded, row = 0, defiType = utils.constants.NAME_DEF):
        defi:Definition = self.def_manager.get(targetns)
        if not defi:
            defi = self.def_manager.create(targetns, defiType)
        if defi.get_type == utils.constants.NA_DEF:
            defi.def_type = utils.constants.NAME_DEF
        try:
            iter(decoded)
        except TypeError:
            return defi
        defi.add_value_point(row,decoded)
        return defi

    def _visit_return(self, node):
        if not node or not node.value:
            return

        self.visit(node.value)

        return_ns = utils.join_ns(self.current_ns, utils.constants.RETURN_NAME)
        self._handle_assign(return_ns, self.decode_node(node.value))



    def _visit_assign(self, value, targets):
        self.visit(value)

        decoded = self.decode_node(value)

        def do_assign(decoded, target):
            self.visit(target)
            # 元组需要解构
            if isinstance(target, ast.Tuple):
                for pos, elt in enumerate(target.elts):
                    if not isinstance(decoded, Definition) and pos < len(decoded):
                        do_assign(decoded[pos], elt)
            else:
                targetns = self._get_target_ns(target)
                for tns in targetns:
                    if not tns:
                        continue
                    defi = self._handle_assign(tns, decoded)
                    splitted = tns.split(".")
                    self.scope_manager.handle_assign(".".join(splitted[:-1]), splitted[-1], defi)

        for target in targets:
            do_assign(decoded, target)

    def decode_node(self, node):
        if isinstance(node, ast.Name):
            return [self.scope_manager.get_def(self.current_ns, node.id)]
        elif isinstance(node, ast.Call):
            decoded = self.decode_node(node.func)
            return_defs = []
            for called_def in decoded:
                if not isinstance(called_def, Definition):
                    continue
                return_ns = utils.constants.INVALID_NAME
                # 如果收func，则指向其返回值
                if called_def.get_type() == utils.constants.FUN_DEF:
                    return_ns = utils.join_ns(called_def.get_ns(), utils.constants.RETURN_NAME)
                #     如果是cls，指向其类
                elif called_def.get_type() == utils.constants.CLS_DEF:
                    return_ns = called_def.get_ns()
                #     如果是ext，指向其类，然后在后续的解析中完善
                elif called_def.get_type() == utils.constants.EXT_DEF:
                    return_ns = called_def.get_ns()
                defi = self.def_manager.get(return_ns)
                if defi:
                    return_defs.append(defi)

            return return_defs
        elif isinstance(node, ast.Lambda):
            lambda_counter = self.scope_manager.get_scope(self.current_ns).get_lambda_counter()
            lambda_name = utils.get_lambda_name(lambda_counter)
            return [self.scope_manager.get_def(self.current_ns, lambda_name)]
        elif isinstance(node, ast.Tuple):
            decoded = []
            for elt in node.elts:
                decoded.append(self.decode_node(elt))
            return decoded
        elif isinstance(node, ast.BinOp):
            decoded_left = self.decode_node(node.left)
            decoded_right = self.decode_node(node.right)
            # return the non definition types if we're talking about a binop
            # since we only care about the type of the return (num, str, etc)
            if not isinstance(decoded_left, Definition):
                return decoded_left
            if not isinstance(decoded_right, Definition):
                return decoded_right
        elif isinstance(node, ast.Attribute):
            names = self._retrieve_attribute_names(node)
            defis = []
            for name in names:
                defi = self.def_manager.get(name)
                if defi:
                    defis.append(defi)
            return defis
        elif isinstance(node, ast.Num):
            return [node.n]
        elif isinstance(node, ast.Str):
            return [node.s]
        elif self._is_literal(node):
            return [node]
        elif isinstance(node, ast.Dict):
            dict_counter = self.scope_manager.get_scope(self.current_ns).get_dict_counter()
            dict_name = utils.get_dict_name(dict_counter)
            scope_def = self.scope_manager.get_def(self.current_ns, dict_name)
            return [self.scope_manager.get_def(self.current_ns, dict_name)]
        elif isinstance(node, ast.List):
            list_counter = self.scope_manager.get_scope(self.current_ns).get_list_counter()
            list_name = utils.get_list_name(list_counter)
            scope_def = self.scope_manager.get_def(self.current_ns, list_name)
            return [self.scope_manager.get_def(self.current_ns, list_name)]
        elif isinstance(node, ast.Subscript):
            names = self.retrieve_subscript_names(node)
            defis = []
            for name in names:
                defi = self.def_manager.get(name)
                if defi:
                    defis.append(defi)
            return defis

        return []

    def _is_literal(self, item):
        return isinstance(item, int) or isinstance(item, str) or isinstance(item, float)

    def _retrieve_base_names(self, node):
        if not isinstance(node, ast.Attribute):
            raise Exception("The node is not an attribute")


        decoded = self.decode_node(node.value)
        if not decoded:
            return set()

        names = set()
        for name in decoded:
            if not name or not isinstance(name, Definition):
                continue
            names.add(name.get_ns())
            # for base in self.closured.get(name.get_ns(), []):
            #     cls = self.class_manager.get(base)
            #     if not cls:
            #         continue
            #
            #     for item in cls.get_mro():
            #         names.add(item)
        return names


    def _retrieve_parent_names(self, node):
        if not isinstance(node, ast.Attribute):
            raise Exception("The node is not an attribute")

        decoded = self.decode_node(node.value)
        if not decoded:
            return set()

        names = set()
        for parent in decoded:
            if not parent or not isinstance(parent, Definition):
                continue
            if getattr(self, "closured", None) and self.closured.get(parent.get_ns(), None):
                names = names.union(self.closured.get(parent.get_ns()))
            else:
                names.add(parent.get_ns())
        return names

    def _retrieve_attribute_names(self, node):
        if not getattr(self, "closured", None):
            return set()

        parent_names = self._retrieve_parent_names(node)
        names = set()
        for parent_name in parent_names:
            for name in self.closured.get(parent_name, []):
                defi = self.def_manager.get(name)
                if not defi:
                    continue
                if defi.get_type() == utils.constants.CLS_DEF:
                    cls_names = self.find_cls_fun_ns(defi.get_ns(), node.attr)
                    if cls_names:
                        names = names.union(cls_names)
                if defi.get_type() in [utils.constants.FUN_DEF, utils.constants.MOD_DEF]:
                    names.add(utils.join_ns(name, node.attr))
                if defi.get_type() == utils.constants.EXT_DEF:
                    # HACK: extenral attributes can lead to infinite loops
                    # Identify them here
                    if node.attr in name:
                        continue
                    ext_name = utils.join_ns(name, node.attr)
                    if not self.def_manager.get(ext_name):
                        self.def_manager.create(ext_name, utils.constants.EXT_DEF)
                    names.add(ext_name)
        return names

    def iterate_call_args(self, defi, node):
        for pos, arg in enumerate(node.args):
            self.visit(arg)
            decoded = self.decode_node(arg)
            if defi.is_function_def():
                pos_arg_names = defi.get_name_pointer().get_pos_arg(pos)
                # if arguments for this position exist update their namespace
                if not pos_arg_names:
                    continue
                for name in pos_arg_names:
                    arg_def = self.def_manager.get(name)
                    if not arg_def:
                        continue
                    for d in decoded:
                        if isinstance(d, Definition):
                            arg_def.get_name_pointer().add(d.get_ns())
                        else:
                            arg_def.get_lit_pointer().add(d)
            else:
                for d in decoded:
                    if isinstance(d, Definition):
                        defi.get_name_pointer().add_pos_arg(pos, None, d.get_ns())
                    else:
                        defi.get_name_pointer().add_pos_lit_arg(pos, None, d)

        for keyword in node.keywords:
            self.visit(keyword.value)
            decoded = self.decode_node(keyword.value)
            if defi.is_function_def():
                arg_names = defi.get_name_pointer().get_arg(keyword.arg)
                if not arg_names:
                    continue
                for name in arg_names:
                    arg_def = self.def_manager.get(name)
                    if not arg_def:
                        continue
                    for d in decoded:
                        if isinstance(d, Definition):
                            arg_def.get_name_pointer().add(d.get_ns())
                        else:
                            arg_def.get_lit_pointer().add(d)
            else:
                for d in decoded:
                    if isinstance(d, Definition):
                        defi.get_name_pointer().add_arg(keyword.arg, d.get_ns())
                    else:
                        defi.get_name_pointer().add_lit_arg(keyword.arg, d)

    # def retrieve_subscript_names(self, node):
    #     if not isinstance(node, ast.Subscript):
    #         raise Exception("The node is not an subcript")
    #
    #
    #     if getattr(node.slice, "value", None) is not None and self._is_literal(node.slice.value):
    #         sl_names = [node.slice.value]
    #     else:
    #         sl_names = self.decode_node(node.slice)
    #
    #     val_names = self.decode_node(node.value)
    #
    #     decoded_vals = set()
    #     keys = set()
    #     full_names = set()
    #     # get all names associated with this variable name
    #     for n in val_names:
    #         if n and isinstance(n, Definition):
    #             # decoded_vals |= self.closured.get(n.get_ns())
    #             decoded_vals.add(n.get_ns())
    #     for s in sl_names:
    #         if isinstance(s, Definition):
    #             keys.add(s.get_ns())
    #             # for name in self.closured.get(s.get_ns()):
    #             #     defi = self.def_manager.get(name)
    #             #     if not defi:
    #             #         continue
    #             #     keys |= defi.get_lit_pointer().get()
    #         elif isinstance(s, str):
    #             keys.add(s)
    #         elif isinstance(s, int):
    #             keys.add(s)
    #
    #     for d in decoded_vals:
    #         for key in keys:
    #             # check for existence of var name and key combination
    #             str_key = str(key)
    #             if isinstance(key, int):
    #                 # str_key = utils.get_int_name(key)
    #                 str_key = key
    #             full_ns = utils.join_ns(d, str_key)
    #             full_names.add(full_ns)
    #
    #
    #     return full_names

    def retrieve_subscript_names(self, node, literFlag=False):
        if not isinstance(node, ast.Subscript):
            raise Exception("The node is not an subcript")
        if getattr(node.slice, "value", None) is not None and self._is_literal(node.slice.value):
            sl_names = [node.slice.value]
        else:
            sl_names = self.decode_node(node.slice)

        val_names = self.decode_node(node.value)

        decoded_vals = set()
        keys = set()
        full_names = set()
        # get all names associated with this variable name
        for n in val_names:
            if n and isinstance(n, Definition):
                # decoded_vals |= self.closured.get(n.get_ns())
                decoded_vals.add(n.get_ns())
        for s in sl_names:
            if isinstance(s, Definition):
                keys.add(s.get_ns())
            elif isinstance(s, str):
                keys.add(s)
            elif isinstance(s, int):
                keys.add(s)
        returnDefins = set()
        for d in decoded_vals:
            definsList = self.resolve(d, node.lineno)
            for defins in definsList:
                defi: Definition = self.def_manager.get(defins)
                if defi and defi.get_type() in [utils.constants.LIST_DEF, utils.constants.MAP_DEF]:
                    if hasattr(defi, 'memo'):
                        defiList = set(reduce(lambda x, y: x + y, defi.memo.values()))

                        # defiList = set(map(lambda x:self.resolveList(x,node.lineno),defiList))
                        returnDefins = returnDefins.union(defiList)
            # for key in keys:
            #     # check for existence of var name and key combination
            #     definsList = self.resolve(d,node.lineno)
            #     for defins in definsList:
            #         defi:Definition = self.def_manager.get(defins)
            #         if defi and defi.get_type() == utils.constants.LIST_DEF:
            #             # defi:Definition = self.def_manager.get(defins)
            #             # if not defi:
            #             #     continue
            #             defiList = defi.get_element(key)
            #             # defiList = set(map(lambda x:self.resolveList(x,node.lineno),defiList))
            #             returnDefins = returnDefins.union(set(defiList))

        return returnDefins

        # return full_names

    def retrieve_call_names(self, node):
        names = set()
        if isinstance(node.func, ast.Name):
            defi = self.scope_manager.get_def(self.current_ns, node.func.id)
            if defi:
                names = self.closured.get(defi.get_ns(), None)
        elif isinstance(node.func, ast.Call) and self.last_called_names:
            for name in self.last_called_names:
                return_ns = utils.join_ns(name, utils.constants.RETURN_NAME)
                returns = self.closured.get(return_ns)
                if not returns:
                    continue
                for ret in returns:
                    defi = self.def_manager.get(ret)
                    names.add(defi.get_ns())
        elif isinstance(node.func, ast.Attribute):
            names = self._retrieve_attribute_names(node.func)
        elif isinstance(node.func, ast.Subscript):
            # Calls can be performed only on single indices, not ranges
            full_names = self.retrieve_subscript_names(node.func)
            for n in full_names:
                if self.closured.get(n, None):
                    names |= self.closured.get(n)

        return names

    def analyze_submodules(self, cls, *args, **kwargs):
        imports = self.import_manager.get_imports(self.modname)

        for imp in imports:
            self.analyze_submodule(cls, imp, *args, **kwargs)

    def analyze_submodule(self, cls, imp, *args, **kwargs):
        if imp in self.get_modules_analyzed():
            return

        fname = self.import_manager.get_filepath(imp)
        if not fname:
            return
        if fname.endswith(".so"):
            return
        # if not fname or not self.import_manager.get_mod_dir() in fname:
        #     return

        self.import_manager.set_current_mod(imp, fname)

        visitor = cls(fname, imp, *args, **kwargs)
        visitor.analyze()
        self.merge_modules_analyzed(visitor.get_modules_analyzed())

        # self.import_manager.set_current_mod(self.modname, self.filename)
        self.setMod()
    def setMod(self):
        imp = self.module_manager.get(self.get_module_ns(self.current_ns))
        if not imp:
            print()
        self.import_manager.set_current_mod(imp.name, imp.filename)
    def find_cls_fun_ns(self, cls_name, fn):
        cls = self.class_manager.get(cls_name)
        if not cls:
            return set()

        ext_names = set()
        for item in cls.get_mro():
            ns = utils.join_ns(item, fn)
            names = set()
            if getattr(self, "closured", None) and self.closured.get(ns, None):
                names = self.closured[ns]
            else:
                names.add(ns)

            if self.def_manager.get(ns):
                return names

            parent = self.def_manager.get(item)
            if parent and parent.get_type() == utils.constants.EXT_DEF:
                ext_names.add(ns)

        for name in ext_names:
            self.def_manager.create(name, utils.constants.EXT_DEF)
            self.add_ext_mod_node(name)
        return ext_names

    def add_ext_mod_node(self, name):
        ext_modname = name.split(".")[0]
        ext_mod = self.module_manager.get(ext_modname)
        if not ext_mod:
            ext_mod = self.module_manager.create(ext_modname, None, external=True)
            ext_mod.add_method(ext_modname)

        ext_mod.add_method(name)
