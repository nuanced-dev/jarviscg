import os
from jarviscg.formats.base import BaseFormatter
from jarviscg import utils

class Nuanced(BaseFormatter):
    def __init__(self, cg_generator, *, relpath=None):
        self.relpath = relpath
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

        if self.relpath:
            dir_parts = self.relpath.split("/")
            last_dir = dir_parts.pop()
            relpath_prefix = ".".join(dir_parts)

            return {
                self._transform_name(name, relpath_prefix, last_dir): {
                    **attrs,
                    "callees": [self._transform_name(callee, relpath_prefix, last_dir) for callee in attrs["callees"]]
                }
                for name, attrs in output.items()
                if name.split(".")[0] == last_dir
            }
        else:
            return output

    def _transform_name(self, name, relpath_prefix, last_dir):
        if name.split(".")[0] == last_dir:
            return utils.join_ns(relpath_prefix, name)
        else:
            return name
