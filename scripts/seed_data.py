import sys
import os
from datetime import datetime

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from data.database import (
    engine,
    SessionLocal,
    Base
)
from data.models import User, Content, Skill, UserSkill, ContentSkill, Interaction

# reset database
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# seed teh skills
skills = [
    Skill(id=1, name="python"),
    Skill(id=2, name="sql"),
    Skill(id=3, name="ml"),
    Skill(id=4, name="systems"),
    Skill(id=5, name="math"),
    Skill(id=6, name="docker"),
    Skill(id=7, name="git")
]
db.add_all(skills)
db.commit()

# seed users
users = [
    User(id=1, name="Alice", interests="python,ml"),
    User(id=2, name="Bob", interests="ml,math"),
    User(id=3, name="Charlie", interests="sql,python"),
    User(id=4, name="David", interests="systems,docker"),
    User(id=5, name="Eve", interests="python,sql"),
    User(id=6, name="Frank", interests="docker,git"),
    User(id=7, name="Grace", interests="math,ml"),
    User(id=8, name="Heidi", interests="python,git"),
    User(id=9, name="Ivan", interests="sql,systems"),
    User(id=10, name="Judy", interests="ml,python")
]
db.add_all(users)
db.commit()

# seed content(following part is generated for accuracy in repeated code, redundant typos n all)
content = [
    Content(id=1, title="Python Basics", category="Programming", difficulty="Beginner", popularity=95),
    Content(id=2, title="SQL Mastery", category="Database", difficulty="Intermediate", popularity=88),
    Content(id=3, title="Machine Learning", category="AI", difficulty="Advanced", popularity=97),
    Content(id=4, title="Statistics", category="Math", difficulty="Intermediate", popularity=75),
    Content(id=5, title="Deep Learning", category="AI", difficulty="Advanced", popularity=92),
    Content(id=6, title="Docker for Devs", category="Systems", difficulty="Beginner", popularity=80),
    Content(id=7, title="Git Essentials", category="Systems", difficulty="Beginner", popularity=85),
    Content(id=8, title="Data Pipelines", category="Programming", difficulty="Intermediate", popularity=89),
    Content(id=9, title="Advanced Python", category="Programming", difficulty="Advanced", popularity=91),
    Content(id=10, title="PostgreSQL Advanced", category="Database", difficulty="Advanced", popularity=83),
    Content(id=11, title="Neural Networks", category="AI", difficulty="Advanced", popularity=90),
    Content(id=12, title="Cloud Computing", category="Systems", difficulty="Intermediate", popularity=86),
    Content(id=13, title="Kubernetes Intro", category="Systems", difficulty="Advanced", popularity=84),
    Content(id=14, title="Linear Algebra", category="Math", difficulty="Intermediate", popularity=70),
    Content(id=15, title="Probability", category="Math", difficulty="Beginner", popularity=72),
    Content(id=16, title="PyTorch Guide", category="AI", difficulty="Intermediate", popularity=88),
    Content(id=17, title="Rust for Beginners", category="Systems", difficulty="Beginner", popularity=78),
    Content(id=18, title="Linux Command Line", category="Systems", difficulty="Beginner", popularity=82),
    Content(id=19, title="NoSQL Databases", category="Database", difficulty="Intermediate", popularity=76),
    Content(id=20, title="Flask Web Apps", category="Programming", difficulty="Intermediate", popularity=85)
]
db.add_all(content)
db.commit()

# seed user_skills (proficiencies)
user_skills = [
    UserSkill(user_id=1, skill_id=1, proficiency=1.0),
    UserSkill(user_id=1, skill_id=3, proficiency=0.8),
    UserSkill(user_id=2, skill_id=3, proficiency=0.9),
    UserSkill(user_id=2, skill_id=5, proficiency=0.7),
    UserSkill(user_id=3, skill_id=2, proficiency=0.9),
    UserSkill(user_id=3, skill_id=1, proficiency=0.6),
    UserSkill(user_id=4, skill_id=4, proficiency=0.8),
    UserSkill(user_id=4, skill_id=6, proficiency=0.7),
    UserSkill(user_id=5, skill_id=1, proficiency=0.8),
    UserSkill(user_id=5, skill_id=2, proficiency=0.5),
    UserSkill(user_id=6, skill_id=6, proficiency=0.9),
    UserSkill(user_id=6, skill_id=7, proficiency=0.8),
    UserSkill(user_id=7, skill_id=5, proficiency=0.9),
    UserSkill(user_id=7, skill_id=3, proficiency=0.8),
    UserSkill(user_id=8, skill_id=1, proficiency=0.7),
    UserSkill(user_id=8, skill_id=7, proficiency=0.7),
    UserSkill(user_id=9, skill_id=2, proficiency=0.8),
    UserSkill(user_id=9, skill_id=4, proficiency=0.6),
    UserSkill(user_id=10, skill_id=3, proficiency=0.9),
    UserSkill(user_id=10, skill_id=1, proficiency=0.9)
]
db.add_all(user_skills)
db.commit()

# seed content_skills (skill tags)
content_skills = [
    ContentSkill(content_id=1, skill_id=1), # Python Basics -> python
    ContentSkill(content_id=2, skill_id=2), # SQL Mastery -> sql
    ContentSkill(content_id=3, skill_id=3), # Machine Learning -> ml
    ContentSkill(content_id=3, skill_id=5), # Machine Learning -> math
    ContentSkill(content_id=4, skill_id=5), # Statistics -> math
    ContentSkill(content_id=5, skill_id=3), # Deep Learning -> ml
    ContentSkill(content_id=5, skill_id=5), # Deep Learning -> math
    ContentSkill(content_id=6, skill_id=6), # Docker for Devs -> docker
    ContentSkill(content_id=6, skill_id=4), # Docker for Devs -> systems
    ContentSkill(content_id=7, skill_id=7), # Git Essentials -> git
    ContentSkill(content_id=8, skill_id=1), # Data Pipelines -> python
    ContentSkill(content_id=8, skill_id=2), # Data Pipelines -> sql
    ContentSkill(content_id=9, skill_id=1), # Advanced Python -> python
    ContentSkill(content_id=10, skill_id=2),# PostgreSQL Advanced -> sql
    ContentSkill(content_id=11, skill_id=3),# Neural Networks -> ml
    ContentSkill(content_id=12, skill_id=4),# Cloud Computing -> systems
    ContentSkill(content_id=13, skill_id=6),# Kubernetes Intro -> docker
    ContentSkill(content_id=13, skill_id=4),# Kubernetes Intro -> systems
    ContentSkill(content_id=14, skill_id=5),# Linear Algebra -> math
    ContentSkill(content_id=15, skill_id=5),# Probability -> math
    ContentSkill(content_id=16, skill_id=1),# PyTorch Guide -> python
    ContentSkill(content_id=16, skill_id=3),# PyTorch Guide -> ml
    ContentSkill(content_id=17, skill_id=4),# Rust for Beginners -> systems
    ContentSkill(content_id=18, skill_id=4),# Linux Command Line -> systems
    ContentSkill(content_id=19, skill_id=2),# NoSQL Databases -> sql
    ContentSkill(content_id=20, skill_id=1),# Flask Web Apps -> python
    ContentSkill(content_id=20, skill_id=4) # Flask Web Apps -> systems
]
db.add_all(content_skills)
db.commit()

# seed interactions (ratings)
interactions = [
    Interaction(user_id=1, content_id=1, type="rating", rating=5.0),
    Interaction(user_id=1, content_id=3, type="rating", rating=4.5),
    Interaction(user_id=1, content_id=5, type="rating", rating=4.8),
    
    Interaction(user_id=2, content_id=3, type="rating", rating=4.7),
    Interaction(user_id=2, content_id=4, type="rating", rating=4.0),
    Interaction(user_id=2, content_id=5, type="rating", rating=4.5),
    
    Interaction(user_id=3, content_id=2, type="rating", rating=4.8),
    Interaction(user_id=3, content_id=8, type="rating", rating=4.2),
    Interaction(user_id=3, content_id=1, type="rating", rating=3.5),
    
    Interaction(user_id=4, content_id=6, type="rating", rating=4.5),
    Interaction(user_id=4, content_id=12, type="rating", rating=4.0),
    Interaction(user_id=4, content_id=13, type="rating", rating=4.2),

    Interaction(user_id=5, content_id=1, type="rating", rating=4.0),
    Interaction(user_id=5, content_id=2, type="rating", rating=4.5),
    Interaction(user_id=5, content_id=8, type="rating", rating=4.4),

    Interaction(user_id=6, content_id=6, type="rating", rating=4.8),
    Interaction(user_id=6, content_id=7, type="rating", rating=4.6),

    Interaction(user_id=7, content_id=4, type="rating", rating=4.2),
    Interaction(user_id=7, content_id=11, type="rating", rating=4.5),
    Interaction(user_id=7, content_id=14, type="rating", rating=4.8),

    Interaction(user_id=8, content_id=1, type="rating", rating=4.0),
    Interaction(user_id=8, content_id=7, type="rating", rating=4.2),

    Interaction(user_id=9, content_id=2, type="rating", rating=4.3),
    Interaction(user_id=9, content_id=12, type="rating", rating=4.1),

    Interaction(user_id=10, content_id=3, type="rating", rating=4.9),
    Interaction(user_id=10, content_id=16, type="rating", rating=4.7)
]
db.add_all(interactions)
db.commit()

print("Database seeded successfully.")