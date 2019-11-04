==============================
Vertical App Merging With Rend
==============================

Since `rend` is a `pop` project, if can be vertically app merged! This is
generally the right way to extend `rend` because you can make rend interfaces
that have application specific code in them while still being directly
integrated into `rend` itself.

To use vertical app merging just add the *DYNE* option to your conf.py file
specifying that your project provides `rend` or `output` modules:

.. code-block:: python

    DYNE = {
        'rend': ['rend'],
        'output': ['output'],
        }

Then when the rend system starts up it will add your modules to its own
namepsace on the hub! It is as easy as that!
