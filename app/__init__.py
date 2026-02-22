"""NgakaAssist Flask backend package.

Public exports are kept minimal so the rest of the project can import:
- create_app (app factory)
- db (SQLAlchemy extension)

All implementation lives under app/core, app/api, app/services, app/models.
"""

from app.core.app_factory import create_app  # noqa: F401
from app.core.extensions import db  # noqa: F401
