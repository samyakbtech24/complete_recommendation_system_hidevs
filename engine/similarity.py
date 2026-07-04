import math


class SimilarityCalculator:

    def cosine_similarity(self, vec1, vec2):
        if len(vec1) != len(vec2):
            raise ValueError("Vectors must have same length")

        dot_product = sum(a*b for a, b in zip(vec1, vec2))

        magnitude1 = math.sqrt(sum(a*a for a in vec1))
        magnitude2 = math.sqrt(sum(b*b for b in vec2))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        similarity = dot_product / (magnitude1 * magnitude2)
        return round(similarity, 4)


    def jaccard_similarity(self, set1, set2):
        if not set1 and not set2:
            return 0.0

        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        if union == 0:
            return 0.0
        similarity = intersection / union
        return round(similarity, 4)


    def pearson_correlation(self, ratings1, ratings2):

        common_items = set(ratings1.keys()).intersection(
            set(ratings2.keys())
        )
        if len(common_items) == 0:
            return 0.0

        values1 = [ratings1[item] for item in common_items]
        values2 = [ratings2[item] for item in common_items]

        mean1 = sum(values1) / len(values1)
        mean2 = sum(values2) / len(values2)

        numerator = sum(
            (a - mean1) * (b - mean2)
            for a, b in zip(values1, values2)
        )

        denominator1 = math.sqrt(
            sum((a - mean1) ** 2 for a in values1)
        )

        denominator2 = math.sqrt(
            sum((b - mean2) ** 2 for b in values2)
        )

        denominator = denominator1 * denominator2

        if denominator == 0:
            return 0.0

        correlation = numerator / denominator
        return round(correlation, 4)