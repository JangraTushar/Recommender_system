import pandas as pd


def load_chapters(path):
    chapters = pd.read_csv(path)
    chapters.columns = [col.strip().lower() for col in chapters.columns]
    return chapters


def load_interactions(path):
    interactions = pd.read_csv(path)
    interactions.columns = [col.strip().lower() for col in interactions.columns]
    return interactions


def load_data(chapters_path, interactions_path):
    chapters = load_chapters(chapters_path)
    interactions = load_interactions(interactions_path)
    return chapters, interactions