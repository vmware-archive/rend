# Import python libs
import sys
import os

# Import pop libs
import pop.hub

FDIR = os.path.join(sys.path[0], 'files')


def prep_hub():
    hub = pop.hub.Hub()
    hub.pop.sub.add('rend.rend')
    hub.pop.sub.add('rend.output')
    return hub


def test_yaml():
    hub = prep_hub()
    fn = os.path.join(FDIR, 'test.yml')
    ret = hub.rend.init.parse(fn, 'yaml')
    assert ret == {'test': {'foo': 'bar'}}


def test_ordered_yaml():
    hub = prep_hub()
    fn = os.path.join(FDIR, 'order.yml')
    ret = hub.rend.init.parse(fn, 'yaml')
    assert list(ret.keys()) == ['first', 'second', 'third', 'forth', 'fifth']
    assert list(ret['first'].keys()) == [1, 2, 3, 7, 4]


def test_toml():
    hub = prep_hub()
    fn = os.path.join(FDIR, 'test.toml')
    ret = hub.rend.init.parse(fn, 'toml')
    assert ret == {'test': {'foo': 'bar'}}


def test_shebang():
    hub = prep_hub()
    fn = os.path.join(FDIR, 'shebang.yml')
    ret = hub.rend.init.parse(fn, 'toml')  # Pass in bad pipe so we use the one in the file
    assert ret == {'test': {'foo': 'bar'}}
