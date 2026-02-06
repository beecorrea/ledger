import src.etl.categorizer as categorizer
import src.etl.remainder as remainder
import src.etl.ingestor as ingestor
import src.structs.category as category
import src.structs.runtime.v2.duck as duck
import src.structs.ledger as ledger


def main():
    ldg = ledger.Ledger()
    d = duck.DuckRuntime(ldg.database["name"])

    for target in ldg.ingestion["targets"]:
        models = list()
        models.append(ingestor.Ingestor(target))

        for cat in category.build_categories(ldg.categories):
            models.append(categorizer.Categorizer(cat))

        models.append(remainder.Remainder())

        for model in models:
            d.run(model)
        print()


if __name__ == "__main__":
    main()
