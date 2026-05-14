from src.config import CHAPTERS_PATH, INTERACTIONS_PATH, OUTPUT_DIR, TOP_K, RANDOM_SEED
from src.utils import set_seed, save_json, save_csv, ensure_dir
from src.data_loader import load_data
from src.preprocessing import preprocess_chapters, preprocess_interactions, merge_data
from src.feature_engineering import (
    build_user_book_progress,
    build_user_tag_profile,
    build_user_author_profile,
    build_popularity_table,
)
from src.candidate_generation import generate_next_chapter_candidates
from src.ranking import add_tag_scores, add_author_scores, score_candidates, rank_top_k
from src.evaluation import leave_last_chapter_out, build_ground_truth, evaluate_recommendations


def main():
    set_seed(RANDOM_SEED)
    ensure_dir(OUTPUT_DIR)

    chapters_raw, interactions_raw = load_data(CHAPTERS_PATH, INTERACTIONS_PATH)

    chapters = preprocess_chapters(chapters_raw)
    interactions = preprocess_interactions(interactions_raw)

    merged_df = merge_data(interactions, chapters)

    train_df, test_df = leave_last_chapter_out(merged_df)

    user_progress = build_user_book_progress(train_df)
    user_tag_profile = build_user_tag_profile(train_df)
    user_author_profile = build_user_author_profile(train_df)
    popularity_table = build_popularity_table(train_df)

    candidates = generate_next_chapter_candidates(user_progress, chapters)
    candidates = add_tag_scores(candidates, user_tag_profile)
    candidates = add_author_scores(candidates, user_author_profile)
    candidates = score_candidates(candidates)

    ranked_recommendations = rank_top_k(candidates, k=TOP_K)

    ground_truth = build_ground_truth(test_df)
    metrics = evaluate_recommendations(ranked_recommendations, ground_truth, k=TOP_K)

    eda_summary = merged_df.agg({
        "user_id": "nunique",
        "book_id": "nunique",
        "chapter_id": "nunique"
    }).reset_index()
    eda_summary.columns = ["metric", "value"]

    save_csv(eda_summary, OUTPUT_DIR / "eda_summary.csv")
    save_csv(ranked_recommendations.head(100), OUTPUT_DIR / "recommendations_sample.csv")
    save_json(metrics, OUTPUT_DIR / "metrics.json")

    print("Pipeline executed successfully.")
    print("Metrics:", metrics)
    print("Popularity table sample:")
    print(popularity_table.head())


if __name__ == "__main__":
    main()