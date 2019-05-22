.. _props:

Attribute access dictionary
===========================

The attribute access dictionary allows users to access items of a dictionary using attribute access. So instead of
doing::

    d["foo"][0]["bar"]

You can do::

    d.foo[0].bar

To create such a dictionary, use the :func:`nhlapi.props.wrap` function. However, you should rarely have to create the
dictionary yourself because the :ref:`endpoints <endpoints>` create them for you.

Since the underlying dictionary can contain any key, the attribute access dictionary does not have any method. They
could easily conflict with the data inside. In order to operate on the attribute access dictionary, use the functions
inside the :mod:`nhlapi.props` module, such as :func:`nhlapi.props.keys`, :func:`nhlapi.props.get`, etc.

------

.. autofunction:: nhlapi.props.wrap
.. autofunction:: nhlapi.props.get
.. autofunction:: nhlapi.props.keys
.. autofunction:: nhlapi.props.values
.. autofunction:: nhlapi.props.items
.. autofunction:: nhlapi.props.json_dump

------

.. autoclass:: nhlapi.props.PropDict
    :members:
    :undoc-members:
    :special-members:
    :exclude-members: __slots__, __dict__, __module__, __abstractmethods__, __weakref__

.. autoclass:: nhlapi.props.PropList
    :members:
    :undoc-members:
    :special-members:
    :exclude-members: __slots__, __dict__, __module__, __abstractmethods__, __weakref__
