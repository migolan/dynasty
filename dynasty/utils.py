import os
import pyclbr
import pandas as pd
import numpy as np
import anytree
import ipytree


def get_module_classes(module_name):
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


def get_pkg_modules(pkg_path):
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


def get_pkg_classes(pkg):
    """Returns all classes in package recursively."""
    class_table = pd.DataFrame()
    pkg_path = pkg.__path__[0]
    for module_name in get_pkg_modules(pkg_path):
        class_table = pd.concat([class_table, get_module_classes(module_name)])
    class_table.reset_index(drop=True, inplace=True)
    class_table.name = pkg.__name__
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
    if baseclass == "-":
        print(class_table.name)
    base_parented_classes = class_table[class_table['baseclass'] == baseclass].reset_index()
    for i, classdata in base_parented_classes.iterrows():
        print(prefix + classdata['module'] + "." + classdata['classname'])
        next_prefix = prefix.replace("_", " ")
        if i == len(base_parented_classes)-1:
            k = next_prefix.rfind("|")
            next_prefix = next_prefix[:k] + " " + next_prefix[k+1:]
        next_prefix = next_prefix + "|_"
        print_class_hierarchy(class_table, classdata['classname'], next_prefix)


def get_anytree(class_table, baseclass="-"):
    if baseclass == "-":
        anytree_node = anytree.Node(class_table.name)
        anytree_node.classpath = class_table.name
    else:
        anytree_node = anytree.Node(baseclass)
    base_parented_classes = class_table[class_table['baseclass'] == baseclass].reset_index()
    for i, classdata in base_parented_classes.iterrows():
        child_anytree_node = get_anytree(class_table, classdata['classname'])
        child_anytree_node.parent = anytree_node
        child_anytree_node.classpath = classdata['module'] + "." + classdata['classname']
    return anytree_node


def print_anytree(anytree_topnode, classpath=False):
    for pre, fill, node in anytree.RenderTree(anytree_topnode):
        print("%s%s" % (pre, node.classpath if classpath else node.name))


def get_ipytree(anytree_topnode, classpath=False):
    tree = ipytree.Tree()
    ipytree_topnode = get_ipytree_node(anytree_topnode, classpath)
    ipytree_topnode.icon = "archive"
    for node in ipytree_topnode.nodes:
        node.icon = "angle-right"
    tree.add_node(ipytree_topnode)
    return tree


def get_ipytree_node(anytree_node, classpath=False):
    if hasattr(anytree_node, "_NodeMixin__children"):
        child_ipytree_nodes = [get_ipytree_node(x, classpath=classpath) for x in anytree_node._NodeMixin__children]
    else:
        child_ipytree_nodes = []
    return ipytree.Node(anytree_node.classpath if classpath else anytree_node.name, child_ipytree_nodes, icon="angle-up")
