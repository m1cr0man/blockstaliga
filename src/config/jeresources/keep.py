import json

with open('world-gen.json', 'r') as gen_file:
    data = json.load(gen_file)

new_data = [
    block for block in data if
    print('Keep', block['block']) or
    'ore' in block['block'] or
    input().lower() == 'y'
]

print('saving')
with open('new-world-gen.json', 'w') as gen_file:
    json.dump(sorted(new_data, key=lambda x: x['block']), gen_file)

print('done')
