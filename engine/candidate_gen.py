from similarity import SimilarityCalculator
from sample_data import (
    user_vectors,
    user_history,
    item_tags,
    item_popularity,
    all_items
)


class CandidateGenerator:

    def __init__(self):

        self.similarity = SimilarityCalculator()


    def collaborative_candidates(
            self,
            user_id,
            limit=20):

        if user_id not in user_history:
            return self.popularity_candidates()

        similarities = {}

        target_vector = user_vectors[user_id]

        for user in user_vectors:

            if user == user_id:
                continue

            score = self.similarity.cosine_similarity(
                target_vector,
                user_vectors[user]
            )

            similarities[user] = score

        similar_users = sorted(
            similarities,
            key=similarities.get,
            reverse=True
        )

        candidates = set()

        for user in similar_users:

            for item in user_history[user]:

                if item not in user_history[user_id]:
                    candidates.add(item)

        return list(candidates)[:limit]


    def content_based_candidates(
            self,
            user_id,
            limit=20):

        if user_id not in user_history:
            return self.popularity_candidates()

        user_items = user_history[user_id]

        candidates = set()

        for watched_item in user_items:

            watched_tags = item_tags[watched_item]

            for item in all_items:

                if item in user_items:
                    continue

                similarity = self.similarity.jaccard_similarity(
                    watched_tags,
                    item_tags[item]
                )

                if similarity > 0:
                    candidates.add(item)

        return list(candidates)[:limit]


    def popularity_candidates(
            self,
            limit=20):

        popular = sorted(
            item_popularity,
            key=item_popularity.get,
            reverse=True
        )

        return popular[:limit]


    def hybrid_candidates(
            self,
            user_id,
            limit=20):

        collaborative = self.collaborative_candidates(
            user_id
        )

        content = self.content_based_candidates(
            user_id
        )

        popular = self.popularity_candidates()

        combined = (
            collaborative +
            content +
            popular
        )

        unique = []

        for item in combined:
            if item not in unique:
                unique.append(item)

        return unique[:limit]