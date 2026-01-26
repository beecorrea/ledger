import yaml


class Category:
    def __init__(self, name, prefix=None) -> None:
        self.name = name
        self.prefix = prefix

    def id(self):
        if self.prefix == None:
            return self.name
        return "{}__{}".format(self.name, "-".join(self.prefix.lower().split()))


def build_categories(file="ledger.yaml"):
    res = []

    with open(file) as f:
        ledger = yaml.safe_load(f)
        cats = ledger["categories"]
        for cat in cats:
            res.append(Category(cat["name"], cat["key"]))

    return res
