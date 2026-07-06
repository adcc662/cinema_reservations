"""remove surrogate pk from junction tables

Replace surrogate UUID `id` primary keys on the `movie_genres` and
`reservation_seats` junction tables with composite primary keys built from
their foreign-key columns. This brings both tables into 3NF compliance and
removes the redundant unique constraints that protected the natural key.

Revision ID: 20260427_0001
Revises:
Create Date: 2026-04-27

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260427_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


# ---------------------------------------------------------------------------
# movie_genres
# ---------------------------------------------------------------------------
# Original shape (pre-migration):
#   id            UUID  PRIMARY KEY
#   movie_id      UUID  FK -> movies.id
#   genre_id      UUID  FK -> genres.id
#   UNIQUE (movie_id, genre_id)
#
# Target shape (post-migration):
#   movie_id      UUID  PK + FK -> movies.id
#   genre_id      UUID  PK + FK -> genres.id
#   PRIMARY KEY (movie_id, genre_id)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# reservation_seats
# ---------------------------------------------------------------------------
# Original shape (pre-migration):
#   id              UUID  PRIMARY KEY
#   reservation_id  UUID  FK -> reservations.id
#   seat_id         UUID  FK -> seats.id
#   created_at      TIMESTAMP
#   UNIQUE (reservation_id, seat_id)
#
# Target shape (post-migration):
#   reservation_id  UUID  PK + FK -> reservations.id
#   seat_id         UUID  PK + FK -> seats.id
#   created_at      TIMESTAMP
#   PRIMARY KEY (reservation_id, seat_id)
# ---------------------------------------------------------------------------


def upgrade() -> None:
    """Drop surrogate `id` PK and promote the composite key on both tables."""

    # ------------------------------------------------------------------
    # movie_genres
    # ------------------------------------------------------------------
    # Drop the legacy unique constraint on (movie_id, genre_id) if it exists.
    # We use a raw SQL guard so the migration is idempotent regardless of how
    # the constraint was originally named.
    op.execute(
        """
        DO $$
        DECLARE
            cname text;
        BEGIN
            SELECT conname
              INTO cname
              FROM pg_constraint
             WHERE conrelid = 'movie_genres'::regclass
               AND contype  = 'u'
               AND pg_get_constraintdef(oid) ILIKE '%(movie_id, genre_id)%';
            IF cname IS NOT NULL THEN
                EXECUTE format('ALTER TABLE movie_genres DROP CONSTRAINT %I', cname);
            END IF;
        END$$;
        """
    )

    # Drop the existing primary key on `id`.
    op.drop_constraint("movie_genres_pkey", "movie_genres", type_="primary")

    # Drop the surrogate `id` column.
    op.drop_column("movie_genres", "id")

    # Create the composite primary key on (movie_id, genre_id).
    op.create_primary_key(
        "movie_genres_pkey",
        "movie_genres",
        ["movie_id", "genre_id"],
    )

    # ------------------------------------------------------------------
    # reservation_seats
    # ------------------------------------------------------------------
    op.execute(
        """
        DO $$
        DECLARE
            cname text;
        BEGIN
            SELECT conname
              INTO cname
              FROM pg_constraint
             WHERE conrelid = 'reservation_seats'::regclass
               AND contype  = 'u'
               AND pg_get_constraintdef(oid) ILIKE '%(reservation_id, seat_id)%';
            IF cname IS NOT NULL THEN
                EXECUTE format('ALTER TABLE reservation_seats DROP CONSTRAINT %I', cname);
            END IF;
        END$$;
        """
    )

    op.drop_constraint(
        "reservation_seats_pkey", "reservation_seats", type_="primary"
    )

    op.drop_column("reservation_seats", "id")

    op.create_primary_key(
        "reservation_seats_pkey",
        "reservation_seats",
        ["reservation_id", "seat_id"],
    )


def downgrade() -> None:
    """Restore the surrogate `id` PK and the unique natural-key constraint."""

    # ------------------------------------------------------------------
    # reservation_seats
    # ------------------------------------------------------------------
    op.drop_constraint(
        "reservation_seats_pkey", "reservation_seats", type_="primary"
    )

    op.add_column(
        "reservation_seats",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
    )
    # Drop the server_default once the column is populated so that the column
    # definition matches the original model (default generated in the app).
    op.alter_column("reservation_seats", "id", server_default=None)

    op.create_primary_key(
        "reservation_seats_pkey", "reservation_seats", ["id"]
    )

    op.create_unique_constraint(
        "uq_reservation_seats_reservation_id_seat_id",
        "reservation_seats",
        ["reservation_id", "seat_id"],
    )

    # ------------------------------------------------------------------
    # movie_genres
    # ------------------------------------------------------------------
    op.drop_constraint("movie_genres_pkey", "movie_genres", type_="primary")

    op.add_column(
        "movie_genres",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
    )
    op.alter_column("movie_genres", "id", server_default=None)

    op.create_primary_key("movie_genres_pkey", "movie_genres", ["id"])

    op.create_unique_constraint(
        "uq_movie_genres_movie_id_genre_id",
        "movie_genres",
        ["movie_id", "genre_id"],
    )
