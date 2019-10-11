# Import third party libs
import yaml

# Import local libs
import rend.exc

__virtualname__ = 'yaml'


def render(hub, data):
    '''
    Given the data, attempt to render it as yaml
    '''
    try:
        ret = yaml.safe_load(data)
    except (yaml.parser.ParserError,
            yaml.constructor.ConstructorError,
            yaml.scanner.ScannerError) as exc:
        raise rend.exc.RenderException(f'Yaml render error: {exc.problem}')
    return ret
