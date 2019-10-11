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


def test_rend_parse(prep_hub):
    '''
    test rend.init.parse when RendererException raised
    '''
    fn_ = os.path.join(FDIR, 'test_exc.jinja2')
    with pytest.raises(rend.exc.RenderException) as exc:
        prep_hub.rend.init.parse(fn_, 'jinja')
    assert exc.value.args[0] == "Jinja syntax error Encountered unknown tag 'test_exc'."
