.. image:: https://img.shields.io/pypi/v/mccolor.svg
    :target: https://pypi.org/project/colorama/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/colorama.svg
    :target: https://pypi.org/project/colorama/
    :alt: Supported Python versions

MCColor
========

Use Minecraft color codes in your Python terminal!

.. |donate| image:: https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif
  :target: https://www.paypal.com/donate/?hosted_button_id=FSDW2D6ECKHPA
  :alt: Donate with Paypal

`Releases <https://pypi.org/project/mccolor/>`_ |
`Github <https://github.com/tartley/mccolor>`_ |

If you want to support me: |donate|. Thank you!

Installation
------------

Tested on Python 3.7, 3.8, 3.9, 3.10 and 3.11.

No requirements other than the standard library.

.. code-block:: bash

    pip install mccolor

Description
-----------

This library could make your Minecraft projects in Python easier! 
You can use/replace/remove Minecraft color codes in a text.

.. image:: https://i.imgur.com/2NSQurq.png
    :width: 661
    :height: 357
    :alt: Colors

Usage
-----

Write

Write a text using the color codes.

.. code-block:: python

    from mccolor import mcwrite

    mcwrite('§aThis text is green!')

Replace

Replace the color codes of a text.

.. code-block:: python

    from mccolor import mcreplace

    text = '§aThis text is green!'
    colored = mcreplace(text)
    print(colored)

Remove

Remove colored characters from text.

.. code-block:: python

    from mccolor import mcremove

    text = '§aThis text is green!'
    clean = mcremove(text)
    print(clean)