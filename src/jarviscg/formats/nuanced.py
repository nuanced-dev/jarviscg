import os
from jarviscg.formats.base import BaseFormatter
from jarviscg import utils

class Nuanced(BaseFormatter):
    def __init__(self, cg_generator, *, scope_prefix=None):
        self.scope_prefix = scope_prefix
        self.cg_generator = cg_generator
        self.internal_mods = self.cg_generator.output_internal_mods() or {}
        self.edges = self.cg_generator.output_edges() or []

    def generate(self):
        output = {}

        for modname, module in self.internal_mods.items():
            for namespace, info in module["methods"].items():
                output[namespace] = {
                    "filepath": os.path.abspath(module["filename"]),
                    "callees": [],
                    "lineno": info["first"],
                    "end_lineno": info["last"],
                }

        for src, dst in self.edges:
            if src in output:
                output[src]["callees"].append(dst)

        if self.scope_prefix and not self.scope_prefix == ".":
            scopes = self.scope_prefix.split(".")
            last_scope = scopes.pop()
            prefix = ".".join(scopes)

            return {
                self._transform_name(name, prefix, last_scope): {
                    **attrs,
                    "callees": [self._transform_name(callee, prefix, last_scope) for callee in attrs["callees"]]
                }
                for name, attrs in output.items()
                if name.split(".")[0] == last_scope
            }
        else:
            return output

    def _transform_name(self, name, prefix, last_scope):
        if name.split(".")[0] == last_scope:
            return utils.join_ns(prefix, name)
        else:
            return name
