********
Tutorial
********

In this chapter, we are going to develop a ``dirtem`` project by making a Python project directory template.

Step 0 - The Idea
*****************

.. code-block:: text
    
    .
    └── template
        ├── pyproject.toml
        ├── README.md
        └── project_name
            └── py.typed *


Step 1 - Designing the Directory
********************************

.. code-block:: text
    
    .
    ├── dirtem.toml
    └── template
        ├── pyproject.toml
        ├── README.md
        └── {{project_name}}
            └── {%if typed%}py.typed{%endif%}

The file ``py.typed`` will only exist when the variable ``typed`` is set to ``True``. Every file must have
a name. The expression ``{%if typed is true%}py.typed{%endif%}`` will name the file ``py.typed`` when
the variable ``typed`` is true. Otherwise the file will not exist.

Step 2 - File Content
*********************

==============
pyproject.toml
==============

.. note:: For demonstration purposes, this file is simplified.

.. code-block:: toml
    
    [project]
    name = "{{ project_name }}"
    version = "{{ project_version }}"
    description = "{{ project_description }}"
    readme = "README.md"
    license = {text = "{{ project_license }}"}

===========
dirtem.toml
===========

.. code-block:: toml
    
    [default-variables]
    project_version = "0.0.1"
    project_license = "MIT"

Step 3 - Building
*****************

Let us finnaly build our project template! For that we use the command-line interface:

.. code-block:: bash
    
    python3 -m dirtem template build

We will be prompted for variables that are not defined in the ``[default-variables]``
table of the dirtem.toml file.




