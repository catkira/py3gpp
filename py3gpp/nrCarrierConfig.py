_default_dict = {
    "NCellId" : 1,
    "SubcarrierSpacing" : 15,
    "CyclicPrefix" : 'normal',
    "NSizeGrid" : 52,
    "NStartGrid" : 0,
    "NSlot" : 0,
    "NFrame" : 0
}


def nrCarrierConfig(arg_dict = None):
    if arg_dict == None:
        return _default_dict
    return _default_dict | arg_dict