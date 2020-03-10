import yaml
import os
import sys
from shutil import copyfile

try:
    with open('mappings.yml', 'rb') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
except yaml.YAMLError as exc:
    print("Failed to parse mappings.yaml", file=sys.stderr)
    sys.exit(2)
except:
    print("Failed to read mappings.yaml", file=sys.stderr)
    sys.exit(2)

path = config['path']
files = config['files']
text = config['text']
exclude = config['exclude']
errors = False

def is_excluded(filepath, exclude=exclude):
    for e in exclude:
        if e == filepath:
            return True
    return False

print("Checking path " + path)
if not os.path.isdir(path):
    print(path + " doesn't exist or it's not a directory", file=sys.stderr)
    sys.exit(2)

print("Excluding: " + str(exclude))

for f in files:
    if is_excluded(f):
        continue
    if not os.path.isfile(os.path.join(path, f['dst'])):
        print("Missing destination file: " + os.path.join(path, f['dst']), file=sys.stderr)
        errors = True
    if not os.path.isfile(f['src']):
        print("Missing source file: " + f['src'], file=sys.stderr)
        errors = True

for t in text:
    if is_excluded(t['file']):
        continue
    if not os.path.isfile(os.path.join(path, t['file'])):
        print("Missing destination file: " + t['file'], file=sys.stderr)
        errors = True

if errors:
    print("\n^^^\nPlease fix errors above before proceeding")
    sys.exit(2)

for f in files:
    if is_excluded(f):
        continue
    print("Replacing file: " + f['dst'] + " with " + f['src'])
    try:
        copyfile(f['src'], os.path.join(path, f['dst']))
    except:
        print("Failed to replace " + f['dst'])

for t in text:
    if is_excluded(f):
        continue
    print("Replacing text in " + t['file'] + ": " + t['text'] + " -> " + t['replace'])
    with open(os.path.join(path, t['file']), 'r') as file :
        contents = file.read()
    contents = contents.replace(t['text'], t['replace'])
    try:
        with open(os.path.join(path, t['file']), 'w') as file:
            file.write(contents)
    except:
        print("Failed to replace text in " + t['file'], file=sys.stderr)
