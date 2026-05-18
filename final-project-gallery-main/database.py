import sqlite3
import hashlib
import os

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gallery.db")

# CONNECTION------------------------------------------------------
def get_connection():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# DATABASE INITIALIZATION----------------------------------------------
def init_db():

    with get_connection() as conn:

        # USERS---------------------------------------------------------
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        # ALBUMS--------------------------------------------------------
        conn.execute("""
            CREATE TABLE IF NOT EXISTS albums (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # PHOTOS--------------------------------------------------------
        conn.execute("""
            CREATE TABLE IF NOT EXISTS photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                filename TEXT NOT NULL,
                filepath TEXT NOT NULL UNIQUE,

                thumbnail_path TEXT,

                title TEXT,

                album_id INTEGER,

                is_favorite INTEGER DEFAULT 0,

                file_size INTEGER DEFAULT 0,

                image_width INTEGER DEFAULT 0,
                image_height INTEGER DEFAULT 0,

                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_deleted INTEGER DEFAULT 0,
                deleted_at TIMESTAMP,
                user_id INTEGER,
                FOREIGN KEY (album_id)
                REFERENCES albums(id)
                ON DELETE SET NULL
            )
        """)

        # DEFAULT USER--------------------------------------------------------
        hashed = hashlib.sha256(
            "user1".encode()
        ).hexdigest()

        conn.execute(
            """
            INSERT OR IGNORE INTO users
            (username, password)
            VALUES (?, ?)
            """,
            ("user1", hashed)
        )

        conn.commit()

# AUTH---------------------------------------------------------------------------
def validate_user(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    with get_connection() as conn:

        row = conn.execute(
            """SELECT id FROM users WHERE username=? AND password=?""",
            (username, hashed)
        ).fetchone()

    return row[0] if row else None

# REGISTER USER-----------------------------------------------------------------
def register_user(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    with get_connection() as conn:
        try:
            conn.execute("""
                INSERT INTO users (username, password)
                VALUES (?, ?)
            """, (username, hashed))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
# GET ALL USERS-----------------------------------------------------------------
def get_all_users():
    with get_connection() as conn:
        return conn.execute("""
            SELECT id, username FROM users
            ORDER BY id ASC
        """).fetchall()

# DELETE USER-----------------------------------------------------------------
def delete_user(user_id):
    with get_connection() as conn:
        # delete their photos files first
        photos = conn.execute(
            "SELECT filepath, thumbnail_path FROM photos WHERE user_id=?",
            (user_id,)
        ).fetchall()
        import os
        for filepath, thumbnail in photos:
            try:
                if filepath and os.path.exists(filepath):
                    os.remove(filepath)
            except: pass
            try:
                if thumbnail and os.path.exists(thumbnail):
                    os.remove(thumbnail)
            except: pass

        conn.execute("DELETE FROM photos WHERE user_id=?", (user_id,))
        conn.execute("DELETE FROM albums WHERE user_id=?", (user_id,))
        conn.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        
# MIGRATE DB-----------------------------------------------------------------
def migrate_db():
    with get_connection() as conn:
        try:
            conn.execute("ALTER TABLE photos ADD COLUMN is_deleted INTEGER DEFAULT 0")
        except Exception as e:
            print("is_deleted:", e)
        try:
            conn.execute("ALTER TABLE photos ADD COLUMN deleted_at TIMESTAMP")
        except Exception as e:
            print("deleted_at:", e)
        try:
            conn.execute("ALTER TABLE photos ADD COLUMN user_id INTEGER")
        except Exception as e:
            print("user_id:", e)
        try:
            conn.execute("ALTER TABLE albums ADD COLUMN user_id INTEGER")
        except Exception as e:
            print("albums user_id:", e)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS albums_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    user_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='albums'"
            ).fetchone()
            if tables:
                conn.execute("""
                    INSERT OR IGNORE INTO albums_new (id, name, user_id, created_at)
                    SELECT id, name, user_id, created_at FROM albums
                """)
                conn.execute("DROP TABLE albums")
                conn.execute("ALTER TABLE albums_new RENAME TO albums")
        except Exception as e:
            print("albums migration:", e)
        conn.commit()

# PHOTOS--------------------------------------------------------------------

def add_photo(
    filename,
    filepath,
    title=None,
    album_id=None,
    thumbnail_path=None,
    file_size=0,
    image_width=0,
    image_height=0,
    user_id=None
):

    with get_connection() as conn:

        conn.execute("""
            INSERT INTO photos (
                filename,
                filepath,
                title,
                album_id,
                thumbnail_path,
                file_size,
                image_width,
                image_height,
                user_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            filename,
            filepath,
            title,
            album_id,
            thumbnail_path,
            file_size,
            image_width,
            image_height,
            user_id
        ))

        conn.commit()

# GET PHOTOS--------------------------------------------------------------------

def get_photos(search=None, album_id=None, user_id=None):

    query = """
        SELECT
            id,
            filename,
            filepath,
            title,
            album_id,
            is_favorite,
            thumbnail_path,
            uploaded_at
        FROM photos
        WHERE is_deleted=0 AND user_id=?
    """
    params = [user_id]

    if search:
        query += "AND (title LIKE ? OR filename LIKE ?)"
        params += [f"%{search}%", f"%{search}%"]
    if album_id:
        query += " AND album_id=?"
        params.append(album_id)
    query += " ORDER BY uploaded_at DESC"

    with get_connection() as conn:
        return conn.execute(query,params).fetchall()

# DELETE PHOTO--------------------------------------------------------------------
def delete_photo(photo_id):
    move_to_trash(photo_id)

# FAVORITES--------------------------------------------------------------------
def toggle_favorite(photo_id):

    with get_connection() as conn:

        current = conn.execute(
            "SELECT is_favorite FROM photos WHERE id=?",
            (photo_id,)
        ).fetchone()

        if current:

            new_value = 0 if current[0] else 1

            conn.execute(
                """
                UPDATE photos
                SET is_favorite=?
                WHERE id=?
                """,
                (new_value, photo_id)
            )

            conn.commit()
            
# GET FAVORITE PHOTOS------------------------------------------
def get_favorite_photos(user_id=None):
    with get_connection() as conn:
        return conn.execute("""
            SELECT
                id,
                filename,
                filepath,
                title,
                album_id,
                is_favorite,
                thumbnail_path
            FROM photos
            WHERE is_favorite=1 AND is_deleted=0 AND user_id=?
            ORDER BY uploaded_at DESC
        """, (user_id,)).fetchall()

# ALBUMS-------------------------------------------------------------

def add_album(name, user_id=None):

    with get_connection() as conn:

        conn.execute(
            "INSERT INTO albums (name, user_id)VALUES (?, ?)",
            (name, user_id))
        conn.commit()

# GET ALBUMS----------------------------------------------------------------
def get_albums(user_id=None):
    with get_connection() as conn:
        return conn.execute("""
            SELECT
                id,
                name
            FROM albums
            WHERE user_id=?
            ORDER BY created_at DESC
        """, (user_id,)).fetchall()

# DELETE ALBUM----------------------------------------------------------------
def delete_album(album_id):

    with get_connection() as conn:

        # Remove album assignment
        conn.execute(
            """
            UPDATE photos
            SET album_id=NULL
            WHERE album_id=?
            """,
            (album_id,)
        )

        # Delete album
        conn.execute(
            """
            DELETE FROM albums
            WHERE id=?
            """,
            (album_id,)
        )

        conn.commit()

# RENAME ALBUM----------------------------------------------------------------
def rename_album(album_id, new_name):

    with get_connection() as conn:

        conn.execute(
            """
            UPDATE albums
            SET name=?
            WHERE id=?
            """,
            (new_name, album_id)
        )

        conn.commit()

# PHOTO COUNT-----------------------------------------------------------------
def get_album_photo_count(album_id):

    with get_connection() as conn:

        count = conn.execute(
            """
            SELECT COUNT(*)
            FROM photos
            WHERE album_id=?
            """,
            (album_id,)
        ).fetchone()[0]

    return count

# MOVE PHOTO TO ALBUM----------------------------------------------------------------
def move_photo_to_album(photo_id, album_id):

    with get_connection() as conn:

        conn.execute(
            """
            UPDATE photos
            SET album_id=?
            WHERE id=?
            """,
            (album_id, photo_id)
        )

        conn.commit()

# GET RECENT PHOTOS-----------------------------------------------------------------
def get_recent_photos(limit=20):

    with get_connection() as conn:

        return conn.execute(
            """
            SELECT
                id,
                filename,
                filepath,
                title,
                album_id
            FROM photos
            ORDER BY uploaded_at DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

# GET SINGLE ALBUM-----------------------------------------------------------------
def get_album(album_id):

    with get_connection() as conn:

        return conn.execute(
            """
            SELECT id, name
            FROM albums
            WHERE id=?
            """,
            (album_id,)
        ).fetchone()

# GET PHOTOS BY ALBUM-----------------------------------------------------------------
def get_photos_by_album(album_id):

    with get_connection() as conn:

        return conn.execute(
            """
            SELECT
                id,
                filename,
                filepath,
                title,
                is_favorite
            FROM photos
            WHERE album_id=? AND is_deleted=0
            ORDER BY uploaded_at DESC
            """,
            (album_id,)
        ).fetchall()

# MOVE TO TRASH-----------------------------------------------------------------
def move_to_trash(photo_id):
    from datetime import datetime
    with get_connection() as conn:
        print(f"Moving photo {photo_id} to trash")
        conn.execute("""
            UPDATE photos SET is_deleted=1, deleted_at=?
            WHERE id=?
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), photo_id))
        conn.commit()
        print("Done!")

# GET TRASHED PHOTOS-----------------------------------------------------------------
def get_trashed_photos(user_id=None):
    with get_connection() as conn:
        results = conn.execute("""
            SELECT id, filename, filepath, title, album_id,
                   is_favorite, thumbnail_path, deleted_at
            FROM photos WHERE is_deleted=1 AND user_id=?
            ORDER BY deleted_at DESC
        """, (user_id,)).fetchall()
        return results

# RESTORE PHOTO-----------------------------------------------------------------
def restore_photo(photo_id):
    with get_connection() as conn:
        print(f"Restoring photo {photo_id}")
        conn.execute("""
            UPDATE photos SET is_deleted=0, deleted_at=NULL
            WHERE id=?
        """, (photo_id,))
        conn.commit()
        print("Done!")

# PERMANENT DELETE-----------------------------------------------------------------
def permanent_delete(photo_id):
    with get_connection() as conn:
        photo = conn.execute(
            "SELECT filepath, thumbnail_path FROM photos WHERE id=?",
            (photo_id,)
        ).fetchone()
        if photo:
            try:
                if photo[0] and os.path.exists(photo[0]):
                    os.remove(photo[0])
            except: pass
            try:
                if photo[1] and os.path.exists(photo[1]):
                    os.remove(photo[1])
            except: pass
        conn.execute("DELETE FROM photos WHERE id=?", (photo_id,))
        conn.commit()

# EMPTY TRASH-----------------------------------------------------------------
def empty_trash():
    with get_connection() as conn:
        photos = conn.execute(
            "SELECT filepath, thumbnail_path FROM photos WHERE is_deleted=1"
        ).fetchall()
        for filepath, thumbnail in photos:
            try:
                if filepath and os.path.exists(filepath):
                    os.remove(filepath)
            except: pass
            try:
                if thumbnail and os.path.exists(thumbnail):
                    os.remove(thumbnail)
            except: pass
        conn.execute("DELETE FROM photos WHERE is_deleted=1")
        conn.commit()

# DATABASE START------------------------------------------------------------------
init_db()
migrate_db()
