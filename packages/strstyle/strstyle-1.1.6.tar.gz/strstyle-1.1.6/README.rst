style
=====

Install
-------

::

    $ pip install strstyle


Usage
-----

.. code:: py

    import strstyle

    print(strstyle.red('Hello', strstyle.bold('world') + '!'))


API
---

strstyle.\ ``strstyle*[.strstyle](*objects, sep=' ')``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Chain `strstyle <#strstyles>`__ and call the last one as a method with an argument. Order doesn't matter, and later strstyles
take precedence in case of a conflict, e.g. ``strstyle.red.yellow.green`` is equivalent to ``strstyle.green``. strstyles can
be nested.

Multiple arguments will be separated by ``sep``, a space by default.

strstyle.\ ``enabled``
~~~~~~~~~~~~~~~~~~~

Color support is automatically detected, but can also be changed manually.

- set ``strstyle.enabled`` to ``True`` or ``False``
- use the command line parameter ``--color`` or ``--no-color``


strstyles
------

+---------------------+-------------------------------------+-------------------------------------------+
| Modifiers           | Colors                              | Background colors                         |
+=====================+===============+=====================+==================+========================+
| - ``bold``          | - ``black``   | - ``light_black``   | - ``on_black``   | - ``on_light_black``   |
| - ``dim``           | - ``red``     | - ``light_red``     | - ``on_red``     | - ``on_light_red``     |
| - ``italic``        | - ``green``   | - ``light_green``   | - ``on_green``   | - ``on_light_green``   |
| - ``underline``     | - ``yellow``  | - ``light_yellow``  | - ``on_yellow``  | - ``on_light_yellow``  |
| - ``inverse``       | - ``blue``    | - ``light_blue``    | - ``on_blue``    | - ``on_light_blue``    |
| - ``hidden``        | - ``magenta`` | - ``light_magenta`` | - ``on_magenta`` | - ``on_light_magenta`` |
| - ``strikethrough`` | - ``cyan``    | - ``light_cyan``    | - ``on_cyan``    | - ``on_light_cyan``    |
|                     | - ``white``   | - ``light_white``   | - ``on_white``   | - ``on_light_white``   |
+---------------------+---------------+---------------------+------------------+------------------------+



