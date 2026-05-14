import pandas as pd
import numpy as np


def leave_last_chapter_out(df: pd.DataFrame):
    df = df.sort_values(
        by=["user_id", "book_id", "chapter_sequence_no"]
    ).copy()

    test_idx = df.groupby(["user_id", "book_id"]).tail(1).index
    test_df = df.loc[test_idx].copy()
    train_df = df.drop(test_idx).copy()

    return train_df, test_df


def build_ground_truth(test_df: pd.DataFrame) -> pd.DataFrame:
    ground_truth = test_df[["user_id", "chapter_id"]].copy()
    ground_truth = ground_truth.rename(columns={"chapter_id": "actual_chapter_id"})
    return ground_truth


def precision_at_k(actual, predicted, k=5):
    predicted_k = predicted[:k]
    if len(predicted_k) == 0:
        return 0.0
    return len(set(actual) & set(predicted_k)) / len(predicted_k)


def recall_at_k(actual, predicted, k=5):
    predicted_k = predicted[:k]
    if len(actual) == 0:
        return 0.0
    return len(set(actual) & set(predicted_k)) / len(actual)


def hit_rate_at_k(actual, predicted, k=5):
    predicted_k = predicted[:k]
    return 1.0 if len(set(actual) & set(predicted_k)) > 0 else 0.0


def reciprocal_rank(actual, predicted):
    for i, item in enumerate(predicted, start=1):
        if item in actual:
            return 1.0 / i
    return 0.0


def evaluate_recommendations(ranked_df: pd.DataFrame, ground_truth_df: pd.DataFrame, k: int = 5) -> dict:
    pred_df = ranked_df.groupby("user_id")["candidate_chapter_id"].apply(list).reset_index()
    gt_df = ground_truth_df.groupby("user_id")["actual_chapter_id"].apply(list).reset_index()

    merged = pred_df.merge(gt_df, on="user_id", how="inner")

    precisions, recalls, hits, mrrs = [], [], [], []

    for _, row in merged.iterrows():
        actual = row["actual_chapter_id"]
        predicted = row["candidate_chapter_id"]

        precisions.append(precision_at_k(actual, predicted, k))
        recalls.append(recall_at_k(actual, predicted, k))
        hits.append(hit_rate_at_k(actual, predicted, k))
        mrrs.append(reciprocal_rank(actual, predicted))

    metrics = {
        f"precision@{k}": float(np.mean(precisions)) if precisions else 0.0,
        f"recall@{k}": float(np.mean(recalls)) if recalls else 0.0,
        f"hit_rate@{k}": float(np.mean(hits)) if hits else 0.0,
        "mrr": float(np.mean(mrrs)) if mrrs else 0.0,
        "evaluated_users": int(len(merged)),
    }

    return metrics