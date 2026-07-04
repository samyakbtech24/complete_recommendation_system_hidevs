import math


class RecommendationEvaluator:
    def precision_at_k(
            self,
            recommendations,
            relevant_items,
            k):

        recommendations = recommendations[:k]

        if len(recommendations) == 0:
            return 0
        relevant = sum(
            1
            for item in recommendations
            if item in relevant_items
        )

        return round(
            relevant / len(recommendations),
            4
        )


    def recall_at_k(
            self,
            recommendations,
            relevant_items,
            k):

        recommendations = recommendations[:k]

        if len(relevant_items) == 0:
            return 0

        relevant = sum(
            1
            for item in recommendations
            if item in relevant_items
        )

        return round(
            relevant / len(relevant_items),
            4
        )


    def ndcg_at_k(
            self,
            recommendations,
            relevant_items,
            k):

        recommendations = recommendations[:k]

        dcg = 0

        for i, item in enumerate(recommendations):

            if item in relevant_items:
                dcg += 1 / math.log2(i + 2)

        ideal_dcg = 0

        for i in range(
                min(k, len(relevant_items))):

            ideal_dcg += (
                1 / math.log2(i + 2)
            )

        if ideal_dcg == 0:
            return 0

        return round(
            dcg / ideal_dcg,
            4
        )


    def evaluate_all(
            self,
            recommendations_dict,
            ground_truth_dict,
            k):

        precision_scores = []
        recall_scores = []
        ndcg_scores = []

        for user in recommendations_dict:

            if user not in ground_truth_dict:
                continue

            recommendations = (
                recommendations_dict[user]
            )

            truth = (
                ground_truth_dict[user]
            )

            precision_scores.append(
                self.precision_at_k(
                    recommendations,
                    truth,
                    k
                )
            )

            recall_scores.append(
                self.recall_at_k(
                    recommendations,
                    truth,
                    k
                )
            )

            ndcg_scores.append(
                self.ndcg_at_k(
                    recommendations,
                    truth,
                    k
                )
            )

        return {
            "precision@k":
                round(
                    sum(precision_scores)
                    /
                    len(precision_scores),
                    4
                ),

            "recall@k":
                round(
                    sum(recall_scores)
                    /
                    len(recall_scores),
                    4
                ),

            "ndcg@k":
                round(
                    sum(ndcg_scores)
                    /
                    len(ndcg_scores),
                    4
                )
        }