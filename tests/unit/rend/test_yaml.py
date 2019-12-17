# -*- coding: utf-8 -*-
'''
    tests.unit.rend.test_yaml
    ~~~~~~~~~~~~~~

    Unit tests for the yaml renderer
'''

# Import python libs
import pytest

# Import local libs
import rend.exc


@pytest.mark.asyncio
@pytest.mark.parametrize('data',
                         [b'test: one',
                          'test: one'])
async def test_yaml(prep_hub, data):
    '''
    test rend.yaml.render renders correctly
    '''
    ret = await prep_hub.rend.yaml.render(data)
    assert isinstance(ret, dict)
    assert ret['test'] == 'one'


@pytest.mark.asyncio
async def test_yaml_scanner_exc(prep_hub):
    '''
    test rend.yaml.render when there is a scanner error
    '''
    with pytest.raises(rend.exc.RenderException) as exc:
        await prep_hub.rend.yaml.render('test:\none')
    assert exc.value.args[0] == "Yaml render error: could not find expected ':'"


@pytest.mark.asyncio
async def test_yaml_parser_exc(prep_hub):
    '''
    test rend.yaml.render when there is a parser error
    '''
    with pytest.raises(rend.exc.RenderException) as exc:
        await prep_hub.rend.yaml.render('- !-!str just a string')
    assert exc.value.args[0] == "Yaml render error: found undefined tag handle"


@pytest.mark.asyncio
async def test_yaml_constructor_exc(prep_hub):
    '''
    test rend.yaml.render when there is a contructor error
    '''
    with pytest.raises(rend.exc.RenderException) as exc:
        await prep_hub.rend.yaml.render('- !!!str just a string:one')
    assert exc.value.args[0] == "Yaml render error: could not determine "\
                                "a constructor for the tag 'tag:yaml.org,2002:!str'"

@pytest.mark.asyncio
async def test_duplicate_keys(prep_hub):
    data = '''foo: bar
foo: bar
    '''
    with pytest.raises(rend.exc.RenderException) as exc:
        ret = await prep_hub.rend.yaml.render(data)
    assert exc.value.args[0] == "Yaml render error: found conflicting ID 'foo'"

