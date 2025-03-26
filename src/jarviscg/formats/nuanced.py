import os
from .base import BaseFormatter

class Nuanced(BaseFormatter):
    def __init__(self, cg_generator):
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

        return output
