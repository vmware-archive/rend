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


@pytest.mark.parametrize('data',
                         [b'test: one',
                          'test: one'])
def test_yaml(prep_hub, data):
    '''
    test rend.yaml.render renders correctly
    '''
    ret = prep_hub.rend.yaml.render(data)
    assert isinstance(ret, dict)
    assert ret['test'] == 'one'

def test_yaml_scanner_exc(prep_hub):
    '''
    test rend.yaml.render when there is a scanner error
    '''
    with pytest.raises(rend.exc.RenderException) as exc:
        prep_hub.rend.yaml.render('test:\none')
    assert exc.value.args[0] == "Yaml render error: could not find expected ':'"

def test_yaml_parser_exc(prep_hub):
    '''
    test rend.yaml.render when there is a parser error
    '''
    with pytest.raises(rend.exc.RenderException) as exc:
        prep_hub.rend.yaml.render('- !-!str just a string')
    assert exc.value.args[0] == "Yaml render error: found undefined tag handle '!-!'"

def test_yaml_constructor_exc(prep_hub):
    '''
    test rend.yaml.render when there is a contructor error
    '''
    with pytest.raises(rend.exc.RenderException) as exc:
        prep_hub.rend.yaml.render('- !!!str just a string:one')
    assert exc.value.args[0] == "Yaml render error: could not determine "\
                                "a constructor for the tag 'tag:yaml.org,2002:!str'"
