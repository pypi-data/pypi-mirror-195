*************
Configuration
*************

While the API supports using a ``dict``, it is still recommended to use a configuration file. The CLI requires a
configuration file. The `TOML file format <https://toml.io>`_ is used to configure several things. The snippet
below can be used as a template for a quick start.

.. code-block:: toml
    
    [jinja]
    select = ["foo.txt", "*.zip"]
    select-mode = ["exclude"]
        
    [debug]
    generate-metadata-file = true
    
    [debug.metadata-add]
    foo = "foo"
    bar = "bar"
    
    [cli]
    log-level = 2
    
    [default-variables]
    baz = "baz"
    foobar = "foobar"

Sections
********

* :ref:`[jinja]<config.jinja>`
  
  * :ref:`select<config.jinja.select>`
  * :ref:`select-mode<config.jinja.select-mode>`
  * :ref:`prompt-missing<config.jinja.prompt-missing>`
  * :ref:`[config.jinja.configure]<config.jinja.configure>`

* :ref:`[fs]<config.fs>`
  
  * :ref:`select<config.fs.select>`
  * :ref:`select-mode<config.fs.select-mode>`

* :ref:`[debug]<config.debug>`
  
  * :ref:`generate-metadata-file<config.debug.generate-metadata-file>`
  * :ref:`[debug.metadata-add]<config.debug.metadata-add>`

* :ref:`[cli]<config.cli>`

* :ref:`[default-variables]<config.default-variables>`


.. _config.jinja:

=====================
The ``jinja`` section
=====================

.. code-block:: toml
    
    [jinja]

This section controlls the jinja template engine and which files use it.

.. _config.jinja.select:

The ``select`` option
=====================

``array<string>``

.. code-block:: toml
    
    select = []

By default all non-binary files are assumed to use the jinja template unless the first line is ``{# nojinja #}``.
Note that a file starting with ``{# nojinja #}`` or ``{# isjinja #}`` always overrides this option for that file.
When this is set, ``select-mode`` should also be defined.

All files matching one of the `glob patterns <https://en.wikipedia.org/wiki/Glob_(programming)>`_ will be rendered
using the jinja template engine.

.. _config.jinja.select-mode:

The ``select-mode`` option
==========================

``"include"|"exclude" ("include")``

.. code-block:: toml
    
    select-mode = "include"

When this is ``include`` all files matching one of the patterns in ``select`` are marked as using the jinja#
template. The opposite is the case when this option is set to ``exclude``.

.. _config.jinja.prompt-missing:

The ``prompt-missing`` option
=============================

``boolean (true)``

.. code-block:: toml
    
    prompt-missing = true

Prompts the user for a string when some variable is nowhere provided.

.. _config.jinja.configure:

The ``jinja.configure`` section
===============================

.. code-block:: toml
    
    [jinja.configure]

This section allows you to configures jinja itself. There are currently no options but this might change in
the future.


.. _config.fs:

==================
The ``fs`` section
==================

.. code-block:: toml
    
    [fs]

.. _config.fs.select:

The ``select`` option
=====================

``array<string>``

.. code-block:: toml
    
    select = []

There is usually no reason to exclude files in a template directory: just remove the files from that directory. An
exception might be for a ``README`` file.

.. _config.fs.select-mode:

The ``select-mode`` option
==========================

``"include"|"exclude" ("include")``

.. code-block:: toml
    
    select-mode = "include"

.. _config.fs.file-pattern-engine:

The ``file-pattern-style`` option
==================================

``"glob"|"regex" ("glob")``

.. code-block:: toml
    
    file-pattern-style = "glob"

The pattern style to use for filtering files in the ``select`` options.

.. _config.debug:

=====================
The ``debug`` section
=====================

.. code-block:: toml
    
    [debug]

.. _config.debug.generate-metadata-file:

The ``generate-metadata-file`` option
=====================================

``boolean (false)``

.. code-block:: toml
    
    generate-metadata-file = false

Whether the ``.dirtem`` metadata file in the build directory should be generated. This file contains data about
when the build was made, which version of ``dirtem`` was used and more information.

.. _config.debug.metadata-add:

The ``debug.metadata-add`` section
==================================

.. code-block:: toml
    
    [debug.metadata-add]

Arbitrary key/value pairs that will be added to the ``.dirtem`` metadata file.

.. _config.cli:

===================
The ``cli`` section
===================

.. code-block:: toml
    
    [cli]

.. _config.default-variables:

=================================
The ``default-variables`` section
=================================

.. code-block:: toml
    
    [default-variables]

Key/Value pairs of variables that will be used when one is not provided when building.
