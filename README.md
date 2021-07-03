# dynasty

Dynasty extracts the class hierachy for your Python package, to track down lost or misplaced classes and help prevent [ravioli code](https://docs.python-guide.org/writing/structure).

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
<img src="https://github.com/migolan/dynasty/blob/main/widget_demo.gif" width="400">
<img src="https://github.com/migolan/dynasty/blob/main/print_demo.png" width="400">

**Author**

Michal Golan <[migolan@gmail.com](mailto:migolan@gmail.com)> [migolan@github](https://github.com/migolan)
