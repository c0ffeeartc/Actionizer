import os
from Step import Step
from model.options.Options import Options

__author__ = 'c0ffee'


class StepPool(object):
    step_files = None
    steps = []

    def __init__(self):
        self.reinit()

    def reinit(self):
        self.step_files = []
        for root, dirnames, filenames in os.walk(Options.path_to_steps):
            for filename in filenames:
                if filename.endswith(".jsx"):
                    self.step_files.append(os.path.join(root, filename))
        self.load_steps()

    def load_steps(self):
        for file_path_name in self.step_files:
            step = Step()
            self.steps.append(step)
            step.file_path_name = file_path_name
            with open(file_path_name, "r") as f:
                step.script = f.read()

    def get_step(self, **kwargs):
        """
        uses **kwargs
        """
        if "file_path_name" in kwargs.keys():
            for step in self.steps:
                if kwargs["file_path_name"] == step.file_path_name:
                    return step
