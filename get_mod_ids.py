import requests, sys, re, os, json

API_ROOT = 'https://staging_cursemeta.dries007.net/api/v3/direct'
GAME_ID = 432

def find_mod(filename: str):
    # Find a sanitised version of the filename to search against
    modmatch = r'^([a-z_\-]+[a-z])[\_\-]'
    if not re.match(modmatch, filename):
        return
    regname = re.match(modmatch, filename).group(1)

    capitalised = re.sub(r'[_-]?([B-Z]+|A)', r' \1', regname).lstrip()
    capitalised = re.sub(r'[_-]([a-z])', r' \1', capitalised).lstrip()

    modnames = [
        capitalised.lower(),
        regname,
        capitalised.split()[0],
        capitalised.split()[-1]
    ]

    # Search for the (unique) possibilities
    for modname in set(modnames):
        mods = requests.get(API_ROOT + '/addon/search', params={
            'gameId': GAME_ID,
            'searchFilter': modname
        }).json()

        for mod in mods:
            if mod['name'].lower() in modnames:
                return mod

            for modfile in mod['latestFiles']:
                if modfile['fileNameOnDisk'].lower() == filename:
                    return mod

                online_modname = re.match(modmatch, modfile['fileNameOnDisk'], flags=re.IGNORECASE)

                if online_modname and online_modname.group(1).lower() in modnames:
                    return mod

    print(modnames)

def main():
    j = os.path.join
    folder = sys.argv[1]

    for filename in sorted(os.listdir(folder)):
        if '.meta.json' in filename:
            continue
        metapath = j(folder, filename + '.meta.json')
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
