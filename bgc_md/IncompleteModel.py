# vim:set ff=unix expandtab ts=4 sw=4:
from .Model import Model
from .helpers import retrieve_this_or_that
import yaml

class IncompleteModel(Model):
    # the purpose of this class is to avoid complete initialization by Models __inti__   # so that we can test part of the functionality wihtout
    # the necessity to provide all the parameters of a full model 
    def __init__(self, yaml_str):
        self.complete_dict = yaml.load(yaml_str)

    @property
    def name(self):
        try:
            name=retrieve_this_or_that("name",  self.bibtex_entry.key, self.complete_dict)
        except Exception as e:
            print(e)
            if hasattr(self,"outsideName"):
                name=self.outsideName
            else:
                name="default"
        finally:
            return(name)    
                

