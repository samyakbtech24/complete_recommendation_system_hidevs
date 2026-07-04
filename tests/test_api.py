import unittest
import sys
import os
import json

# ensuring project root is in path:
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from api.app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_dashboard_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Recommendation Lab", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")
        self.assertIn("database", data)

    def test_unauthorized_access(self):
        # test unathorized access
        response = self.client.get("/recommend/1")
        self.assertEqual(response.status_code, 401)
        
        response = self.client.post("/feedback", json={})
        self.assertEqual(response.status_code, 401)

    def test_recommend_success(self):
        response = self.client.get("/recommend/1?api_key=capstone-key&limit=3")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["user_id"], 1)
        self.assertIn("recommendations", data)
        self.assertTrue(len(data["recommendations"]) <= 3)

    def test_recommend_not_found(self):
        response = self.client.get("/recommend/999?api_key=capstone-key")
        self.assertEqual(response.status_code, 404)

    def test_feedback_success(self):
        payload = {
            "user_id": 1,
            "content_id": 4,
            "type": "rating",
            "rating": 4.5
        }
        response = self.client.post("/feedback?api_key=capstone-key", json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("recorded successfully", data["message"])

    def test_metrics_endpoint(self):
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("total_requests", data)
        self.assertIn("cache_hit_rate", data)

if __name__ == "__main__":
    unittest.main()
