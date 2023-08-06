import itertools
from inspect import isclass
from types import FunctionType

import docutils.parsers.rst.directives
from bsb.config import get_config_attributes
from bsb.config._make import MISSING
from bsb.config._attrs import (
    ConfigurationListAttribute,
    ConfigurationDictAttribute,
)
from bsb.config.parsers import get_parser_classes
from bsb.config.types import class_
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList
from sphinx.util.docutils import SphinxDirective

__version__ = "0.1.0"


def example_function():
    pass


example_function.__module__ = "my_module"
example_function.__name__ = "my_function"

_example_values = {
    bool: True,
    list: [],
    str: "example",
    int: 42,
    float: 3.14,
    FunctionType: example_function,
    dict: {},
}


class ComponentIntro(Directive):
    has_content = False

    def run(self):
        # Use the state machine to generate a block quote for us and parse our text :)
        return self.state.block_quote(
            StringList(
                [
                    ":octicon:`light-bulb;1em;sd-text-info` New to components?"
                    + " Write your first one with :doc:`our guide </guides/components>`"
                ]
            ),
            self.content_offset,
        )


class AutoconfigNode(nodes.General, nodes.Element):
    pass


def visit_autoconfig_node(self, node):
    pass


def depart_autoconfig_node(self, node):
    pass


class AutoconfigDirective(SphinxDirective):
    required_arguments = 1
    has_content = False
    option_spec = {"no-imports": docutils.parsers.rst.directives.flag}

    def run(self):
        clsref = self.arguments[0]
        cls = class_()(clsref)
        tree = self.guess_example(cls)
        elem = AutoconfigNode()
        self.state.nested_parse(
            StringList(
                [
                    ".. tab-set-code::",
                    "",
                    "    .. code-block:: Python",
                    "",
                    *(
                        ()
                        if "no-imports" in self.options
                        else (f"        {imp}" for imp in self.get_import_lines(cls))
                    ),
                    "",
                    *(f"        {line}" for line in self.get_python_lines(cls, tree)),
                    "",
                    *itertools.chain.from_iterable(
                        self.get_parser_lines(key, parser(), tree)
                        for key, parser in get_parser_classes().items()
                    ),
                ]
            ),
            self.content_offset,
            elem,
        )
        return [elem]

    def guess_example(self, cls):
        attrs = get_config_attributes(cls)
        tree = {attr.attr_name: self.guess_default(attr) for attr in attrs.values()}
        return tree

    def guess_default(self, attr):
        """
        Guess a default value/structure for the given attribute. Defaults are paired in
        tuples with functions that can unpack the tree value to their Python
        representation. The most basic "argument unpacker" exemplifies this, and turns
        the value ``x`` into ``f"{key}={repr(x)}"``.

        :param attr:
        :return:
        """
        type_ = self.get_attr_type(attr)

        # If the attribute is a node type, we have to guess recursively.
        if attr.is_node_type():
            # Node types that come from private modules shouldn't be promoted,
            # so instead we make use of the dictionary notation.
            if any(m.startswith("_") for m in type_.__module__.split(".")):
                untree = self.private_untree(type_)
            else:
                untree = self.public_untree(type_)
            # Configuration lists and dicts should be packed into a list/dict
            if isinstance(attr, ConfigurationListAttribute):
                untree = self.list_untree(untree)
            elif isinstance(attr, ConfigurationDictAttribute):
                untree = self.dict_untree(untree)
            return (untree, self.guess_example(type_))
        else:
            return (self.argument_untree, self.guess_example_value(attr))

    def guess_example_value(self, attr):
        type_ = self.get_attr_type(attr)
        # The attribute may have a hinted example from the declaration `hint` kwarg,
        # or from the `__hint__` method of its type handler
        hint = attr.get_hint()
        if hint is not MISSING:
            example = hint
        else:
            # No hint, so check if the default is sensible
            default = attr.get_default()
            example = None
            if default is not None:
                example = default
            elif isclass(type_):
                # No default value, and likely a primitive was passed as type handler
                for parent_type, value in _example_values.items():
                    # Loop over some basic possible basic primitives
                    if issubclass(type_, parent_type):
                        example = value
                        break
            if example is None:
                # Try to have the type handler cast some primitive examples,
                # if no error is raised we assume it's a good example
                example = self.try_types(type_, *_example_values.values())
                # `str` is a kind of greedy type handler, so correct the casts
                if example == "[]":
                    example = []
                elif example == "{}":
                    example = {}
                elif example == "true":
                    example = True
        # Some values need to be cast back to a tree-form, so we create a shim
        # for the attribute descriptor to use as an instance.
        shim = type("AttrShim", (), {})()
        setattr(shim, f"_{attr.attr_name}", example)
        try:
            example = attr.tree(shim)
        except Exception:
            pass
        # Hope we have a default value.
        return example

    def get_attr_type(self, attr):
        type_ = attr.get_type()
        type_ = str if type_ is None else type_
        return type_

    def try_types(self, type_, arg, *args):
        try:
            return type_(arg)
        except Exception:
            if args:
                return self.try_types(type_, *args)

    def get_python_lines(self, cls, tree):
        return [
            f"{cls.__name__}(",
            *(
                f"  {line}"
                for line in itertools.chain.from_iterable(
                    self.get_argument_lines(key, *value) for key, value in tree.items()
                )
            ),
            ")",
        ]

    def get_argument_lines(self, key, untree, value):
        return untree(key, value)

    def get_parser_lines(self, name, parser, tree):
        raw = self.raw_untree((None, tree))
        language = getattr(parser, "data_syntax", False) or name
        return [
            f"    .. code-block:: {language}",
            "",
            *(
                f"        {line}"
                for line in parser.generate(raw, pretty=True).split("\n")
            ),
            "",
        ]

    def raw_untree(self, tree):
        try:
            node_data = tree[1]
        except TypeError:
            # If the element wasn't packed as a tuple it's just a list/dict attr
            return tree
        if getattr(tree[0], "dict_repack", False):
            node_data = {"key_of_thing": (None, node_data)}
        if getattr(tree[0], "list_repack", False):
            node_data = [(None, node_data)]
        if isinstance(node_data, dict):
            return {k: self.raw_untree(v) for k, v in node_data.items()}
        elif isinstance(node_data, list):
            return [self.raw_untree(v) for v in node_data]
        else:
            return node_data

    def public_untree(self, cls):
        def untree(key, value):
            lines = self.get_python_lines(cls, value)
            lines[0] = f"{key}={lines[0]}"
            lines[-1] += ","
            return lines

        return untree

    def private_untree(self, cls):
        def untree(key, value):
            lines = self.get_python_lines(cls, value)
            lines[0] = key + "={"
            for i in range(1, len(lines) - 1):
                line = lines[i]
                if "=" in line:
                    lp = line.split("=")
                    indent = len(lp[0]) - len(lp[0].lstrip())
                    lines[i] = f"{' ' * indent}'{lp[0].lstrip()}': " + "=".join(lp[1:])
            lines[-1] = "},"
            return lines

        return untree

    def dict_untree(self, inner_untree):
        def untree(key, value):
            lines = inner_untree(key, value)
            return lines

        untree.dict_repack = True
        return untree

    def list_untree(self, inner_untree):
        def untree(key, value):
            lines = inner_untree(key, value)
            lines[0] = lines[0].split("=")[0] + "=["
            lines.insert(1, "  {")
            lines[2:] = ["  " + line for line in lines[2:]]
            lines.append("],")
            return lines

        untree.list_repack = True
        return untree

    def argument_untree(self, key, value):
        return [f"{key}={repr(value)},"]

    def get_imports(self, cls):
        imports = {}
        if not any(m.startswith("_") for m in cls.__module__.split(".")):
            imports.setdefault(cls.__module__, []).append(cls.__name__)
        for attr in get_config_attributes(cls).values():
            if attr.is_node_type():
                for k, v in self.get_imports(attr.get_type()).items():
                    imports.setdefault(k, []).extend(v)

        return imports

    def get_import_lines(self, cls):
        return [
            f"from {key} import {', '.join(value)}"
            for key, value in self.get_imports(cls).items()
        ]


def setup(app):
    if "sphinx_design" not in app.extensions:
        from sphinx_design import setup as sphinx_design_setup

        sphinx_design_setup(app)

    app.add_node(
        AutoconfigNode,
        html=(visit_autoconfig_node, depart_autoconfig_node),
        latex=(visit_autoconfig_node, depart_autoconfig_node),
        text=(visit_autoconfig_node, depart_autoconfig_node),
    )
    app.add_directive("bsb_component_intro", ComponentIntro)
    app.add_directive("autoconfig", AutoconfigDirective)

    return {
        "version": "0.0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
