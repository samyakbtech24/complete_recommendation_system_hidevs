import unittest
import sys
import os

# ensure project root is in path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from engine.similarity import SimilarityCalculator
from engine.scorer import RecommendationScorer
from engine.evaluator import RecommendationEvaluator
from data.database import SessionLocal
from engine.orchestrator import RecommendationOrchestrator

class TestEngine(unittest.TestCase):
    def test_similarity_math(self):
        calc = SimilarityCalculator()
        
        # cosine similarity
        vec1 = [1.0, 0.0, 0.5]
        vec2 = [1.0, 0.0, 0.5]
        self.assertEqual(calc.cosine_similarity(vec1, vec2), 1.0)
        
        vec3 = [0.0, 1.0, 0.0]
        self.assertEqual(calc.cosine_similarity(vec1, vec3), 0.0)
        
        # jaccard similarity
        set1 = {"python", "ml"}
        set2 = {"python", "sql"}
        self.assertEqual(calc.jaccard_similarity(set1, set2), 0.3333)
        self.assertEqual(calc.jaccard_similarity(set(), set()), 0.0)

        # pearson correlation
        r1 = {"item1": 5.0, "item2": 3.0}
        r2 = {"item1": 4.0, "item2": 2.0}
        self.assertEqual(calc.pearson_correlation(r1, r2), 1.0)
        self.assertEqual(calc.pearson_correlation({"item3": 5}, {"item4": 2}), 0.0)

    def test_scorer_logic(self):
        # testing for the  scorer
        scorer = RecommendationScorer()
        
        def mock_pop(item_id):
            return 0.8 if item_id == 1 else 0.5
            
        scorer.add_scorer("pop", mock_pop, 1.0)
        
        recs = scorer.rank_candidates(user_id=1, candidates=[1, 2], limit=2)
        self.assertEqual(len(recs), 2)
        self.assertEqual(recs[0]["item"], 1)
        self.assertEqual(recs[0]["score"], 0.8)

    def test_evaluator_metrics(self):
        evaluator = RecommendationEvaluator()
        recs = [1, 2, 3]
        truth = [2, 3, 4]
        
        precision = evaluator.precision_at_k(recs, truth, k=2)
        self.assertEqual(precision, 0.5)
        
        recall = evaluator.recall_at_k(recs, truth, k=3)
        self.assertEqual(recall, 0.6667)
        
        ndcg = evaluator.ndcg_at_k(recs, truth, k=3)
        self.assertTrue(ndcg > 0.0)

    def test_orchestrator_integration(self):
        db = SessionLocal()
        orchestrator = RecommendationOrchestrator(db)
        
        recs = orchestrator.get_recommendations(user_id=1, limit=3)
        self.assertTrue(len(recs) > 0)
        self.assertIn("score", recs[0])
        self.assertIn("explanation", recs[0])
        
        orchestrator.get_recommendations(user_id=1, limit=3)
        self.assertIn(1, orchestrator.cache)
        orchestrator.record_feedback(user_id=1, content_id=2, interaction_type="click")
        self.assertNotIn(1, orchestrator.cache)
        
        db.close()

if __name__ == "__main__":
    unittest.main()
