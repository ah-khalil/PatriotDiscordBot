def iterate_items(subject_dict, search_dict):
    subject_item = search_dict.__iter__().__next__()

    if subject_item in subject_dict:
        if isinstance(subject_dict[subject_item], dict):
            subject_dict[subject_item] = iterate_items(subject_dict[subject_item], search_dict[subject_item])
        else:
            subject_dict[subject_item] = search_dict[subject_item]
            return subject_dict
    else:
        subject_dict[subject_item] = search_dict[subject_item]
    return subject_dict

def keys_exists(element, *keys):
    '''
    Check if *keys (nested) exists in `element` (dict).
    '''
    if type(element) is not dict:
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False

    return True