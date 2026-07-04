from sample_data import (
    item_popularity,
    item_recency,
    item_relevance
)


class RecommendationScorer:
    def __init__(self):
        self.scorers = {}


    def add_scorer(
            self,
            name,
            function,
            weight):

        self.scorers[name] = {
            "function": function,
            "weight": weight
        }


    def calculate_score(
            self,
            user_id,
            item_id,
            context=None):

        total_score = 0
        total_weight = 0

        explanation = []

        for name, scorer in self.scorers.items():
            score = scorer["function"](item_id)
            total_score += (
                score *
                scorer["weight"]
            )

            total_weight += scorer["weight"]
            explanation.append(
                f"{name}:{round(score,2)}"
            )

        if total_weight == 0:
            final_score = 0

        else:
            final_score = (
                total_score /
                total_weight
            )

        return {
            "score": round(final_score, 4),
            "explanation": explanation
        }


    def rank_candidates(
            self,
            user_id,
            candidates,
            limit=10):

        ranked = []

        for item in candidates:
            result = self.calculate_score(
                user_id,
                item
            )

            ranked.append({
                "item": item,
                "score": result["score"],
                "explanation":
                    result["explanation"]
            })

        ranked.sort(
            key=lambda x: x["score"],
            reverse=True
        )
        return ranked[:limit]