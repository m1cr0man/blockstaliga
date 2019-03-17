import sys, re, os, json
import requests

MODID_REGEX = r'.*MODID(\d+)'
API_ROOT = 'https://staging_cursemeta.dries007.net/api/v3/direct'
GAME_ID = 432

def inlist_ignorecase(a: str, l: [str]):
    return a in l or a.lower() in l


def find_by_id(filename: str):
    # Check filename for an id
    id_exp = re.match(MODID_REGEX, filename, flags=re.IGNORECASE)
    if not id_exp:
        return None

    return requests.get(API_ROOT + '/addon/{}'.format(id_exp.group(1))).json()

def find_mod(filename: str):
    mod_by_id = find_by_id(filename)
    if mod_by_id:
        return mod_by_id

    # Find a sanitised version of the filename to search against
    modmatch = r'^([a-z_\-]+[a-z])[\_\-]'
    regname_exp = re.match(modmatch, filename, flags=re.IGNORECASE)
    if not regname_exp:
        print('Couldnt parse filename')
        return None
    regname = regname_exp.group(1)

    # Prettify the mod name
    capitalised = re.sub(r'[_-]?([B-Z]+|A)', r' \1', regname).lstrip()
    capitalised = re.sub(r'[_-]([a-zA-Z])', r' \1', capitalised).lstrip()

    # Make a set of the possible names
    modnames = {
        capitalised.lower(),
        regname,
        capitalised.split()[0],
        capitalised.split()[-1]
    }

    # Search for the possibilities
    for modname in modnames:
        mods = requests.get(API_ROOT + '/addon/search', params={
            'gameId': GAME_ID,
            'searchFilter': modname
        }).json()

        for mod in mods:
            # Exact match of mod name against possibilities
            if inlist_ignorecase(mod['name'], modnames):
                return mod

            for modfile in mod['latestFiles']:
                # Exact match of file name on disk
                if modfile['fileNameOnDisk'].lower() == filename.lower():
                    return mod

                online_modname = re.match(modmatch, modfile['fileNameOnDisk'], flags=re.IGNORECASE)

                # Match of online mod name from filename against possibilities
                if online_modname and inlist_ignorecase(online_modname.group(1), modnames):
                    return mod

    print(modnames)
    return None

def main():
    j = os.path.join
    folder = sys.argv[1]

    for filename in sorted(os.listdir(folder)):
        if '.meta.json' in filename:
            continue
        metapath = j(folder, re.sub(r'\.jar', '.meta.json', filename))
        if os.path.exists(metapath):
            continue

        mod = find_mod(filename)

        if not mod:
            print(filename, 'source mod not found')
            continue

        print('found', filename, '->', mod['id'])
        with open(metapath, 'w') as metafile:
            json.dump(mod, metafile)

if __name__ == '__main__':
    main()
