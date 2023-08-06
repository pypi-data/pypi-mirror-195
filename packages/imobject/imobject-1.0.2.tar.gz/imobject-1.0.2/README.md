# imobject

If you want to make data handling easier in Python, you can use imobject. It is a library that has three helpful classes: `ObjDict`, `ImprovedList` and `OrmCollection`.

The `ObjDict` class allows you to create dictionary objects (Dictionary-like object or Dynamic Class as dict), which makes it easier to access and manipulate data elements. This class inherits from the built-in `dict` class and adds features such as converting dictionaries to objects, handling missing keys and access dictionary keys as attributes.

The `ImprovedList` class offers an improved alternative to the Python list class, which it provide additional methods for working with lists of `ObjDict`. This class extends the built-in `list` class and adds features such as inspecting the elements of a list and performing advanced mapping operations.

The `OrmCollection` class providing an interface and additional methods for querying and manipulating objects in the `ImprovedList`. This class is a list-like collection that extends `ImprovedList` and that implements an ORM overlay (wrapper) for a list of `ObjDict`.