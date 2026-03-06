import os
import glob
import re
import pandas as pd

def normalize_name(s: str) -> str:
    """Lower, split underscores/camelCase, strip punctuation, collapse spaces."""
    if not isinstance(s, str):
        s = str(s) if s is not None else ""
    s = s.strip().replace("_", " ").replace("-", " ")
    s = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", s)  # camelCase → camel Case
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def split_labels(label: str):
    """Split label string by '/', trim, drop empty."""
    if label is None or (isinstance(label, float) and pd.isna(label)):
        return []
    label = str(label).strip()
    if not label:
        return []
    return [x.strip() for x in label.split("/") if x.strip()]

def union_labels(series: pd.Series) -> str:
    """
    Union labels across rows, keep stable order:
    first appearance order across the group.
    """
    seen = set()
    out = []
    for v in series:
        for lab in split_labels(v):
            if lab not in seen:
                seen.add(lab)
                out.append(lab)
    return "/".join(out)

def build_mapping_csv(input_folder: str, output_csv_path: str):
    csv_paths = sorted(glob.glob(os.path.join(input_folder, "*.csv")))
    if not csv_paths:
        raise FileNotFoundError(f"No CSV files found in: {input_folder}")

    frames = []
    required_cols = {"AADL_model", "AADL_node_name", "final_label"}

    for path in csv_paths:
        # dtype=str để tránh pandas tự convert + giữ nguyên nội dung
        df = pd.read_csv(path, dtype=str, keep_default_na=False)

        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"File {os.path.basename(path)} missing columns: {sorted(missing)}")

        frames.append(df[list(required_cols)].copy())

    all_df = pd.concat(frames, ignore_index=True)

    all_df["AADL_model"] = all_df["AADL_model"].astype(str).str.strip()
    all_df["AADL_node_name"] = all_df["AADL_node_name"].astype(str).str.strip()
    all_df["final_label"] = all_df["final_label"].astype(str).str.strip()

    grouped = (
        all_df.groupby(["AADL_model", "AADL_node_name"], as_index=False)
             .agg({"final_label": union_labels})
    )

    out = grouped.rename(columns={
        "AADL_node_name": "component_name",
        "final_label": "ra_component"
    })

    out["normalized_name"] = out["component_name"].apply(normalize_name)

    out = out[["AADL_model", "component_name", "normalized_name", "ra_component"]]

    out.to_csv(output_csv_path, index=False, encoding="utf-8")
    print(f"Saved: {output_csv_path} | rows={len(out)} | input_files={len(csv_paths)}")

if __name__ == "__main__":
    INPUT_FOLDER = "Validation_results"
    OUTPUT_CSV = "Component_mapping/iot_ra_component_mapping_labels.csv"
    build_mapping_csv(INPUT_FOLDER, OUTPUT_CSV)