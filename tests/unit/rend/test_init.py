# -*- coding: utf-8 -*-
'''
    tests.unit.rend.init
    ~~~~~~~~~~~~~~

    Tests for unit.rend.init
'''

# Import python libs
import os
import pytest
import sys

# Import local libs
import rend.exc

FDIR = os.path.join(os.path.dirname(sys.path[0]), 'files')


def test_rend_parse_jinja_exc(prep_hub):
    '''
    test rend.init.parse when RendererException
    raised with jinja renderer
    '''
    fn_ = os.path.join(FDIR, 'test_exc.jinja2')
    with pytest.raises(rend.exc.RenderException) as exc:
        prep_hub.rend.init.parse(fn_, 'jinja')
    assert exc.value.args[0] == "Jinja syntax error Encountered unknown tag 'test_exc'."

def test_rend_parse_yaml_exc(prep_hub):
    '''
    test rend.init.parse when RendererException
    raised with yaml renderer
    '''
    fn_ = os.path.join(FDIR, 'test_exc.yaml')
    with pytest.raises(rend.exc.RenderException) as exc:
        prep_hub.rend.init.parse(fn_, 'yaml')
    assert exc.value.args[0] == "Yaml render error: found undefined tag handle '!-!'"

def test_rend_parse_toml_exc(prep_hub):
    '''
    test rend.init.parse when RendererException
    raised with toml renderer
    '''
    fn_ = os.path.join(FDIR, 'test_exc.toml')
    with pytest.raises(rend.exc.RenderException) as exc:
        prep_hub.rend.init.parse(fn_, 'toml')
    assert exc.value.args[0] == "Toml render error: Empty value is invalid"


def test_blocks(prep_hub):
    '''
    Test that the block seperation and rendering works
    '''
    fn = os.path.join(FDIR, 'test.sls')
    data = prep_hub.rend.init.blocks(fn)
    for ref, block in data.items():
        if ref == 'raw':
            assert not block['bytes']
            assert block['ln'] == 0
            continue
        if block['ln'] == 3:
            assert block['keys'] == {'require': 'red'}
            assert block['bytes'] == b'red:\n  rum: 5\n'
        if block['ln'] == 6:
            assert block['pipe'] == [b'toml']
        if ref != 'raw' and block['ln'] == 0:
            assert block['keys'] == {'require': 'cheese'}
            assert block['bytes'] == b'foo:\n  bar: baz\n'


def test_blocks_nest(prep_hub):
    '''
    Test that the block seperation and rendering works
    '''
    fn = os.path.join(FDIR, 'nest.sls')
    data = prep_hub.rend.init.blocks(fn)
    for ref, block in data.items():
        if ref == 'raw':
            assert block['bytes'] == b'raw: True\n'
            assert block['ln'] == 0
            continue
        if block['ln'] == 3:
            assert block['keys'] == {'require': 'red'}
            assert block['bytes'] == b'red:\n  rum: 5\n'
        if ref != 'raw' and block['ln'] == 0:
            assert block['keys'] == {'require': 'cheese'}
            assert block['bytes'] == b'foo:\n  bar: baz\n'


def test_blocks_end(prep_hub):
    '''
    Test that the block seperation and rendering works
    '''
    fn = os.path.join(FDIR, 'end.sls')
    data = prep_hub.rend.init.blocks(fn)
    for ref, block in data.items():
        if ref == 'raw':
            assert not block['bytes']
            assert block['ln'] == 0
            continue
        if block['ln'] == 3:
            assert block['keys'] == {'require': 'red'}
            assert block['bytes'] == b'red:\n  rum: 5\n'
        if ref != 'raw' and block['ln'] == 0:
            assert block['keys'] == {'require': 'cheese'}
            assert block['bytes'] == b'foo:\n  bar: baz\n'


def test_blocks_each(prep_hub):
    '''
    Test that the block seperation and rendering works
    '''
    fn = os.path.join(FDIR, 'each_end.sls')
    data = prep_hub.rend.init.blocks(fn)
    for ref, block in data.items():
        if ref == 'raw':
            assert not block['bytes']
            assert block['ln'] == 0
            continue
        if block['ln'] == 3:
            assert block['keys'] == {'require': 'red'}
            assert block['bytes'] == b'red:\n  rum: 5\n'
        if ref != 'raw' and block['ln'] == 0:
            assert block['keys'] == {'require': 'cheese'}
            assert block['bytes'] == b'foo:\n  bar: baz\n'


def test_blocks_bad_end(prep_hub):
    '''
    Test that the block seperation and rendering works
    '''
    fn = os.path.join(FDIR, 'bad_end.sls')
    with pytest.raises(rend.exc.RenderException) as exc:
        data = prep_hub.rend.init.blocks(fn)
    assert exc.value.args[0] == 'Unexpected End of file line 8'
