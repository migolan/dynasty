import os
import pyclbr
import pandas as pd
import numpy as np


def module_classes(module_name):
    """Returns all classes in module."""
    module_members = pyclbr.readmodule_ex(module_name, [])
    module_members = dict(sorted(module_members.items(), key=lambda a: getattr(a, 'lineno', 0)))
    module_members = module_members.values()

    classes = [x for x in module_members if isinstance(x, pyclbr.Class)]
    classnames = [x.name for x in classes]
    baseclasses = [x.super for x in classes]
    baseclasses = [x[0] if len(x) > 0 else "-" for x in baseclasses]
    baseclasses = [x.name if isinstance(x, pyclbr.Class) else x for x in baseclasses]
    class_table = pd.DataFrame(list(zip(classnames, baseclasses)), columns=['classname', 'baseclass'])
    class_table['module'] = module_name
    return class_table


def pkg_modules(pkg_path):
    """Returns all modules in package recursively."""
    modules = []
    pkg_root = os.path.split(pkg_path)[0]
    for path, subdirs, files in os.walk(pkg_path):
        pyfiles = filter(lambda x: x.endswith(".py"), files)
        pyfilepaths = [os.path.join(path, x) for x in pyfiles]
        newmodules = [x.replace(".py", "")
                       .replace(pkg_root+os.path.sep, "")
                       .replace(os.path.sep, ".")
                      for x in pyfilepaths]
        modules.extend(newmodules)
    return modules


def pkg_classes(pkg_path):
    """Returns all classes in package recursively."""
    class_table = pd.DataFrame()
    for module_name in pkg_modules(pkg_path):
        class_table = pd.concat([class_table, module_classes(module_name)])
    class_table.reset_index(drop=True, inplace=True)
    return class_table


def analyze_children(class_table):
    """Finds child classes across package recursively."""
    class_table['children'] = np.empty((len(class_table), 0)).tolist()
    for i, row in class_table.iterrows():
        baseclassrows = class_table[class_table['classname'] == row['baseclass']]
        if len(baseclassrows) > 0:
            baseclassrows['children'].values[0].append(row['classname'])


def print_class_hierarchy(class_table, baseclass="-", prefix="|_"):
    """Prints class hierarchy in tree structure."""
    base_parented_classes = class_table[class_table['baseclass'] == baseclass].reset_index()
    for i, classdata in base_parented_classes.iterrows():
        print(prefix + classdata['module'] + "." + classdata['classname'])
        next_prefix = prefix.replace("_", " ")
        if i == len(base_parented_classes)-1:
            k = next_prefix.rfind("|")
            next_prefix = next_prefix[:k] + " " + next_prefix[k+1:]
        next_prefix = next_prefix + "|_"
        print_class_hierarchy(class_table, classdata['classname'], next_prefix)
