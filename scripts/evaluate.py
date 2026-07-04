import sys
import os


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from data.database import SessionLocal
from data.models import User, Interaction
from engine.orchestrator import RecommendationOrchestrator
from engine.evaluator import RecommendationEvaluator

def run_evaluation():
    db = SessionLocal()
    orchestrator = RecommendationOrchestrator(db)
    evaluator = RecommendationEvaluator()


    ground_truth = {}
    users = db.query(User).all()
    for u in users:
        high_ratings = (
            db.query(Interaction)
            .filter(
                Interaction.user_id == u.id,
                Interaction.type == "rating",
                Interaction.rating >= 4.0
            )
            .all()
        )
        if high_ratings:
            ground_truth[u.id] = [r.content_id for r in high_ratings]
    recs_dict = {}
    for user_id in ground_truth:
        recs = orchestrator.get_recommendations(user_id, limit=5, use_cache=False)
        recs_dict[user_id] = [r["item"] for r in recs]


    metrics = evaluator.evaluate_all(recs_dict, ground_truth, k=5)
    
    print("\n--- Evaluation Metrics @ K=5 ---")
    print(f"Precision@5: {metrics['precision@k']}")
    print(f"Recall@5:    {metrics['recall@k']}")
    print(f"NDCG@5:      {metrics['ndcg@k']}")
    print("--------------------------------\n")

    # save report snippet
    report_path = os.path.join(project_root, "evaluation_report.md")
    with open(report_path, "w") as f:
        f.write("# Recommendation Engine Evaluation Report\n\n")
        f.write("This report presents the performance metrics of the hybrid recommendation engine.\n\n")
        f.write("## Performance Summary\n\n")
        f.write("| Metric | Score |\n")
        f.write("| --- | --- |\n")
        f.write(f"| **Precision@5** | {metrics['precision@k']} |\n")
        f.write(f"| **Recall@5** | {metrics['recall@k']} |\n")
        f.write(f"| **NDCG@5** | {metrics['ndcg@k']} |\n\n")
        f.write("## Methodology\n")
        f.write("- **Ground Truth**: Content items rated >= 4.0 by users in the database.\n")
        f.write("- **Evaluation Size**: Evaluated across all users who have sufficient ratings data.\n")
        f.write("- **Recommendation Limit**: Top-5 candidates computed using candidate generators (collaborative + content) and sorted by the RecommendationScorer using popularity, recency, and skill-relevance weights.\n")

    print(f"Report written to: {report_path}")
    db.close()

if __name__ == "__main__":
    run_evaluation()