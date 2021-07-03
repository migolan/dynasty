# dynasty

Dynasty extracts the class hierachy for your Python package, to track down lost or misplaced classes and help prevent [ravioli code](https://docs.python-guide.org/writing/structure).

See the [example jupyter notebook](https://github.com/migolan/dynasty/blob/main/example.ipynb) for demonstration.

**Installation**
```buildoutcfg
pip install dynasty
```

**Usage**
```python
import mypackage
from dynasty import Dynasty

mypackage_dynasty = Dynasty(mypackage)

# display collapsible class hierarchy (in jupyter notebook)
mypackage_dynasty.widget()

# print class hierarchy to screen
mypackage_dynasty.print()
```

**Author**

Michal Golan, [migolan@gmail.com](migolan@gmail.com), [migolan@github](https://github.com/migolan)