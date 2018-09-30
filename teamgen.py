import functools
import itertools
import json
import random
import requests

SUBS = {
    'I': 'Y',
    'Y': 'I',
    'X': 'Z',
    'Z': 'X',
    'W': 'U'
}

def invert_dict(d):
    return {v: k for k, v in d.items()}


def get_data():
    r = requests.get('https://api.color.pizza/v1/')
    full_data = json.loads(r.content.decode())
    # full_data = {'colors': [{'name': ..., 'hex': ..., ...}]}

    # filter data according to single words
    data = [color for color in full_data['colors'] if ' ' not in color['name'] and '-' not in color['name']]
    
    return data

def get_random_teams(k=10):
    colors = get_data()
    n = len(colors)
    for i in random.sample(range(n), k):
        color = colors[i]
        try:
            name = ''.join(str(e).upper() for e in random.sample(color['name'], 4))
            yield name, color['name'], color['hex']
        except ValueError:
            pass

def substitute(letter_set: set):
    result = letter_set.copy()
    for k, v in SUBS.items():
        if k in letter_set:
            result.add(v)
    
    return result

def teamgen(c1, c2, c3, c4, allow_subs=True, fix_leader=False):
    
    # original letter sets
    o1 = set(c.upper() for c in c1)
    o2 = set(c.upper() for c in c2)
    o3 = set(c.upper() for c in c3)
    o4 = set(c.upper() for c in c4)
    osets = [s for s in (o1, o2, o3, o4) if s]       # ignore any empty sets
    original = functools.reduce(lambda s, t: s.union(t), osets)

    if allow_subs:
        ssets = [substitute(o) for o in osets]       # "sub" sets (i.e. sets with substitutions)
        options = itertools.product(*ssets)
    else:
        options = itertools.product(*osets)

    colors = get_data()
    for opt in options:
        tup = tuple(x.upper() for x in opt)
        
        if fix_leader:
            start_tup = tuple(c1 if allow_subs else o1)
        else:
            start_tup = tup

        for color in colors:
            name = color['name'].upper()
            if all(name.count(x) == 1 for x in tup):
                if len(osets) < 4 or name.startswith(start_tup):
                    # we want to include all matches for team size < 4
                    # but if all four names are given, the name has to start with one of those letters
                    team = ''.join(sorted(tup, key=lambda s: name.index(s)))

                    if allow_subs:
                        invsub = invert_dict(SUBS)
                        for letter in team:
                            if letter not in original:
                                team = team.replace(letter, invsub[letter])

                    yield team, color['name'], color['hex']
