from utils.log_utils import Logging
from evaluator.comparer import Comparer
from evaluator.weights import default_weights
import argparse
import pandas as pd
import pathlib 

if __name__ == "__main__":
    logger = Logging.get_logger("evaluator")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-sys",
        dest="system_output",
        help="The full path to the system output in parquet",
        type=str,
        default="annotations/annotations_original.csv"
    )

    parser.add_argument(
        "-gold",
        dest="gold_set",
        help="The full path to the gold set in parquet",
        type=str,
        default="annotations/annotations_corrected.csv"
    )

    parser.add_argument(
        "-m",
        "--model_name",
        dest="model_name",
        help="A model name to store the results",
        type=str,
        default="test"
    )

    parser.add_argument(
        "-null",
        "--null_penalty",
        dest="null_penalty",
        default=1,
        help="Null penalty, defaults to 1",
        type=float,
    )

    args = parser.parse_args()
    output_dir = f"evaluation_results/{args.model_name}"
    logger.info(f"Creating {output_dir} if it does not exist!")
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    sys = pd.read_csv(args.system_output)
    gold = pd.read_csv(args.gold_set)
    sys = sys[sys.UUID.isin(gold["UUID"].to_list())]
    sys = sys.sort_values("UUID")
    gold = gold.sort_values("UUID")

    comp = Comparer(args.null_penalty, target_columns=default_weights.keys())
    print(default_weights.keys())
    print(sys.columns)


    sys_data = sys[list(default_weights.keys())].to_dict(orient="records")
    gold_data = gold[list(default_weights.keys())].to_dict(orient="records")

    pairs = zip(sys_data, gold_data)
    comps = [
        [
            sys["UUID"],
            gold["UUID"],
            comp.weighted(sys, gold, default_weights),
            comp.all(sys, gold),
        ]
        for (sys, gold) in pairs
    ]

    all_comps = pd.DataFrame(
        [[i, j, c, d] + list(a.values()) for [i, j, (c, d), a] in comps],
        columns=["UUID1", "UUID2", "Coverage", "Weighted_Score"] + list(default_weights.keys()),
    ).replace({float("nan"): None})

    all_comps.sort_values("Weighted_Score")

    print(all_comps)