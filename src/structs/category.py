import yaml


class Category:
    def __init__(self, name, prefix=None) -> None:
        self.name = name
        self.prefix = prefix

    def id(self):
        if self.prefix == None:
            return self.name
        return "{}__{}".format(self.name, "-".join(self.prefix.lower().split()))


def build_categories(categories: list):
    res = []
    for cat in categories:
        res.append(Category(cat["name"], cat["key"]))

    return res
