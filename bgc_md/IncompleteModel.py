# vim:set ff=unix expandtab ts=4 sw=4:
from .Model import Model
import yaml

class IncompleteModel(Model):
    # the purpose of this class is to avoid complete initialization by Models __init__   
    # so that we can test part of the functionality wihtout
    # the necessity to provide all the parameters of a full model 

    def __init__(self 
                 ,yaml_str
                 ,id="fromString"  #something to defer the output filename from, change if you want to compare different incomplete models
                ):
        # if a model is created directly from a string (e.g. in tests) it does not have
        # a filename that could serve as an id in a folder 
        # To distinguish the different such models from each other an id has to be given manually
        self.complete_dict = yaml.load(yaml_str)
        self.id=id


