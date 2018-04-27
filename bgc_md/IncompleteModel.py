# vim:set ff=unix expandtab ts=4 sw=4:
from .Model import Model
import yaml

class IncompleteModel(Model):
    # the purpose of this class is to avoid complete initialization by Models __init__   
    # so that we can test part of the functionality wihtout
    # the necessity to provide all the parameters of a full model 

    def __init__(self, yaml_str,name="from_string"):
        self.complete_dict = yaml.load(yaml_str)
        self.name=name


