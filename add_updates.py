import os, re, shutil, sys

MOD_MATCHER = r'^[a-z\-_]+'
j = os.path.join

def get_mod_name(fname: str):
    match = re.match(MOD_MATCHER, fname, flags=re.IGNORECASE)
    return match and match.group(0) or ''

def main():
    folder = sys.argv[1]

    existing_files = {get_mod_name(fname) for fname in os.listdir(folder)}
    updates = {get_mod_name(fname) for fname in os.listdir('updates')}

    print('\n'.join(existing_files.intersection(updates)))

    for update in updates:
        # rename old file
        for fname in os.listdir(folder):
            if get_mod_name(fname) == update and '.old' not in fname:
                os.rename(j(folder, fname), j(folder, fname + '.old'))

    # copy in new files
    for fname in os.listdir('updates'):
        shutil.move(j('updates', fname), j(folder, fname))

if __name__ == '__main__':
    main()
