# Import third party libs
import yaml

__virtualname__ = 'yaml'


def render(hub, data):
    '''
    Given the data, attempt to render it as yaml
    '''
    return yaml.safe_load(data)
