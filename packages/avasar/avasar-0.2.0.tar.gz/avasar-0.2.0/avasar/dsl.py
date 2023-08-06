from dataclasses import dataclass
from pathlib import Path
from typing import Union
from collections import defaultdict
from itertools import combinations
import toml  # type: ignore
import random

_default = object()
_base = Path(__file__).parent
_data = Path(_base, "data")

# TODO: make words.firstname possible


class Namespace:
    pass


class Context:
    def fstr(self, template):
        return eval(f"f'''{template}'''", self.__dict__)


def set_path(context, path, value):
    parts = path.strip().split(".")
    cur = context
    for x in parts[:-1]:
        if hasattr(cur, x):
            cur = getattr(cur, x)
        else:
            new = Namespace()
            setattr(cur, x, new)
            cur = new
    setattr(cur, parts[-1], value)


class Transform:
    def draw(self, n):
        result = []
        copy = self.strings
        random.shuffle(copy)
        for i in range(n):
            result.append(copy[i])
        return Items(self.context, result)

    def take(self, n):
        return Items(self.context, self._strings[0:n])

    def set(self, name):
        set_path(self.context, name, self)
        return self

    def choose(self, n):
        results = []
        for _ in range(n):
            results.append(random.choice(self._strings))
        return Items(self.context, results)

    @property
    def choice(self):
        return Items(self.context, [random.choice(self._strings)])

    @property
    def lower(self):
        return Items(self.context, [x.lower() for x in self.strings])

    @property
    def capitalize(self):
        return Items(self.context, [f"{x[0].upper()}{x[1:]}" for x in self.strings])

    def __repr__(self):
        return self.__str__()


@dataclass
class Items(Transform):
    context: Context
    _items: list[str]

    @property
    def _strings(self):
        return self._items

    @property
    def strings(self):
        return list(self._items)

    def __str__(self):
        if any([("\n" in x) for x in self._items]):
            return self.context.fstr("\n-\n".join(self._items))
        else:
            return self.context.fstr(", ".join(self._items))

    def __repr__(self):
        return self.__str__()


@dataclass
class Text(Transform):
    context: Context
    name: str
    _items: dict[frozenset, list[str]]

    def groups(self, *args):
        result = []
        for group in args:
            if isinstance(group, str):
                group = frozenset([group])
            elif isinstance(group, set):
                group = frozenset(group)
            result.extend(self._items[group])
        return Items(self.context, result)

    @property
    def _strings(self):
        return self.strings

    @property
    def strings(self):
        result = []
        for group in self._items.values():
            result.extend(group)
        return result

    def set(self, name):
        item = Items(self.context, [random.choice(self._items[_default])])
        set_path(self.context, name, item)
        return item

    @property
    def items(self):
        return Items(self.context, self.strings)

    def __str__(self):
        return self.context.fstr(random.choice(self._items[_default]))

    def __repr__(self):
        return self.__str__()


def build_context():
    context = Context()
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
                items = [x.strip() for x in items]
                items = [x for x in items if x]
                avasar["items"] = items
                combs = set()
                for i in range(len(groups)):
                    for x in combinations(groups, i + 1):
                        combs.add(frozenset(x))
                for comb in combs:
                    map[avasar["name"]][comb].extend(avasar["items"])
                else:
                    map[avasar["name"]][_default].extend(avasar["items"])
    for name, groups in map.items():
        group = defaultdict(list)
        for key, item in groups.items():
            if isinstance(key, frozenset) and len(key) == 1:
                gr_name = list(key)[0]
                group[gr_name] = Text(context, gr_name, {_default: item})
        ns = Namespace()
        ns.__dict__ = group
        obj = Text(context, name, groups)
        obj.group = ns
        set_path(context, name, obj)
    return context
