# Recommendation Engine Evaluation Report

This report presents the performance metrics of the hybrid recommendation engine.

## Performance Summary

| Metric | Score |
| --- | --- |
| **Precision@5** | 0.22 |
| **Recall@5** | 0.45 |
| **NDCG@5** | 0.4122 |

## Methodology
- **Ground Truth**: Content items rated >= 4.0 by users in the database.
- **Evaluation Size**: Evaluated across all users who have sufficient ratings data.
- **Recommendation Limit**: Top-5 candidates computed using candidate generators (collaborative + content) and sorted by the RecommendationScorer using popularity, recency, and skill-relevance weights.
