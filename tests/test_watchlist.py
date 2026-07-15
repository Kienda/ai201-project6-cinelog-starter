"""Tests for the watchlist service."""

from datetime import datetime, timedelta, timezone

import pytest

from app import create_app, db
from models import Film, User, WatchlistEntry
from services.collection_service import FilmNotFoundError
from services.watchlist_service import add_to_watchlist, get_watchlist


@pytest.fixture
def app():
    """Create an isolated test app with an in-memory database."""
    app = create_app(config={
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_user(app):
    """Create a user for watchlist service tests."""
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        db.session.add(user)
        db.session.commit()
        return user.id


def test_add_to_watchlist_nonexistent_film_raises(app, sample_user):
    """Adding a nonexistent film should raise FilmNotFoundError."""
    with app.app_context():
        nonexistent_film_id = "00000000-0000-0000-0000-000000000000"

        with pytest.raises(FilmNotFoundError):
            add_to_watchlist(
                user_id=sample_user,
                film_id=nonexistent_film_id,
            )


def test_get_watchlist_returns_newest_first(app, sample_user):
    """The most recently added watchlist film should appear first."""
    with app.app_context():
        older_film = Film(title="Alien")
        newer_film = Film(title="Arrival")
        db.session.add_all([older_film, newer_film])
        db.session.commit()

        older_entry = WatchlistEntry(
            user_id=sample_user,
            film_id=older_film.id,
            date_added=datetime.now(timezone.utc) - timedelta(days=1),
        )
        newer_entry = WatchlistEntry(
            user_id=sample_user,
            film_id=newer_film.id,
            date_added=datetime.now(timezone.utc),
        )
        db.session.add_all([older_entry, newer_entry])
        db.session.commit()

        watchlist = get_watchlist(sample_user)

        assert [film["title"] for film in watchlist] == ["Arrival", "Alien"]
