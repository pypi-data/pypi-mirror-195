import json
import csv
import logging
import event_dataframe as ev

logger=logging.getLogger()

poly_cols=["T", "F", "ID", "_P", "_V", "_L", "_R", "_T", "_W", "_X", "_Y", "_Z"]


def read_expr(expr, line):
    def read_val(val):
        try:
            ret=int(val)
        except ValueError:
            try:
                ret=float(val)
            except ValueError:
                try:
                    ret=int(line[poly_cols.index(val)])
                except ValueError:
                    raise RuntimeError("Unable to parse value. Perhaps invalid column name?")
        return ret
        
    if isinstance(expr, list):
        if len(expr)==3:
            (v1, op, v2) = (expr[0], expr[1], expr[2])
            if op == "=":
                (val1, val2) = (read_val(v1), read_val(v2))
                ret = val1==val2
                # logger.info("Ret of {} is {}. Items are {} {}. Line is {}".format(expr, ret, val1, val2, line))
            elif op == ">":
                (val1, val2) = (read_val(v1), read_val(v2))
                ret = val1>val2
            else:
                raise RuntimeError("Unhandled operator")
        else:
            raise RuntimeError("Unhandled list (need 3 items)")
    else:
        ret = read_val(expr)
    return ret

def interpret(channel, line):
    selected = channel["select"]
    if isinstance(selected, list):
        if not isinstance(selected[0], list):
            selected=[selected]
        ret = True
        for s in selected:
            if not read_expr(s, line):
                ret = False
                break
    if "value" in channel:
        return (ret, read_expr(channel["value"], line)) 
    else:           
        return (ret, None) 
    
def load(config_file, poly_data):

    with open(config_file) as config_file:
        poly_config = json.loads(config_file.read())
    

    data = ev.EventData()
    for channel in poly_config:
        data.add_channel(channel["name"], channel["type"])

    to_add=[]
    with open(poly_data, mode ='r') as file:
        csvFile = csv.reader(file, delimiter="\t")
        for line in csvFile:
            if len(line)==len(poly_cols):
                for channel in poly_config:
                    (selected, value) = interpret(channel, line)
                    if selected:
                        to_add.append({"T":float(line[0])/1000.0, "event_name":channel["name"], "value": value})

    data.add_events(to_add)
    return data