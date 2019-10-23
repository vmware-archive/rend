CLI_CONFIG = {
        'file': {
            'options': ['--file', '-f'],
            'default': None,
            'help': 'Pass in a file location that will be rendered',
            },
        'pipe': {
            'options': ['--pipe', '-p'],
            'default': 'yaml',
            'help': 'Define what render pipeline should be used',
            },
        'output': {
            'options': ['--output', '-o'],
            'default': 'nested',
            'help': 'Define which outputter system should be used to display the result of this render',
            },
        }
CONFIG = {}
GLOBAL = {}
SUBS = {}
DYNE = {
        'rend': ['rend'],
        'output': ['output'],
        }
