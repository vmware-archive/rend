# -*- coding: utf-8 -*-
'''
Render jinja data
'''
# Import local libs
import rend.exc

# Import third party libs
import jinja2


def render(hub, data):
    '''
    Render the given data through Jinja2
    '''
    if isinstance(data, bytes):
        data = data.decode()
    try:
        template = jinja2.Template(data)
        ret = template.render(hub=hub)
    except jinja2.exceptions.UndefinedError as exc:
        raise rend.exc.RenderException(f'Jinja variable {exc.message}')
    except jinja2.exceptions.TemplateSyntaxError as exc:
        raise rend.exc.RenderException(f'Jinja syntax error {exc.message}')
    return ret
