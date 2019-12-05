# Import python libs
import sys
import os

# Import pop libs
import pop.hub

# Import third party libs
import pytest

FDIR = os.path.join(sys.path[0], 'files')


def prep_hub():
    hub = pop.hub.Hub()
    hub.pop.sub.add('rend.rend')
    hub.pop.sub.add('rend.output')
    return hub


@pytest.mark.asyncio
async def test_yaml():
    hub = prep_hub()
    fn = os.path.join(FDIR, 'test.yml')
    ret = await hub.rend.init.parse(fn, 'yaml')
    assert ret == {'test': {'foo': 'bar'}}


@pytest.mark.asyncio
async def test_ordered_yaml():
    hub = prep_hub()
    fn = os.path.join(FDIR, 'order.yml')
    ret = await hub.rend.init.parse(fn, 'yaml')
    assert list(ret.keys()) == ['first', 'second', 'third', 'forth', 'fifth']
    assert list(ret['first'].keys()) == [1, 2, 3, 7, 4]


@pytest.mark.asyncio
async def test_toml():
    hub = prep_hub()
    fn = os.path.join(FDIR, 'test.toml')
    ret = await hub.rend.init.parse(fn, 'toml')
    assert ret == {'test': {'foo': 'bar'}}


@pytest.mark.asyncio
async def test_shebang():
    hub = prep_hub()
    fn = os.path.join(FDIR, 'shebang.yml')
    ret = await hub.rend.init.parse(fn, 'toml')  # Pass in bad pipe so we use the one in the file
    assert ret == {'test': {'foo': 'bar'}}
