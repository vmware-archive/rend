===============
The Rend System
===============

The `rend` system is a system used to allow the concept of renderers to be
easily applied to `pop` projects. This  system makes it easy to app-merge
`rend` into your `pop` project and gain access to the template rendering
system and to the `output` system.

Using Rend
==========

Rend is used to render data files that are potentially wrapped in a templating
language. For instance you can have a toml file that is wrapped in jinja2 or
mako. This makes the generation of the dataset defined in the data file
dynamic. When using `rend` the `hub` from your `pop` project will also be
made available to the templating system. This allows for your `pop` project
to always be available to your rendering process.

To use `rend` simply add the `rend` `sub` to your `hub`:

.. code-block:: python

    hub.pop.sub.add(dyne_name='rend')

That's it! Now you have the rend system on your hub for all plugins that
are in your `pop` project! Using the `rend` system is easy, just call
`hub.rend.init.parse` with your preferred render pipe and the file you wish to
render.

.. code-block:: python

    data = hub.rend.init.parse('file.yml', 'yaml')

This simple example if  no different really than just using yaml directly, but
to get the full power of `rend` you can use render pipes.

Render Pipes
============

Render pipes allow you to define how to process the given file. A render pipe
allows for an arbitrary list of renderers to be passed over on the file. For
instance, if you want a jinja rendered toml file.

.. code-block:: python

    data = hub.rend.init.parse('file.jinja.toml'. 'jinja|toml')

With the pipe defined as `jinja|toml` then the rend system will first render it
using jinja and then render that result using toml. The jinja render will also
have access to the `hub` and all of its functions!

Render Pipes in Files
---------------------

A render pipe can be set up to exist in a given file as well. This makes it easy
to define what type of file you are working with based on the contents of the
file itself.

A render pipe is defined using a shebang line at the top of the file:

.. code-block:: yaml

    #!jinja|yaml
    {% for key, val in hub.mysub.stuff.iter() %}
    {{key}}:
      {{val}}
    {% endfor %}

Now this jinja template will execute, call the function on the hub and use it to
generate a dataset.

Output System
=============

The output system is a convenience system used to create pretty cli output from
applications. To use it just add it to your `hub`

.. code-block:: python

    hub.pop.sub.add(dyne_name='output')
    print(hub.output.pretty.display({'foo': 'bar'}))
