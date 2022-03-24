import copy


def mergedicts(dict1, dict2, parent_dict={}, parent_key=""):
    if isinstance(dict1, dict):
        for k in dict1:
            if k in dict2:
                mergedicts(dict1[k], dict2[k], dict2, k)
            else:
                dict2[k] = {}
                mergedicts(dict1[k], dict2[k], dict2, k)
    # dict1 is a value, so we add it
    else:
        parent_dict[parent_key] = dict1


def _parse_data(inputdict, my_uuid):
    new_dict = {}
    total = {"first": {"val": 0, "edited": False}, "second": {"val": 0, "edited": False}}

    for key in inputdict.keys():
        if type(inputdict[key]) == dict:
            new_dict[key] = _parse_data(inputdict[key], my_uuid)
        else:
            print('key ' + str(key))
            print('inputdict' + str(inputdict[key]))
            if inputdict[key]:
                if not total['first']['edited']:
                    total['first']['val'] = inputdict[key]
                    total['first']['edited'] = True
                else:
                    total['second']['val'] = inputdict[key]
                    total['second']['edited'] = True
    if total['first']['edited'] and total['second']['edited']:

        new_dict = {my_uuid: ((total['second']['val'] - total['first']['val']) / total['first']['val'])}
    print('new dict ' + str(new_dict))
    return new_dict


def gen_average(inputdict, my_uuid):
    new_dict = {}
    total = 0
    for key in inputdict.keys():
        if type(inputdict[key]) == dict:
            new_dict[key] = _parse_data(inputdict[key], my_uuid)
        else:
            print('key ' + str(key))
            print('inputdict' + str(inputdict[key]))
            if inputdict[key]:
                total += inputdict[key]
    if total != 0:
        new_dict = {my_uuid: total / len(inputdict.keys())}
    print('new dict ' + str(new_dict))
    return new_dict

def flatten_and_discard(data, discard_keys=[], row_list=[]):
    """
    Flattens a dictionary and discards keys given by discard_keys
    :arg data: Input dicitionary to flatten
    :arg discard_keys: List of keys to discard
    :arg row_list: List to append the flattened dictionary
    """

    def inner_function(input_data, row=[]):
        last = False
        if isinstance(input_data, dict):
            for k in input_data:
                new_row = copy.deepcopy(row)
                if k not in discard_keys:
                    new_row.append(k)
                if not isinstance(input_data[k], dict):
                    row.append(input_data[k])
                    last = True
                else:
                    inner_function(input_data[k], new_row)
        if last:
            row_list.append(row)

    inner_function(data)


def extract_headers(compute_config, identifiers=[], aliases=[]):
    """
    Extracts the headers from a compute configuration
    :arg compute_config: Input compute configuration
    :arg identifiers: Identifier list
    :arg aliases: Alias list
    """
    compute_header = []
    if aliases:
        identifiers = aliases
    for key in compute_config.get("filter", []):
        compute_header.append(key.split(".keyword")[0])
    for bucket in compute_config.get("buckets", []):
        compute_header.append(bucket.split(".keyword")[0])
    for extra_h in ["metric"] + identifiers:
        compute_header.append(extra_h)
    return compute_header
