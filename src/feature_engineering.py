import pandas as pd
from collections import Counter


def build_user_book_progress(df: pd.DataFrame) -> pd.DataFrame:
    progress = (
        df.groupby(["user_id", "book_id"])
        .agg(
            last_seq_read=("chapter_sequence_no", "max"),
            chapters_read=("chapter_id", "nunique"),
            last_author_id=("author_id", "last"),
        )
        .reset_index()
    )
    return progress


def build_user_tag_profile(df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for user_id, group in df.groupby("user_id"):
        tag_counter = Counter()

        for tags in group["tag_list"]:
            tag_counter.update(tags)

        total = sum(tag_counter.values())
        if total == 0:
            continue

        for tag, count in tag_counter.items():
            rows.append(
                {
                    "user_id": user_id,
                    "tag": tag,
                    "tag_score": count / total,
                }
            )

    return pd.DataFrame(rows)


def build_user_author_profile(df: pd.DataFrame) -> pd.DataFrame:
    author_profile = (
        df.groupby(["user_id", "author_id"])
        .size()
        .reset_index(name="author_count")
    )

    author_profile["author_score"] = author_profile.groupby("user_id")[
        "author_count"
    ].transform(lambda x: x / x.sum())

    return author_profile


def build_popularity_table(df: pd.DataFrame) -> pd.DataFrame:
    popularity = (
        df.groupby(["book_id", "chapter_id"])
        .size()
        .reset_index(name="popularity_score")
        .sort_values("popularity_score", ascending=False)
    )
    return popularity