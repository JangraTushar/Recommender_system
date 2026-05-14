import pandas as pd


REQUIRED_CHAPTER_COLS = [
    "chapter_id",
    "chapter_sequence_no",
    "book_id",
    "author_id",
    "published_date",
    "tags",
]

REQUIRED_INTERACTION_COLS = [
    "user_id",
    "book_id",
    "chapter_id",
]


def validate_columns(df: pd.DataFrame, required_cols: list, df_name: str):
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"{df_name} is missing columns: {missing}")


def preprocess_chapters(chapters: pd.DataFrame) -> pd.DataFrame:
    validate_columns(chapters, REQUIRED_CHAPTER_COLS, "chapters.csv")

    chapters = chapters.copy()
    chapters["chapter_sequence_no"] = pd.to_numeric(
        chapters["chapter_sequence_no"], errors="coerce"
    )
    chapters["published_date"] = pd.to_datetime(
        chapters["published_date"], errors="coerce"
    )
    chapters["author_id"] = chapters["author_id"].astype(str)
    chapters["tags"] = chapters["tags"].fillna("").astype(str)

    chapters = chapters.dropna(subset=["chapter_id", "book_id", "chapter_sequence_no"])
    chapters = chapters.drop_duplicates(subset=["chapter_id"])

    chapters["chapter_sequence_no"] = chapters["chapter_sequence_no"].astype(int)
    chapters["tag_list"] = chapters["tags"].apply(
        lambda x: [tag.strip().lower() for tag in x.split("|") if tag.strip()]
    )
    return chapters


def preprocess_interactions(interactions: pd.DataFrame) -> pd.DataFrame:
    validate_columns(interactions, REQUIRED_INTERACTION_COLS, "interaction.csv")

    interactions = interactions.copy()
    interactions = interactions.dropna(subset=["user_id", "book_id", "chapter_id"])
    interactions = interactions.drop_duplicates()

    return interactions


def merge_data(interactions: pd.DataFrame, chapters: pd.DataFrame) -> pd.DataFrame:
    df = interactions.merge(
        chapters,
        on=["book_id", "chapter_id"],
        how="inner"
    )

    df = df.sort_values(
        by=["user_id", "book_id", "chapter_sequence_no"]
    ).reset_index(drop=True)

    return df