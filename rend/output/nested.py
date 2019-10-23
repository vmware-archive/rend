# -*- coding: utf-8 -*-
'''
Recursively display nested data
===============================

Example output::

    some key:
        ----------
        foo:
            ----------
            bar:
                baz
            dictionary:
                ----------
                abc:
                    123
                def:
                    456
            list:
                - Hello
                - World
'''
# Import python libs
from numbers import Number
from collections.abc import Mapping

# Import third party libs
from colored import fg, attr


class NestDisplay(object):
    '''
    Manage the nested display contents
    '''
    def ustring(self,
                indent,
                color,
                msg,
                prefix='',
                suffix='',
                endc=attr(0)):

        indent *= ' '
        fmt = '{0}{1}{2}{3}{4}{5}'

        try:
            return fmt.format(
                indent,
                color,
                prefix,
                msg,
                endc,
                suffix)
        except UnicodeDecodeError:
            try:
                return fmt.format(
                    indent,
                    color,
                    prefix,
                    salt.utils.stringutils.to_unicode(msg),
                    endc,
                    suffix)
            except UnicodeDecodeError:
                # msg contains binary data that can't be decoded
                return str(fmt).format(
                    indent,
                    color,
                    prefix,
                    msg,
                    endc,
                    suffix)

    def display(self, ret, indent, prefix, out):
        '''
        Recursively iterate down through data structures to determine output
        '''
        if isinstance(ret, bytes):
            try:
                ret = ret.decode()
            except UnicodeDecodeError:
                # ret contains binary data that can't be decoded
                pass

        if ret is None or ret is True or ret is False:
            out.append(
                self.ustring(
                    indent,
                    fg(11),
                    ret,
                    prefix=prefix
                )
            )
        # Number includes all python numbers types
        #  (float, int, long, complex, ...)
        # use repr() to get the full precision also for older python versions
        # as until about python32 it was limited to 12 digits only by default
        elif isinstance(ret, Number):
            out.append(
                self.ustring(
                    indent,
                    fg(11),
                    repr(ret),
                    prefix=prefix
                )
            )
        elif isinstance(ret, str):
            first_line = True
            for line in ret.splitlines():
                line_prefix = ' ' * len(prefix) if not first_line else prefix
                if isinstance(line, bytes):
                    out.append(
                        self.ustring(
                            indent,
                            fg(3),
                            'Not string data',
                            prefix=line_prefix
                        )
                    )
                    break
                out.append(
                    self.ustring(
                        indent,
                        fg(2),
                        line,
                        prefix=line_prefix
                    )
                )
                first_line = False
        elif isinstance(ret, (list, tuple)):
            color = fg(2)
            for ind in ret:
                if isinstance(ind, (list, tuple, Mapping)):
                    out.append(
                        self.ustring(
                            indent,
                            color,
                            '|_'
                        )
                    )
                    prefix = '' if isinstance(ind, Mapping) else '- '
                    self.display(ind, indent + 2, prefix, out)
                else:
                    self.display(ind, indent, '- ', out)
        elif isinstance(ret, Mapping):
            if indent:
                color = fg(6)
                out.append(
                    self.ustring(
                        indent,
                        color,
                        '----------'
                    )
                )

            keys = ret.keys()
            color = fg(6)
            for key in keys:
                val = ret[key]
                out.append(
                    self.ustring(
                        indent,
                        color,
                        key,
                        suffix=':',
                        prefix=prefix
                    )
                )
                self.display(val, indent + 4, '', out)
        return out


def display(hub, ret):
    '''
    Display ret data
    '''
    nest = NestDisplay()
    lines = nest.display(ret, 0, '', [])
    try:
        return '\n'.join(lines)
    except UnicodeDecodeError:
        # output contains binary data that can't be decoded
        return str('\n').join(  # future lint: disable=blacklisted-function
            [str(x) for x in lines]
        )
