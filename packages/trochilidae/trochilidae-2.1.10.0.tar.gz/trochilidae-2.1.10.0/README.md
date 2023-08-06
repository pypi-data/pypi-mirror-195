Trochilidae (https://en.wikipedia.org/wiki/Hummingbird) is the family name of hummingbirds. The hummingbird unlike any other bird can fly backwards; similarly, this library allows you to fly backwards by providing backwards compatibility and wrappers around components of existing backwards compatibility libraries like future and six. Trochilidae at this point supports cross version reduce, lazily evaluated filter, and with_metaclass (from six and from future). The issue with both versions of with_metaclass is that when they hook into a dependent class' creation, that class' bases will be hosed. This means the following doesn't work: 
```python
class B(with_metaclass(M), A): ...
```
Trochilidae generates a dummy class for those that want to inherit from base classes and a metaclass.