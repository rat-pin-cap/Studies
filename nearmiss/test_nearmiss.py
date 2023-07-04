def test_fullstring(nms):
    test_dict = {
        1: [nms.get_regexcompiledregex("tEs"),"tested"],
        2: [nms.get_regexcompiledregex("tEs"),"teestEd"],
        3: [nms.get_regexcompiledregex("tEs"),"teweted"],
        4: [nms.get_regexcompiledregex("Bari Etchi"), "Bari Etchi"],
        5: [nms.get_regexcompiledregex("Bari Etchi"), "Barri Etcchi"],
        6: [nms.get_regexcompiledregex("Bari Etchi"), "Barrui Errchi"],
        7: [nms.get_regexcompiledregex("2022 triumph street triple"), "2022 triumph street triple"],
        8: [nms.get_regexcompiledregex("2022 triumph street triple"), "2022triuumph streeeet  trriple"],
        9: [nms.get_regexcompiledregex("2022 triumph street triple"), "201222 triunjphastreet tripople"],
        10: [nms.get_regexcompiledregex("a"),'a'],
        11: [nms.get_regexcompiledregex("a"),'q'],
        12: [nms.get_regexcompiledregex("a"),'aS'],
        13: [nms.get_regexcompiledregex("a"),'l'],
    }
    for i in test_dict.keys():
        assert test_dict[i][0].search(test_dict[i][1]) != None


def test_singlekeys(nms):
    assert nms.find_keycluster("Z") == {('z', None): [('a', None), ('x', None), ('s', None)]}
    assert nms.find_keycluster("d") == {('d', None): [('s', None), ('e', None), ('x', None), ('f', None), ('r', None), ('c', None)]}
    assert nms.find_keycluster("h") == {('h', None): [('g', None), ('y', None), ('b', None), ('j', None), ('u', None), ('n', None)]}
    assert nms.find_keycluster("\\") == {('\\', '|'): [(']', '}')]}
    assert nms.find_keycluster("|") == {('\\', '|'): [(']', '}')]}
    assert nms.find_keycluster("=") == {('=', '+'): [('-', '_'), ('[', '{'), (']', '}')]}
    assert nms.find_keycluster("/") == {('/', '?'): [('.', '>'), (';', ':'), ("'", '"')]}
    assert nms.find_keycluster("6") == {('6', '^'): [('5', '%'), ('t', None), ('7', '&'), ('y', None)]}
    assert nms.find_keycluster("`") == {('`', '~'): [('1', '!')]}
    assert nms.find_keycluster("*") == {('8', '*'): [('7', '&'), ('u', None), ("9", '('), ("i", None)]}



def master_test():
    import Nearmiss_search as nms
    fails = []
    #test_fullstring(nms)
    try:
        test_fullstring(nms)
    except AssertionError as ae:
        ae.args += ("Long KB fail.", "NMS") #when capturing exceptions, add a tuple containing where the failure occured and what module so the master displays this info
        fails.append(ae.args)
    try:
        test_singlekeys(nms)
    except AssertionError as ae:
        ae.args += ("short KB fail.", "NMS")
        fails.append(ae.args)
    return fails

out = master_test()
print("success") if out == [] else print("fail:\n\t"+str(out))