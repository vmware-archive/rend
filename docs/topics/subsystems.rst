===============
Rend Subsystems
===============

Rend ships with 2 very useful subsystems, `rend` and `output`. They are both
used to managed ingesting and outputting structured data. These tools make
it easy to use structured data files in your projects and to maker clean,
readable output from structured data.

The Rend Subsystem
==================

The `rend` subsystem is very simple, just a single function needs to be
defined, this function is called `render`. The render function takes the
data from the previous stage in the render pipe. This means that `data`
will be a bytestring containing the raw bytes, typically from reading the
file, or the out put from a previous render in the pipe. So if the pipe
you are using is `jinja|yaml` then the bytes collected from reading the file
will be sent first to the `jinja` rend plugin, then the return data from
the render function inside of the `jinja` rend plugin will be passed as `data`
to the `yaml` plugin.

The Output Subsystem
====================

The `output` subsystem is all about making the output from specific
datasets look great! So the single function in the output system is called
`display`. The `display` function returns a string that can be displayed.
Generally speaking this string would then be passed to the python built
in `print()` function.
