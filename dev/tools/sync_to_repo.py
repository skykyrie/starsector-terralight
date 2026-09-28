"""Copy the freshly built mod (dev/build/TerraLight) over the repo root and zip it for a GitHub Release.
Usage (from the repo root):  python3 dev/tools/sync_to_repo.py"""
import os, shutil, json, zipfile
DEV = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(DEV)
BUILT = os.path.join(DEV, 'build', 'TerraLight')
assert os.path.exists(os.path.join(BUILT, 'mod_info.json')), 'run dev/build_v11.py first'
for d in ('data', 'graphics'):
    shutil.rmtree(os.path.join(REPO, d), ignore_errors=True)
    shutil.copytree(os.path.join(BUILT, d), os.path.join(REPO, d))
for f in ('mod_info.json', 'README.txt'):
    shutil.copy(os.path.join(BUILT, f), os.path.join(REPO, f))
ver = json.load(open(os.path.join(BUILT, 'mod_info.json')))['version']
z = os.path.join(DEV, '_scratch', f'TerraLight_v{ver}.zip')
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, _, files in os.walk(BUILT):
        for fn in files:
            p = os.path.join(root, fn)
            zf.write(p, os.path.join('TerraLight', os.path.relpath(p, BUILT)))
print('repo updated to', ver, '| release zip:', z)
