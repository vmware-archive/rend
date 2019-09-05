# Import python libs
import pprint
# Import local libs
import rend.exc


def standalone(hub):
    '''
    Execute the render system onto a single file, typically to test basic
    functionality
    '''
    hub.pop.conf.integrate('rend', cli='rend')
    hub.pop.sub.add(dyne_name='output')
    outputter = hub.OPT['rend']['output']
    ret = hub.rend.init.parse(hub.OPT['rend']['file'], hub.OPT['rend']['pipe'])
    print(getattr(hub, f'output.{outputter}.display')(ret))


def parse(hub, fn, pipe=None):
    '''
    Pass in the render pipe to use to render the given file. If no pipe is
    passed in then the file will be checked for a render shebang line. If
    no render shebang line is present then the system will raise an
    Exception
    '''
    with open(fn, 'rb') as rfh:
        data = rfh.read()
    if pipe is None:
        if data.startswith(b'#!'):
            dpipe = data[2:data.index(b'\n')].split(b'|')
        else:
            raise rend.exc.RendPipeException(f'File {fn} passed in without a render pipe defined')
    else:
        dpipe = pipe.split('|')
    for render in dpipe:
        if isinstance(render, bytes):
            render = render.decode()
        data = getattr(hub, f'rend.{render}.render')(data)
    return data
