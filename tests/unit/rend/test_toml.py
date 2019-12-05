# -*- coding: utf-8 -*-
'''
    tests.unit.rend.test_toml
    ~~~~~~~~~~~~~~

    Unit tests for the toml renderer
'''

# Import python libs
import pytest

# Import local libs
import rend.exc


@pytest.mark.asyncio
async def test_toml(prep_hub):
    '''
    test rend.toml.render renders correctly
    '''
    data = """
    # I promise this is toml data
    title = 'toml test'
    [owner]
    name = 'toml owner'
    """
    ret = await prep_hub.rend.toml.render(data)
    assert ret['title'] == 'toml test'
    assert ret['owner']['name'] == 'toml owner'


@pytest.mark.asyncio
async def test_toml_bytes(prep_hub):
    '''
    test rend.toml.render renders correctly with bytes data
    '''
    data = b"""
    # I promise this is toml data
    title = 'toml test'
    [owner]
    name = 'toml owner'
    """
    ret = await prep_hub.rend.toml.render(data)
    assert ret['title'] == 'toml test'
    assert ret['owner']['name'] == 'toml owner'


@pytest.mark.asyncio
async def test_toml_decode_error(prep_hub):
    '''
    test rend.toml.render when there is a decode error
    '''
    data = """
    # I promise this is toml data
    title = 'toml test'
    [owner
    name = 'toml owner'
    """
    with pytest.raises(rend.exc.RenderException) as exc:
        await prep_hub.rend.toml.render(data)
    assert exc.value.args[0] == "Toml render error: Key group not on a line by itself."
