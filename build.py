#!/usr/bin/python3
import sys
import os
import shutil
import subprocess
import tempfile
import venv

NAME = 'rend'

cwd = os.getcwd()
spec_fn = os.path.join(cwd, f'{NAME}.spec')
def to_import(path): 
    ret = path[path.index('site-packages') + 14:].replace(os.sep, '.')
    if ret.endswith('.py'):
        ret = ret.rstrip('.py')
    return ret


SPEC = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

def Entrypoint(dist, group, name, **kwargs):
    import pkg_resources

    # get toplevel packages of distribution from metadata
    def get_toplevel(dist):
        try:
            distribution = pkg_resources.get_distribution(dist)
        except:
            return []
        if distribution.has_metadata('top_level.txt'):
            return list(distribution.get_metadata('top_level.txt').split())
        else:
            return []

    kwargs.setdefault('hiddenimports', %%IMPORTS%%)
    packages = []
    for distribution in kwargs['hiddenimports']:
        packages += get_toplevel(distribution)

    kwargs.setdefault('pathex', [])
    # get the entry point
    ep = pkg_resources.get_entry_info(dist, group, name)
    assert ep, 'Could not find the entry point'
    # insert path of the egg at the verify front of the search path
    kwargs['pathex'] = [ep.dist.location] + kwargs['pathex']
    # script name must not be a valid module name to avoid name clashes on import
    script_path = os.path.join(workpath, name + '-script.py')
    print("creating script for entry point", dist, group, name)
    with open(script_path, 'w') as fh:
        print("import", ep.module_name, file=fh)
        print("%s.%s()" % (ep.module_name, '.'.join(ep.attrs)), file=fh)
        for package in packages:
            print("import", package, file=fh)

    return Analysis(
        [script_path] + kwargs.get('scripts', []),
        **kwargs
    )

a = Entrypoint('%%NAME%%', 'console_scripts', '%%NAME%%')

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='%%NAME%%',
          debug=True,
          bootloader_ignore_signals=False,
          onefile=True,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=True,
               upx=True,
               upx_exclude=[],
               name='%%NAME%%')
'''


# Make a virtual environment based on the version of python used to call this script
venv_dir = tempfile.mkdtemp(prefix='pop_', suffix='_venv')
venv.create(venv_dir, clear=True, with_pip=True)
python_bin = os.path.join(venv_dir, 'bin', 'python')
pip_bin = os.path.join(venv_dir, 'bin', 'pip')

# Install dependencies
subprocess.Popen([pip_bin, 'install', '-r', 'requirements.txt']).wait()
subprocess.Popen([pip_bin, 'install', 'PyInstaller']).wait()
subprocess.Popen([pip_bin, '-v', 'install', cwd]).wait()
vroot = os.path.join(venv_dir, 'lib')
all_paths = set()
for root, dirs, files in os.walk(vroot):
    if 'PyInstaller' in root:
        continue
    if 'pip' in root:
        continue
    if '__pycache__' in root:
        continue
    for d in dirs:
        full = os.path.join(root, d)
        if '__pycache__' in full:
            continue
        all_paths.add(full)
    for f in files:
        full = os.path.join(root, f)
        if '__pycache__' in full:
            continue
        all_paths.add(full)
imports = set()
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
        imp = to_import(path)
        if imp:
            imports.add(imp)


# Run pyinstaller from the virtual environment to create the script
s_path = os.path.join(venv_dir, 'bin', NAME)
cmd = f'{python_bin} -B -OO -m PyInstaller '
pyi_args = [
          '--log-level=INFO',
          '--noconfirm',
          '--onefile',
          '--clean',
          f'{spec_fn}'
        ]
imp_line = '['

SPEC = SPEC.replace('%%NAME%%', NAME)
for imp in imports:
    imp_line += f"'{imp}', "
imp_line += ']'
SPEC = SPEC.replace('%%IMPORTS%%', imp_line)
with open(spec_fn, 'w+') as wfh:
    wfh.write(SPEC)
for arg in pyi_args:
    cmd += f'{arg} '
subprocess.call(cmd, shell=True)


print(cmd)
print(f'venv created in {venv_dir}')
print('Executable created in {}'.format(os.path.join(cwd, 'dist', NAME)))
#shutil.rmtree(venv_dir)
