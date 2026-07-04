from data.models import *


class UserRepository:

    def __init__(self, db):
        self.db = db

    def get_user(self, user_id):
        return (
            self.db.query(User)
            .filter(
                User.id == user_id
            )
            .first()
        )

    def get_all_users(self):
        return (
            self.db.query(User)
            .all()
        )


class ContentRepository:

    def __init__(self, db):
        self.db = db

    def get_content(self, content_id):
        return (
            self.db.query(Content)
            .filter(
                Content.id == content_id
            )
            .first()
        )

    def get_all_content(self):
        return (
            self.db.query(Content)
            .all()
        )


class InteractionRepository:

    def __init__(self, db):
        self.db = db

    def get_user_history(
            self,
            user_id):

        return (
            self.db.query(
                Interaction
            )
            .filter(
                Interaction.user_id
                == user_id
            )
            .all()
        )

    def record_interaction(
            self,
            interaction):

        self.db.add(
            interaction
        )

        self.db.commit()


class SkillRepository:

    def __init__(self, db):
        self.db = db

    def get_user_skills(
            self,
            user_id):

        return (
            self.db.query(
                UserSkill
            )
            .filter(
                UserSkill.user_id
                == user_id
            )
            .all()
        )

    def get_content_skills(
            self,
            content_id):

        return (
            self.db.query(
                ContentSkill
            )
            .filter(
                ContentSkill.content_id
                == content_id
            )
            .all()
        )