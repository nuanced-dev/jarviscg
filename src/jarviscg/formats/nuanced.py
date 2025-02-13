from .base import BaseFormatter

class Nuanced(BaseFormatter):
    def __init__(self, cg_generator):
        self.cg_generator = cg_generator

    def generate(self):
        output = self.cg_generator.output()
        output_cg = {}
        for node in output:
            output_cg[node] = list(output[node])
        return output_cg
