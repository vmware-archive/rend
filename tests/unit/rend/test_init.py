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
