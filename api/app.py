import time
import uuid
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from flask import Flask, request, jsonify, render_template
from data.database import SessionLocal
from data.models import User
from engine.orchestrator import RecommendationOrchestrator

app = Flask(__name__, template_folder="templates")

db_session = SessionLocal()
orchestrator = RecommendationOrchestrator(db_session)

API_KEY = "capstone-key"

api_metrics = {
    "total_requests": 0,
    "total_latency_ms": 0.0,
    "cache_hits": 0,
    "cache_misses": 0
}

@app.before_request
def start_timer():
    request.start_time = time.time()
    # request id tracing
    request.request_id = str(uuid.uuid4())
    api_metrics["total_requests"] += 1

@app.after_request
def add_headers(response):
    if hasattr(request, "start_time"):
        latency = (time.time() - request.start_time) * 1000.0
        api_metrics["total_latency_ms"] += latency
    if hasattr(request, "request_id"):
        response.headers["X-Request-ID"] = request.request_id
    return response

def verify_api_key():
    key = request.headers.get("X-API-Key") or request.args.get("api_key")
    return key == API_KEY

@app.route("/")
def index():
    users = db_session.query(User).all()
    user_list = [{"id": u.id, "name": u.name} for u in users]
    return render_template("index.html", users=user_list)

@app.route("/recommend/<int:user_id>", methods=["GET"])
def recommend(user_id):
    if not verify_api_key():
        return jsonify({"error": "Unauthorized: Invalid API Key"}), 401

    user = db_session.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({"error": f"User {user_id} not found"}), 404

    is_cached = user_id in orchestrator.cache
    if is_cached:
        api_metrics["cache_hits"] += 1
    else:
        api_metrics["cache_misses"] += 1

    try:
        limit = request.args.get("limit", default=5, type=int)
        recs = orchestrator.get_recommendations(user_id, limit=limit)
        
        results = []
        for r in recs:
            content_id = r["item"]
            item_details = orchestrator.content_repo.get_content(content_id)
            results.append({
                "content_id": content_id,
                "title": item_details.title if item_details else f"Content {content_id}",
                "category": item_details.category if item_details else "General",
                "score": r["score"],
                "explanation": ", ".join(r["explanation"])
            })

        return jsonify({
            "user_id": user_id,
            "user_name": user.name,
            "recommendations": results,
            "cached": is_cached
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/feedback", methods=["POST"])
def feedback():
    if not verify_api_key():
        return jsonify({"error": "Unauthorized: Invalid API Key"}), 401

    data = request.get_json()
    if not data or "user_id" not in data or "content_id" not in data or "type" not in data:
        return jsonify({"error": "Bad request: missing parameters"}), 400

    user_id = data["user_id"]
    content_id = data["content_id"]
    feedback_type = data["type"]
    rating = data.get("rating")

    # check if user exists
    user = db_session.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({"error": f"User {user_id} not found"}), 404

    try:
        orchestrator.record_feedback(user_id, content_id, feedback_type, rating)
        return jsonify({"message": "Feedback recorded successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/health", methods=["GET"])
def health():
    try:
        db_session.query(User).first()
        db_ok = True
    except Exception:
        db_ok = False

    return jsonify({
        "status": "healthy" if db_ok else "unhealthy",
        "database": "connected" if db_ok else "disconnected",
        "timestamp": time.time()
    })

@app.route("/metrics", methods=["GET"])
def get_metrics():
    avg_latency = 0.0
    if api_metrics["total_requests"] > 0:
        avg_latency = api_metrics["total_latency_ms"] / api_metrics["total_requests"]

    total_queries = api_metrics["cache_hits"] + api_metrics["cache_misses"]
    hit_rate = 0.0
    if total_queries > 0:
        hit_rate = api_metrics["cache_hits"] / total_queries

    return jsonify({
        "total_requests": api_metrics["total_requests"],
        "average_latency_ms": round(avg_latency, 2),
        "cache_hits": api_metrics["cache_hits"],
        "cache_misses": api_metrics["cache_misses"],
        "cache_hit_rate": round(hit_rate, 4)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
