# Import third party libs
import toml

__virtualname__ = 'toml'


def render(hub, data):
    '''
    Render the given toml data
    '''
    data = data.decode()
    return toml.loads(data)
