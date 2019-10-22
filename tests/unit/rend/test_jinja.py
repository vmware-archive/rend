# -*- coding: utf-8 -*-
'''
    tests.unit.rend.test_jinja
    ~~~~~~~~~~~~~~

    Unit tests for the jinja renderer
'''

# Import python libs
import pytest

# Import local libs
import rend.exc


def test_jinja(prep_hub):
    '''
    test rend.jinja.render renders correctly
    '''
    ret = prep_hub.rend.jinja.render('{% set test = "itworked" %}{{ test }}')
    assert ret == 'itworked'

def test_jinja_bytes(prep_hub):
    '''
    test rend.jinja.render renders correctly with bytes data
    '''
    ret = prep_hub.rend.jinja.render(b'{% set test = "itworked" %}{{ test }}')
    assert ret == 'itworked'

def test_jinja_undefined(prep_hub):
    '''
    test rend.jinja.render when there is an undefined error
    '''
    with pytest.raises(rend.exc.RenderException) as exc:
        prep_hub.rend.jinja.render('{{ hello.test }}')
    assert exc.value.args[0] == "Jinja variable 'hello' is undefined"

def test_jinja_syntax(prep_hub):
    '''
    test rend.jinja.render when there is a syntax error
    '''
    with pytest.raises(rend.exc.RenderException) as exc:
        prep_hub.rend.jinja.render('{% test % }')
    assert exc.value.args[0] == "Jinja syntax error Encountered unknown tag 'test'."
