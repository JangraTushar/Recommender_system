import pandas as pd


def add_tag_scores(candidates: pd.DataFrame, user_tag_profile: pd.DataFrame) -> pd.DataFrame:
    if user_tag_profile.empty:
        candidates["tag_score"] = 0.0
        return candidates

    exploded = candidates[
        ["user_id", "candidate_chapter_id", "candidate_tag_list"]
    ].explode("candidate_tag_list")

    exploded = exploded.rename(columns={"candidate_tag_list": "tag"})

    exploded = exploded.merge(
        user_tag_profile,
        on=["user_id", "tag"],
        how="left"
    )

    tag_scores = (
        exploded.groupby(["user_id", "candidate_chapter_id"])["tag_score"]
        .sum()
        .reset_index()
    )

    candidates = candidates.merge(
        tag_scores,
        on=["user_id", "candidate_chapter_id"],
        how="left"
    )

    candidates["tag_score"] = candidates["tag_score"].fillna(0.0)
    return candidates


def add_author_scores(candidates: pd.DataFrame, user_author_profile: pd.DataFrame) -> pd.DataFrame:
    if user_author_profile.empty:
        candidates["author_score"] = 0.0
        return candidates

    candidates = candidates.merge(
        user_author_profile[["user_id", "author_id", "author_score"]].rename(
            columns={"author_id": "candidate_author_id"}
        ),
        on=["user_id", "candidate_author_id"],
        how="left"
    )

    candidates["author_score"] = candidates["author_score"].fillna(0.0)
    return candidates


def score_candidates(candidates: pd.DataFrame) -> pd.DataFrame:
    candidates = candidates.copy()

    candidates["sequential_score"] = 1.0

    candidates["score"] = (
        0.65 * candidates["sequential_score"]
        + 0.20 * candidates["tag_score"]
        + 0.15 * candidates["author_score"]
    )

    return candidates


def rank_top_k(candidates: pd.DataFrame, k: int = 5) -> pd.DataFrame:
    ranked = candidates.sort_values(
        by=["user_id", "score"],
        ascending=[True, False]
    ).copy()

    ranked["rank"] = ranked.groupby("user_id").cumcount() + 1
    ranked = ranked[ranked["rank"] <= k].copy()

    return ranked