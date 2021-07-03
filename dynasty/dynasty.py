from .utils import get_pkg_classes, get_anytree, get_ipytree, print_anytree, print_class_hierarchy


class Dynasty:
    def __init__(self, pkg):
        self.pkg = pkg
        self.name = pkg.__name__
        self.class_table = get_pkg_classes(pkg)
        self.anytree = get_anytree(self.class_table)
        self.ipytree = get_ipytree(self.anytree)

    def print(self):
        print_anytree(self.anytree)

    def _print(self):
        print_class_hierarchy(self.class_table)

    def widget(self):
        return self.ipytree
