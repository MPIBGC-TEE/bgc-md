import csv
def cable_dict(p):
    with p.open(newline='') as f:
        r=csv.DictReader(f,delimiter=",")
        lindicts=[row for row in r]
    return {key.strip():float(val) for key,val in lindicts[0].items()}
