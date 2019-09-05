# Import third party libs
import toml


def render(hub, data):
    '''
    Render the given toml data
    '''
    return toml.loads(data)
