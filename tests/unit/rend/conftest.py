# import python libs
import pytest

# Import pop libs
import pop.hub

@pytest.fixture
def prep_hub():
    '''
    Add required subs to the hub.
    '''
    hub = pop.hub.Hub()
    hub.pop.sub.add('rend.rend')
    hub.pop.sub.add('rend.output')
    return hub
