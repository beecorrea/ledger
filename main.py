import src.etl.categorizer as categorizer
import src.etl.remainder as remainder
import src.etl.ingestor as ingestor
import src.structs.category as category
import src.structs.runtime.v2.duck as duck


def main():
    d = duck.DuckRuntime()
    models = list()

    models.append(ingestor.Ingestor("2026-01"))

    for cat in category.build_categories():
        models.append(categorizer.Categorizer(cat))

    models.append(remainder.Remainder())

    for model in models:
        d.run(model)


if __name__ == "__main__":
    main()
