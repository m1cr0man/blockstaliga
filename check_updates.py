import requests, sys, re, os, json

API_ROOT = 'https://staging_cursemeta.dries007.net/api/v3/direct'
GAME_ID = 432

if not os.path.exists('updates'):
    os.mkdir('updates')

def get_file(modid, fileId):
    try:
        res = requests.get(API_ROOT + '/addon/{}/file/{}'.format(modid, fileId))
    except Exception:
        print('Failed to download', fileData['downloadUrl'])
    return res.json()

def download_file(fileData):
    if os.path.exists('updates/' + fileData['fileNameOnDisk']):
        print('Skipping')
        return
    try:
        res = requests.get(fileData['downloadUrl'])
    except Exception:
        print('Failed to download', fileData['downloadUrl'])
        return
    with open('updates/' + fileData['fileNameOnDisk'], 'wb') as out_file:
        out_file.write(res.content)
        print('Downloaded')

def main():
    j = os.path.join
    folder = sys.argv[1]

    for filename in sorted(os.listdir(folder)):
        modname = filename.replace('.meta.json', '')
        if '.meta.json' in filename:
            with open(j(folder, filename)) as metafile:
                metadata = json.load(metafile)

            modid = metadata['id']
            latest = None

            # latest = sorted([f for f in metadata['latestFiles' if '1.12' in online_file['gameVersion']]], key='fileDate')[-1]

            # Iterate all files for this mod
            for online_file in metadata['gameVersionLatestFiles']:

                # Filter for 1.12.* only
                if '1.12' in online_file['gameVersion']:

                    # Check if this file is newer than latest
                    # if online_file['fileDate'] == sorted([latest['fileDate'], online_file['fileDate']])[0]:
                    if (not latest) or online_file['projectFileId'] > latest['projectFileId']:
                        latest = online_file

            if not latest:
                print('No updates for {}'.format(filename))
                continue

            latest_file = None
            modfname = latest['projectFileName']
            if '.jar' not in modfname:
                latest_file = get_file(modid, latest['projectFileId'])
                modfname = latest_file['fileNameOnDisk'].replace('.jar', '')

            if modfname.lower() != modname.lower():
                print(modname, '->', modfname)
                print('Downloading')
                if modfname + '.jar' in os.listdir('updates'):
                    continue
                download_file(latest_file or get_file(modid, latest['projectFileId']))

if __name__ == '__main__':
    main()
