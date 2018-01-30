# vim:set ff=unix expandtab ts=4 sw=4:
import yaml
import datetime
def add_edit_date(yaml_file_path,datetimeObject):
    # fixme:
    # This function does not use the knowledge in Model
    # to write yaml files
    # It just dumps out the dictonary
    # thereby confusing the order of the entries
    # while we could define an order in which the dictionary
    # should be written it seems preferable 
    # to implement a dump_yaml method in Model (like a report)
    # This would give us much more control over the entries
    category="edits"
    
    with yaml_file_path.open("r") as f:
        yaml_str=f.read()
    
    complete_dict=yaml.load(yaml_str)
    date_list=complete_dict[category] 
    print(date_list[0])
    #print(date_list)
    #print(type(date_lis2t))
    new_edit={"time": datetimeObject,"user":"mm"}
    date_list.append(new_edit)
    print(date_list[1])
    complete_dict[category]=date_list
    #yaml_str=yaml.dump(complete_dict,canonical=True)
    yaml_str=yaml.dump(complete_dict,default_flow_style=False)
    #yaml_str=yaml.dump(complete_dict,default_flow_style=True)
    
    with yaml_file_path.open("w") as f:
        f.write(yaml_str) 

def add_last_edit_date(yaml_file_path):
    now=datetime.datetime.utcnow()
    add_edit_date(yaml_file_path,now)
    
