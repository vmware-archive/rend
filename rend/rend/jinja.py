# Import third party libs
from jinja2 import Template


def render(hub, data):
    '''
    Render the given data through Jinja2
    '''
    template = Template(data)
    return template.render(hub=hub)
