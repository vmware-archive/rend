#!/usr/bin/python3
import sys
import os
import shutil
import subprocess
import tempfile
import venv

NAME = 'rend'

cwd = os.getcwd()
run = os.path.join(cwd, 'run.py')
def to_import(path): 
    ret = path[path.index('site-packages') + 14:].replace(os.sep, '.')
    if ret.endswith('.py'):
        ret = ret[:-3]
    return ret


def to_data(path):
    dest = path[path.index('site-packages') + 14:]
    src = path
    if not dest.strip():
        return None
    ret = f'{src}{os.pathsep}{dest}'
    return ret


# Make a virtual environment based on the version of python used to call this script
venv_dir = tempfile.mkdtemp(prefix='pop_', suffix='_venv')
venv.create(venv_dir, clear=True, with_pip=True)
python_bin = os.path.join(venv_dir, 'bin', 'python')
pip_bin = os.path.join(venv_dir, 'bin', 'pip')

# Install dependencies
subprocess.call([pip_bin, 'install', '-r', 'requirements.txt'])
subprocess.call([pip_bin, 'install', 'PyInstaller'])
subprocess.call([pip_bin, '-v', 'install', cwd])
vroot = os.path.join(venv_dir, 'lib')
all_paths = set()
for root, dirs, files in os.walk(vroot):
    if 'PyInstaller' in root:
        continue
    if 'pip' in root:
        continue
    if 'setuptools' in root:
        continue
    if 'pkg_resources' in root:
        continue
    if '__pycache__' in root:
        continue
    for d in dirs:
        full = os.path.join(root, d)
        if '__pycache__' in full:
            continue
        if 'dist-info' in full:
            continue
        if 'egg-info' in full:
            continue
        all_paths.add(full)
    for f in files:
        full = os.path.join(root, f)
        if '__pycache__' in full:
            continue
        if 'dist-info' in full:
            continue
        if 'egg-info' in full:
            continue
        all_paths.add(full)
imports = set()
datas = set()
for path in all_paths:
    if not 'site-packages' in path:
        continue
    if os.path.isfile(path):
        if not path.endswith('.py'):
            continue
        if path.endswith('__init__.py'):
            # Skip it, we will get the dir
            continue
        imp = to_import(path)
        if imp:
            imports.add(imp)
    if os.path.isdir(path):
        data = to_data(path)
        imp = to_import(path)
        if imp:
            imports.add(imp)
        if data:
            datas.add(data)


# Run pyinstaller from the virtual environment to create the script
s_path = os.path.join(venv_dir, 'bin', NAME)
shutil.copy(run, s_path)
cmd = f'{python_bin} -B -OO -m PyInstaller '
pyi_args = [
          s_path,
          '--log-level=INFO',
          '--noconfirm',
          '--onefile',
          '--clean',
        ]

for imp in imports:
    pyi_args.append(f'--hidden-import={imp}')
for data in datas:
    pyi_args.append(f'--add-data={data}')
for arg in pyi_args:
    cmd += f'{arg} '
subprocess.call(cmd, shell=True)


print(cmd)
print(f'venv created in {venv_dir}')
print('Executable created in {}'.format(os.path.join(cwd, 'dist', NAME)))
#shutil.rmtree(venv_dir)
