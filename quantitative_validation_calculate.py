import os
import glob
import pandas as pd
import numpy as np
from statsmodels.stats.inter_rater import fleiss_kappa

FOLDER_PATH = "Validation_results"   # đổi thành folder chứa các file CSV
FILE_PATTERN = "*.csv"

REQUIRED_COLUMNS = [
    "AADL_model",
    "AADL_node_name",
    "IOT_RA_component",
    "validation_status_1",
    "validation_status_2",
    "validation_status_3",
]

RATER_COLUMNS = [
    "validation_status_1",
    "validation_status_2",
    "validation_status_3",
]

VALID_LABELS = {"Correct", "Incorrect", "Uncertain"}


def normalize_label(value: str) -> str:
    """Chuẩn hóa nhãn để tránh lỗi viết hoa/thừa khoảng trắng."""
    if pd.isna(value):
        return "Missing"
    value = str(value).strip()
    mapping = {
        "correct": "Correct",
        "incorrect": "Incorrect",
        "uncertain": "Uncertain",
    }
    return mapping.get(value.lower(), value)


def load_all_csvs(folder_path: str, pattern: str = "*.csv") -> pd.DataFrame:
    """Đọc tất cả CSV trong folder và gộp lại."""
    filepaths = sorted(glob.glob(os.path.join(folder_path, pattern)))
    if not filepaths:
        raise FileNotFoundError(f"Không tìm thấy file CSV nào trong: {folder_path}")

    dfs = []
    for fp in filepaths:
        df = pd.read_csv(fp)
        missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing_cols:
            raise ValueError(f"File {fp} thiếu các cột: {missing_cols}")
        df["__source_file"] = os.path.basename(fp)
        dfs.append(df)

    combined = pd.concat(dfs, ignore_index=True)
    return combined


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Chuẩn hóa nhãn, tạo key mapping, loại duplicate theo first occurrence."""
    for col in RATER_COLUMNS:
        df[col] = df[col].apply(normalize_label)

    df["mapping_key"] = list(
        zip(df["AADL_model"], df["AADL_node_name"], df["IOT_RA_component"])
    )

    df = df.drop_duplicates(subset=["mapping_key"], keep="first").copy()

    return df


def compute_majority_label(row: pd.Series) -> str:
    """Tính majority label cho 3 raters."""
    counts = row[RATER_COLUMNS].value_counts()

    if counts.max() == 1:
        return "NoMajority"
    return counts.idxmax()


def compute_agreement_type(row: pd.Series) -> str:
    """Phân loại mức độ agreement."""
    counts = row[RATER_COLUMNS].value_counts()
    max_count = counts.max()

    if max_count == 3:
        return "Strong (3/3)"
    elif max_count == 2:
        return "Moderate (2/3)"
    else:
        return "Disagreement"


def fleiss_kappa_from_df(df: pd.DataFrame) -> float:
    """
    Tính Fleiss' Kappa từ 3 cột rating.
    Chỉ dùng các label hợp lệ: Correct / Incorrect / Uncertain.
    """
    categories = ["Correct", "Incorrect", "Uncertain"]
    matrix = []

    for _, row in df.iterrows():
        counts = [sum(row[col] == cat for col in RATER_COLUMNS) for cat in categories]
        matrix.append(counts)

    matrix = np.array(matrix)
    return fleiss_kappa(matrix, method="fleiss")


def summarize_results(df: pd.DataFrame) -> None:
    """In ra toàn bộ kết quả quantitative validation."""
    df["majority_label"] = df.apply(compute_majority_label, axis=1)
    df["agreement_type"] = df.apply(compute_agreement_type, axis=1)

    total = len(df)

    majority_counts = df["majority_label"].value_counts().to_dict()
    agreement_counts = df["agreement_type"].value_counts().to_dict()

    majority_correct = majority_counts.get("Correct", 0)
    majority_incorrect = majority_counts.get("Incorrect", 0)
    majority_uncertain = majority_counts.get("Uncertain", 0)
    no_majority = majority_counts.get("NoMajority", 0)

    strong = agreement_counts.get("Strong (3/3)", 0)
    moderate = agreement_counts.get("Moderate (2/3)", 0)
    disagreement = agreement_counts.get("Disagreement", 0)

    kappa = fleiss_kappa_from_df(df)

    print("=" * 60)
    print("QUANTITATIVE VALIDATION RESULTS")
    print("=" * 60)
    print(f"Total unique mappings: {total}")
    print()

    print("Majority label distribution:")
    print(f"  Correct   : {majority_correct} ({majority_correct / total * 100:.2f}%)")
    print(f"  Incorrect : {majority_incorrect} ({majority_incorrect / total * 100:.2f}%)")
    print(f"  Uncertain : {majority_uncertain} ({majority_uncertain / total * 100:.2f}%)")
    if no_majority > 0:
        print(f"  NoMajority: {no_majority} ({no_majority / total * 100:.2f}%)")
    print()

    print("Agreement distribution:")
    print(f"  Strong agreement (3/3) : {strong} ({strong / total * 100:.2f}%)")
    print(f"  Moderate agreement (2/3): {moderate} ({moderate / total * 100:.2f}%)")
    print(f"  Disagreement           : {disagreement} ({disagreement / total * 100:.2f}%)")
    print()

    print(f"Majority-correct rate: {majority_correct / total * 100:.2f}%")
    print(f"Fleiss' Kappa: {kappa:.4f}")
    print("=" * 60)

    print(
        f"Overall, {majority_correct / total * 100:.1f}\\% of the mappings were marked as "
        f"correct by majority voting. Strong agreement (3/3 raters) was observed for "
        f"{strong / total * 100:.1f}\\% of the mappings, while "
        f"{moderate / total * 100:.1f}\\% showed moderate agreement (2/3 raters). "
        f"The computed Fleiss' kappa value was {kappa:.3f}."
    )


def main():
    df = load_all_csvs(FOLDER_PATH, FILE_PATTERN)
    df = prepare_dataframe(df)
    summarize_results(df)


if __name__ == "__main__":
    main()


