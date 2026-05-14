import pandas as pd


def generate_next_chapter_candidates(progress_df: pd.DataFrame, chapters_df: pd.DataFrame) -> pd.DataFrame:
    progress_df = progress_df.copy()
    progress_df["candidate_seq"] = progress_df["last_seq_read"] + 1

    candidates = progress_df.merge(
        chapters_df[
            [
                "book_id",
                "chapter_id",
                "chapter_sequence_no",
                "author_id",
                "published_date",
                "tags",
                "tag_list",
            ]
        ],
        left_on=["book_id", "candidate_seq"],
        right_on=["book_id", "chapter_sequence_no"],
        how="left",
    )

    candidates = candidates.dropna(subset=["chapter_id"]).copy()

    candidates = candidates.rename(
        columns={
            "chapter_id": "candidate_chapter_id",
            "author_id": "candidate_author_id",
            "tags": "candidate_tags",
            "tag_list": "candidate_tag_list",
            "published_date": "candidate_published_date",
        }
    )

    return candidates[
        [
            "user_id",
            "book_id",
            "last_seq_read",
            "chapters_read",
            "candidate_seq",
            "candidate_chapter_id",
            "candidate_author_id",
            "candidate_published_date",
            "candidate_tags",
            "candidate_tag_list",
        ]
    ]


def generate_popularity_fallback(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    fallback = (
        df.groupby(
            [
                "book_id",
                "chapter_id",
                "author_id",
                "published_date",
                "tags",
            ]
        )
        .size()
        .reset_index(name="popularity_score")
        .sort_values("popularity_score", ascending=False)
        .head(top_n)
    )

    fallback["candidate_tag_list"] = fallback["tags"].apply(
        lambda x: [tag.strip().lower() for tag in str(x).split("|") if tag.strip()]
    )

    fallback = fallback.rename(
        columns={
            "chapter_id": "candidate_chapter_id",
            "author_id": "candidate_author_id",
            "published_date": "candidate_published_date",
            "tags": "candidate_tags",
        }
    )

    return fallback