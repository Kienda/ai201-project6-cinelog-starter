# PR Response Doc — CineLog Watchlist Feature

## AI Usage

<!-- Fill in at the end — explain specifically how AI supported orientation,
review interpretation, implementation, testing, and argument stress-testing. -->

## Comment 1 — Rename

**What I did:**

I renamed `save_to_watchlist()` to `add_to_watchlist()` in
`services/watchlist_service.py` so it follows CineLog's `verb_to_noun` service
naming convention. I also updated the import and call in
`routes/watchlist/watchlist.py`.

**How I verified:**

I used a project-wide search for `save_to_watchlist` before the change to find
the definition and its one call site. After renaming both, I repeated the search
to confirm no references to the old name remained, then ran the full test suite.

## Comment 2 — Deduplication

**What I did:**

I followed `add_to_collection()`'s existing pattern: query `WatchlistEntry` by
both `user_id` and `film_id` before inserting, and raise a new
`AlreadyInWatchlistError` when that pair already exists. The watchlist route
catches that domain error and returns HTTP 409, matching the collection API's
conflict behavior.

**How I verified:**

I added the same film for the same user twice in an isolated in-memory database.
The second call raised `AlreadyInWatchlistError`, and the database still
contained exactly one matching entry. I also ran the full test suite to check
for regressions.

## Comment 3 — Missing test

**What I did:**

I created `tests/test_watchlist.py` and added
`test_add_to_watchlist_nonexistent_film_raises()`. It confirms that the service
raises `FilmNotFoundError` before attempting to create a database entry when the
film does not exist.

**How I verified:**

I modeled the fixtures, application-context boundary, fake ID, and
`pytest.raises` assertion on
`test_add_to_collection_nonexistent_film_raises()` in
`tests/test_collection.py`. I ran the watchlist test file by itself and then the
full suite.

## Comment 4 — Default visibility

**My position:**

**Reasoning:**

**Tradeoff acknowledged:**

## Comment 5 — Sort order

**My position:**

**Reasoning:**

**Engagement with reviewer's point:**

## Comment 6 — Rebase

**What conflicted:**

**How I resolved it:**

**How I verified no conflict remains:**

## PR Description

<!-- Fill in at the end: a 2–3 sentence feature overview, design decisions,
and end-to-end manual testing steps. -->
