# Sequential Reading Recommendation System

A modular recommendation system that predicts **what a user should read next** from their reading history by modeling **chapter-level progression within books** and enriching recommendations with **author** and **tag** preferences. This project is intentionally scoped as a **next-chapter recommendation** problem because the assignment highlights that chapters are ordered and that user progression within a book carries important sequential signal beyond flat interactions.

---

## Project Objective

The goal of this project is to build a recommendation system that predicts the **next most relevant chapter** for a user based on their past reading behavior. The core idea is that chapter interactions are not independent events; they are part of an ordered reading journey inside a book, so the model should use chapter sequence information directly rather than treating all interactions as unrelated items.

This project defines the recommendation problem as:

> **Given a user’s chapter interaction history, recommend the next chapter they are most likely to read.**

This is a deliberate and practical interpretation of the assignment because recommending the next chapter is one of the explicitly suggested directions, and it aligns closely with the dataset structure.

---

## Dataset Schema

The solution is built using only the provided files, in line with the assignment constraint that no external data sources should be used.

### `chapters.csv`
Contains chapter metadata with the following columns:

- `chapter_id`
- `chapter_sequence_no`
- `book_id`
- `author_id`
- `published_date`
- `tags`

### `interaction.csv` / `interactions.csv`
Contains user interaction records with:

- `user_id`
- `book_id`
- `chapter_id`

---

## Problem Framing

This project treats the task as a **chapter-level sequential recommendation problem** rather than a generic collaborative filtering problem. That choice is based on the assignment’s explicit note that chapter order matters and that flat interaction data alone cannot capture user progression within books.

### Why this framing?

- Chapters belong to books and follow a natural reading order. [file:2]
- If a user has already read chapter \(n\), the next strong candidate is often chapter \(n+1\).
- User preferences such as author affinity and tag affinity can help rank candidates when multiple reading paths are possible.
- A simple, interpretable sequential baseline is a strong fit for a time-constrained assignment where practical thinking matters more than unnecessary complexity.

---

## Approach

The recommender uses a **hybrid sequential ranking pipeline** with the following logic:

1. Reconstruct each user’s reading progress within every book.
2. Identify the latest chapter reached by the user in that book.
3. Generate the next sequential chapter as the primary candidate.
4. Re-rank candidates using user preference signals derived from:
   - `author_id`
   - `tags`
5. Evaluate whether the held-out actual next chapter appears in the top-K recommendations.

This design intentionally prioritizes **sequence awareness**, because the assignment emphasizes that user progression within a book is a key signal.

---

## Key Assumptions

To scope the problem clearly, the following assumptions were made:

- A user interaction with a chapter indicates meaningful reading engagement.
- Users generally move forward through books in chapter order.
- `tags` provide useful signals about topical preference.
- `author_id` helps capture creator-level reading affinity.
- Users with little or no history are difficult to personalize deeply without external information, so popularity-based fallback is the most practical cold-start strategy under the assignment constraints.

---

## Project Structure

```text
reading_recommender/
│
├── data/
│   ├── chapters.csv
│   └── interaction.csv
│
├── outputs/
│   ├── metrics.json
│   ├── recommendations_sample.csv
│   └── eda_summary.csv
│
├── src/
│   ├── config.py
│   ├── utils.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── candidate_generation.py
│   ├── ranking.py
│   ├── evaluation.py
│   └── main.py
│
├── requirements.txt
└── README.md
```

---

## Module Overview

### `config.py`
Stores project paths, output locations, seed values, and evaluation settings.

### `utils.py`
Contains helper utilities for:
- setting random seed,
- saving CSV and JSON outputs,
- creating folders if needed.

### `data_loader.py`
Responsible for loading:
- `chapters.csv`
- `interaction.csv`

and standardizing column names.

### `preprocessing.py`
Handles:
- schema validation,
- type conversion,
- duplicate removal,
- date parsing,
- tag splitting,
- merging interaction data with chapter metadata.

### `feature_engineering.py`
Builds:
- user-book reading progress,
- user tag preference profiles,
- user author preference profiles,
- global popularity statistics.

### `candidate_generation.py`
Generates:
- next-chapter candidates based on sequence progression,
- optional popularity-based fallback candidates.

### `ranking.py`
Scores and ranks recommendations using:
- sequential score,
- tag affinity score,
- author affinity score.

### `evaluation.py`
Implements:
- leave-last-chapter-out evaluation,
- Precision@K,
- Recall@K,
- Hit Rate@K,
- MRR.

### `main.py`
Runs the entire pipeline end to end:
- load data,
- preprocess,
- engineer features,
- generate candidates,
- rank,
- evaluate,
- save outputs.

---

## Recommendation Logic

The model follows a simple but effective ranking strategy:

### 1. Sequential candidate generation
For each user-book pair, the system finds the highest chapter sequence reached and recommends the next chapter in that same book if it exists.

### 2. Preference-based reranking
Candidates are then re-scored using:
- similarity to the user’s historical `tags`,
- frequency of reading the same `author_id`.

### 3. Final ranking
A weighted score is used to prioritize the final top-K recommendations.

This combination keeps the recommender both **interpretable** and **aligned with the structure of the data**.

---

## Evaluation Strategy

The model is evaluated using a **leave-last-chapter-out** setup:

- For each user-book reading sequence, the final interacted chapter is held out.
- The model is trained using the earlier chapters in the sequence.
- The held-out chapter is treated as the ground truth next item.
- The model is then evaluated on whether it successfully ranks that chapter in the top-K recommendations.

This evaluation setup is appropriate because the project is framed as a next-chapter prediction task, and the assignment explicitly asks how recommendation quality is measured.

### Metrics Reported

- **Precision@5**
- **Recall@5**
- **Hit Rate@5**
- **MRR** (Mean Reciprocal Rank)

These metrics provide both ranking quality and retrieval quality for next-item recommendation.

---

## Sample Result Interpretation

A successful run produces outputs such as:

- `metrics.json` → final evaluation metrics
- `recommendations_sample.csv` → top recommendation samples
- `eda_summary.csv` → high-level dataset summary

Example interpretation:
- **Hit Rate@5** tells how often the actual next chapter appears in the top 5.
- **MRR** indicates how high the correct chapter is ranked when it appears.
- **Precision@5** shows how relevant the top 5 recommendations are overall.

---

## How to Run

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd reading_recommender
```

### 2. Create and activate a virtual environment

**Windows**
```bash
python -m venv recsys
recsys\Scripts\activate
```

**Linux / Mac**
```bash
python3 -m venv recsys
source recsys/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Place the dataset files in the `data/` folder

Expected files:

```text
data/chapters.csv
data/interaction.csv
```

### 5. Run the project

```bash
python -m src.main
```

---

## Outputs

After execution, the following files are generated in the `outputs/` folder:

- `metrics.json`
- `recommendations_sample.csv`
- `eda_summary.csv`

---

## Design Decisions and Tradeoffs

This project intentionally uses a **modular, interpretable baseline** rather than a heavy deep learning model. That decision was made for three reasons:

1. The assignment expects practical thinking and tradeoff awareness, not unnecessary complexity.
2. The dataset structure strongly favors a sequence-aware solution because chapter order is central to the problem.
3. A clean, reproducible, well-evaluated baseline is more valuable in a 4–6 hour assignment setting than a partially finished advanced model. [file:2]

### What was prioritized
- Strong alignment with the assignment goal.
- Clear problem framing.
- Reproducible code structure.
- Appropriate evaluation.
- Simplicity and readability.

### What was intentionally not prioritized
- Production deployment,
- distributed infrastructure,
- deep neural sequential models,
- external metadata enrichment,

because the assignment explicitly states that only a clean working script is required and no production setup is expected.

---

## Limitations

While the current system is a solid baseline, it has a few limitations:

- It is strongest for users who already have sequential reading history.
- It does not deeply personalize for true cold-start users.
- It focuses on **next chapter** recommendation rather than **new book** recommendation.
- It uses rule-based / weighted ranking instead of learned ranking.

These are acceptable limitations for the assignment’s time and scope, but they also point directly to meaningful next steps.
---

## Future Improvements

Given more time, the following extensions would be valuable:

- Add a stronger cold-start module using global popularity and tag priors.
- Extend the system to also recommend **new books** to start.
- Learn ranking weights instead of setting them manually.
- Add diversity and novelty metrics.
- Experiment with sequence models such as Markov chains, GRU-based recommenders, or Transformer-based session models.
- Compare chapter-level recommendation against book-level recommendation as an alternative framing.

---

## Why This Project Is a Good Fit for the Assignment

This solution is intentionally designed to match the assignment’s core expectations:

- It builds a recommendation system from user reading history. 
- It uses the sequential nature of chapters directly, which is a key requirement implied by the dataset. 
- It includes evaluation and measurable outputs.
- It keeps the code clean, readable, modular, and reproducible.
- It clearly reflects practical tradeoffs rather than overengineering. 

---

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn

---

## Submission Note

This repository contains the full code, project structure, and evaluation pipeline for a chapter-level sequential recommendation baseline. The implementation is intentionally scoped to produce a clean, interpretable, and reproducible solution within the assignment constraints while remaining aligned to the dataset’s strongest signal: **reading progression within books**.