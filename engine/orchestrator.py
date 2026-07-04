import sys
import os
import types
from data.repositories import (
    UserRepository,
    ContentRepository,
    InteractionRepository,
    SkillRepository
)
from data.models import Interaction, Skill

class RecommendationOrchestrator:

    def __init__(self, db):
        self.db = db
        self.user_repo = UserRepository(db)
        self.content_repo = ContentRepository(db)
        self.interaction_repo = InteractionRepository(db)
        self.skill_repo = SkillRepository(db)
        
        
        self.cache = {}
 
        self.load_data()
        engine_path = os.path.dirname(os.path.abspath(__file__))
        if engine_path not in sys.path:
            sys.path.append(engine_path)
            
        from candidate_gen import CandidateGenerator
        from scorer import RecommendationScorer
        
        self.candidate_gen = CandidateGenerator()
        self.scorer = RecommendationScorer()
        
        self.setup_scorers()

    def load_data(self):
        users = self.user_repo.get_all_users()
        contents = self.content_repo.get_all_content()
        skills = self.db.query(Skill).all()
        
        # sorting skills for vector indices code snippet
        skills = sorted(skills, key=lambda s: s.id)
        skill_ids = [s.id for s in skills]
        skill_names = {s.id: s.name for s in skills}
        
        # user vctors
        user_vectors = {}
        for u in users:
            u_skills = self.skill_repo.get_user_skills(u.id)
            prof_dict = {us.skill_id: us.proficiency for us in u_skills}
            user_vectors[u.id] = [prof_dict.get(sid, 0.0) for sid in skill_ids]
            
        # user_history
        user_history = {}
        for u in users:
            history = self.interaction_repo.get_user_history(u.id)
            user_history[u.id] = {hist.content_id for hist in history}
            
        # item_tags
        item_tags = {}
        for c in contents:
            c_skills = self.skill_repo.get_content_skills(c.id)
            tags = {skill_names.get(cs.skill_id) for cs in c_skills if skill_names.get(cs.skill_id)}
            if c.category:
                tags.add(c.category)
            item_tags[c.id] = tags
            
        # item_popularity
        item_popularity = {c.id: c.popularity for c in contents}
        
        
        all_items = [c.id for c in contents]
        
        
        max_id = max(all_items) if all_items else 1
        item_recency = {c.id: round(c.id / max_id, 4) for c in contents}
        
        
        item_relevance = {c.id: 0.5 for c in contents}
        
        # write sample_data.py to disk
        engine_path = os.path.dirname(os.path.abspath(__file__))
        sample_data_file = os.path.join(engine_path, "sample_data.py")
        
        user_history_list = {k: list(v) for k, v in user_history.items()}
        with open(sample_data_file, "w") as f:
            f.write("# Auto-generated data from DB\n")
            f.write(f"user_vectors = {repr(user_vectors)}\n")
            f.write(f"user_history = {repr(user_history_list)}\n")
            f.write("item_tags = {\n")
            for k, v in item_tags.items():
                f.write(f"    {k}: {repr(v)},\n")
            f.write("}\n")
            f.write(f"item_popularity = {repr(item_popularity)}\n")
            f.write(f"all_items = {repr(all_items)}\n")
            f.write(f"item_recency = {repr(item_recency)}\n")
            f.write(f"item_relevance = {repr(item_relevance)}\n")

        # Inject into sys.modules code snippet
        if 'sample_data' not in sys.modules:
            sample_data_mod = types.ModuleType('sample_data')
            sys.modules['sample_data'] = sample_data_mod
        else:
            sample_data_mod = sys.modules['sample_data']
            
        sample_data_mod.user_vectors = user_vectors
        sample_data_mod.user_history = {k: set(v) for k, v in user_history.items()}
        sample_data_mod.item_tags = item_tags
        sample_data_mod.item_popularity = item_popularity
        sample_data_mod.all_items = all_items
        sample_data_mod.item_recency = item_recency
        sample_data_mod.item_relevance = item_relevance
        
        self.sample_data_mod = sample_data_mod

    def setup_scorers(self):
        # popularity scorer
        def pop_score(item_id):
            pop = self.sample_data_mod.item_popularity.get(item_id, 0)
            return pop / 100.0
            
        # recency scorer
        def rec_score(item_id):
            return self.sample_data_mod.item_recency.get(item_id, 0.0)
            
        # relevance scorer
        def rel_score(item_id):
            user_id = getattr(self.sample_data_mod, 'active_user_id', 1)
            user_skills = self.skill_repo.get_user_skills(user_id)
            user_skill_names = set()
            for us in user_skills:
                skill = self.db.query(Skill).filter(Skill.id == us.skill_id).first()
                if skill:
                    user_skill_names.add(skill.name)
            
            item_tags = self.sample_data_mod.item_tags.get(item_id, set())
            if not user_skill_names or not item_tags:
                return 0.0
                
            intersection = len(user_skill_names.intersection(item_tags))
            union = len(user_skill_names.union(item_tags))
            return intersection / union if union > 0 else 0.0

        
        self.scorer.add_scorer("popularity", pop_score, 0.2)
        self.scorer.add_scorer("recency", rec_score, 0.3)
        self.scorer.add_scorer("relevance", rel_score, 0.5)

    def get_recommendations(self, user_id, limit=5, use_cache=True):
        if use_cache and user_id in self.cache:
            return self.cache[user_id]
            
        self.sample_data_mod.active_user_id = user_id
        
        
        candidates = self.candidate_gen.hybrid_candidates(user_id, limit=20)
        
        ranked = self.scorer.rank_candidates(user_id, candidates, limit=limit)
        
        self.cache[user_id] = ranked
        return ranked

    def record_feedback(self, user_id, content_id, interaction_type, rating=None):
        # write the intraction
        interaction = Interaction(
            user_id=user_id,
            content_id=content_id,
            type=interaction_type,
            rating=rating
        )
        self.interaction_repo.record_interaction(interaction)
        
    
        if user_id in self.cache:
            del self.cache[user_id]
            
        self.load_data()
