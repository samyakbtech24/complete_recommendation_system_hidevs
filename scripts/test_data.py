import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from data.database import (
    SessionLocal
)

from data.repositories import (
    UserRepository,
    ContentRepository,
    InteractionRepository
)

db = SessionLocal()

users = UserRepository(db)
content = ContentRepository(db)

print(
    users.get_all_users()
)

print(
    content.get_all_content()
)