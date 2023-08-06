from dataclasses import dataclass, field
from pathlib import Path
from typing import Union, Optional
from collections import defaultdict
from itertools import combinations
import toml  # type: ignore
import random

_default = object()
_base = Path(__file__).parent
_data = Path(_base, "data")

# TODO: introduce conditionals
# TODO: system for probability (using indexes and normal-distribution random value


@dataclass
class TransparentString:
    value: str

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


class All:
    @property
    def all(self):
        result = []
        size = 0
        for name in self._all.keys():
            size = max(size, len(name))
        for name, value in self._all.items():
            name = name.rjust(size)
            value = capitalize(str(value))
            result.append(f"{name} | {value}")
        return TransparentString("\n".join(result))


@dataclass
class Namespace(All):
    _all: dict[str, "Text"] = field(default_factory=dict)


@dataclass
class Context(All):
    _groups: Optional[list[frozenset[str]]] = None
    _all: dict[str, "Text"] = field(default_factory=dict)

    def _set_groups(self, *args):
        groups = set()
        for group in args:
            if isinstance(group, str):
                group = frozenset([group])
            elif isinstance(group, set):
                group = frozenset(group)
            groups.add(group)
        self._groups = frozenset(groups)

    def fstr(self, template):
        return eval(f"f'''{template}'''", self.__dict__)


class Transform:
    def draw(self, n):
        result = []
        copy = self.strings
        random.shuffle(copy)
        for i in range(n):
            result.append(copy[i])
        return Items(self._context, result)

    def take(self, n):
        return Items(self._context, self._strings[0:n])

    def set(self, name):
        set_path(self._context, name, self)
        return self

    def choose(self, n):
        results = []
        for _ in range(n):
            results.append(random.choice(self._strings))
        return Items(self._context, results)

    @property
    def choice(self):
        return Items(self._context, [random.choice(self._strings)])

    @property
    def lower(self):
        return Items(self._context, [x.lower() for x in self._strings])

    @property
    def capitalize(self):
        return Items(self._context, [capitalize(x) for x in self._strings])

    def __repr__(self):
        return self.__str__()


@dataclass
class Items(Transform):
    _context: Context
    _items: list[str]

    @property
    def _strings(self):
        return self._items

    @property
    def strings(self):
        return list(self._items)

    def __str__(self):
        items = self._strings
        if any([("\n" in x) for x in items]):
            return self._context.fstr("\n-\n".join(self._strings))
        else:
            return self._context.fstr(", ".join(self._strings))

    def __repr__(self):
        return self.__str__()


@dataclass
class Text(Transform, All):
    name: str
    _context: Context
    _items: dict[frozenset, list[str]]
    _all: dict[str, "Text"] = field(default_factory=dict)

    def _groups(self, *args):
        groups = set()
        for group in args:
            if isinstance(group, str):
                group = frozenset([group])
            elif isinstance(group, set):
                group = frozenset(group)
            groups.add(group)
        result = []
        for group in groups:
            result.extend(self._items[group])
        result = list(sorted(set(result)))
        return result

    def groups(self, *args):
        return Items(self._context, self._groups(*args))

    def _groups_from_items(self):
        return frozenset(self._items.keys())

    @property
    def _strings(self):
        groups = self._context._groups
        if groups and groups & self._groups_from_items():
            return self._groups(*groups)
        else:
            return self._items[_default]

    @property
    def strings(self):
        groups = self._context._groups
        if groups and groups & self._groups_from_items():
            return self._groups(*groups)
        else:
            return list(self._items[_default])

    def set(self, name):
        item = Items(self._context, [random.choice(self._strings)])
        set_path(self.context, name, item)
        return item

    @property
    def items(self):
        return Items(self._context, self._strings)

    def __str__(self):
        return self._context.fstr(random.choice(self._strings))

    def __repr__(self):
        return self.__str__()


def capitalize(string):
    if len(string) > 0:
        return f"{string[0].upper()}{string[1:]}"
    else:
        return string


def split_and_capitalize(string, split, join):
    return join.join([capitalize(x) for x in string.split(split)])


def niceup_string(string):
    string = split_and_capitalize(string, ".", " - ")
    string = split_and_capitalize(string, "_", " ")
    return string


def set_path(context, path, value, all=False):
    parts = path.strip().split(".")
    cur = context
    prefix = 0
    for x in parts[:-1]:
        if all and isinstance(value, Text):
            cur._all[niceup_string(value.name[prefix:])] = value
            prefix += len(x) + 1
        if hasattr(cur, x):
            cur = getattr(cur, x)
        else:
            new = Namespace()
            setattr(cur, x, new)
            cur = new
    try:
        if all and isinstance(value, Text):
            cur._all[niceup_string(value.name[prefix:])] = value
        if all:
            value._all[niceup_string(value.name[prefix:])] = value
    except AttributeError:
        print(path)
        raise
    cur._all[niceup_string(value.name[prefix:])] = value
    setattr(cur, parts[-1], value)


def build_context():
    context = Context()
    read_toml(context)

    return context


def read_toml(context):
    map = defaultdict(lambda: defaultdict(list))
    for file in _data.iterdir():
        if file.is_file() and file.name.endswith(".toml"):
            with open(file, "r", encoding="UTF-8") as f:
                data = toml.load(f)
            for avasar in data["avasar"]:
                groups = avasar.get("groups")
                if not groups:
                    groups = []
                items = avasar["items"]
                if isinstance(items, str):
                    items = items.strip().splitlines()
                items = [x.strip().replace("\\s", " ") for x in items]
                avasar["items"] = items
                combs = set()
                for i in range(len(groups)):
                    for x in combinations(groups, i + 1):
                        combs.add(frozenset(x))
                name = avasar["name"]
                if isinstance(name, list):
                    for comb in combs:
                        for x in name:
                            map[x][comb].extend(avasar["items"])
                    for x in name:
                        map[x][_default].extend(avasar["items"])
                else:
                    for comb in combs:
                        map[name][comb].extend(avasar["items"])
                    map[name][_default].extend(avasar["items"])
    for name in sorted(map.keys()):
        groups = map[name]
        group = defaultdict(list)
        for key, item in groups.items():
            item = list(sorted(set(item)))
            groups[key] = item
            if isinstance(key, frozenset) and len(key) == 1:
                gr_name = list(key)[0]
                group[gr_name] = Text(gr_name, context, {_default: item})
        ns = Namespace()
        ns.__dict__ = group
        obj = Text(name, context, groups)
        obj.group = ns
        set_path(context, name, obj, all=True)
