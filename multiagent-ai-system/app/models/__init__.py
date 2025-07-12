# app/models/__init__.py
#
# Import every ORM class so SQLAlchemy sees them
# as soon as you import `app.models`.

from .user import User
from .conversation import Conversation
from .message import Message


