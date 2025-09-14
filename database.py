"""
Database schema and initialization for the closet application.

This module defines the SQLite database schema with tables for:
- images: stores image file paths and descriptions
- categories: clothing categories (shirt, pants, shoes, etc.)
- tags: descriptive tags for clothing items
- image_categories: many-to-many relationship between images and categories
- image_tags: many-to-many relationship between images and tags
"""

import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging


class ClosetDatabase:
    """Manages the SQLite database for the closet application."""

    def __init__(self, db_path: str = "data/closet.db"):
        """
        Initialize the database connection.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.init_database()

    def init_database(self) -> None:
        """Initialize the database with required tables."""
        # Ensure the data directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Create images table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL UNIQUE,
                    file_path TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create categories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create tags table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create image_categories join table (many-to-many)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS image_categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_id INTEGER NOT NULL,
                    category_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (image_id) REFERENCES images (id) ON DELETE CASCADE,
                    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE,
                    UNIQUE(image_id, category_id)
                )
            """)

            # Create image_tags join table (many-to-many)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS image_tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_id INTEGER NOT NULL,
                    tag_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (image_id) REFERENCES images (id) ON DELETE CASCADE,
                    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE,
                    UNIQUE(image_id, tag_id)
                )
            """)

            # Create outfits table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS outfits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL UNIQUE,
                    file_path TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create outfit_items table (many-to-many relationship between outfits and clothing items)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS outfit_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    outfit_id INTEGER NOT NULL,
                    image_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (outfit_id) REFERENCES outfits (id) ON DELETE CASCADE,
                    FOREIGN KEY (image_id) REFERENCES images (id) ON DELETE CASCADE,
                    UNIQUE(outfit_id, image_id)
                )
            """)

            # Create indexes for better performance
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_images_filename ON images(filename)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_categories_name ON categories(name)"
            )
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tags_name ON tags(name)")
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_image_categories_image_id ON image_categories(image_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_image_categories_category_id ON image_categories(category_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_image_tags_image_id ON image_tags(image_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_image_tags_tag_id ON image_tags(tag_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_outfits_filename ON outfits(filename)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_outfit_items_outfit_id ON outfit_items(outfit_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_outfit_items_image_id ON outfit_items(image_id)"
            )

            conn.commit()
            logging.info("Database initialized successfully")

    def add_image(
        self, filename: str, file_path: str, description: Optional[str] = None
    ) -> int:
        """
        Add a new image to the database.

        Args:
            filename: Name of the image file
            file_path: Full path to the image file
            description: Optional description of the image

        Returns:
            ID of the created image record
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO images (filename, file_path, description)
                VALUES (?, ?, ?)
            """,
                (filename, file_path, description),
            )
            conn.commit()
            return cursor.lastrowid

    def get_image(self, image_id: int) -> Optional[Dict[str, Any]]:
        """
        Get an image by ID with its categories and tags.

        Args:
            image_id: ID of the image to retrieve

        Returns:
            Dictionary containing image data with categories and tags, or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Get image data
            cursor.execute("SELECT * FROM images WHERE id = ?", (image_id,))
            image_row = cursor.fetchone()

            if not image_row:
                return None

            # Get categories
            cursor.execute(
                """
                SELECT c.id, c.name, c.description
                FROM categories c
                JOIN image_categories ic ON c.id = ic.category_id
                WHERE ic.image_id = ?
            """,
                (image_id,),
            )
            categories = [dict(row) for row in cursor.fetchall()]

            # Get tags
            cursor.execute(
                """
                SELECT t.id, t.name
                FROM tags t
                JOIN image_tags it ON t.id = it.tag_id
                WHERE it.image_id = ?
            """,
                (image_id,),
            )
            tags = [dict(row) for row in cursor.fetchall()]

            return {**dict(image_row), "categories": categories, "tags": tags}

    def get_all_images(self) -> List[Dict[str, Any]]:
        """
        Get all images with their categories and tags.

        Returns:
            List of dictionaries containing image data with categories and tags
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM images ORDER BY created_at DESC")
            images = []

            for image_row in cursor.fetchall():
                image_id = image_row["id"]

                # Get categories for this image
                cursor.execute(
                    """
                    SELECT c.id, c.name, c.description
                    FROM categories c
                    JOIN image_categories ic ON c.id = ic.category_id
                    WHERE ic.image_id = ?
                """,
                    (image_id,),
                )
                categories = [dict(row) for row in cursor.fetchall()]

                # Get tags for this image
                cursor.execute(
                    """
                    SELECT t.id, t.name
                    FROM tags t
                    JOIN image_tags it ON t.id = it.tag_id
                    WHERE it.image_id = ?
                """,
                    (image_id,),
                )
                tags = [dict(row) for row in cursor.fetchall()]

                images.append(
                    {**dict(image_row), "categories": categories, "tags": tags}
                )

            return images

    def add_category(self, name: str, description: Optional[str] = None) -> int:
        """
        Add a new category.

        Args:
            name: Name of the category
            description: Optional description of the category

        Returns:
            ID of the created category record
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO categories (name, description)
                VALUES (?, ?)
            """,
                (name, description),
            )
            conn.commit()

            # Get the ID of the category (existing or newly created)
            cursor.execute("SELECT id FROM categories WHERE name = ?", (name,))
            return cursor.fetchone()[0]

    def add_tag(self, name: str) -> int:
        """
        Add a new tag.

        Args:
            name: Name of the tag

        Returns:
            ID of the created tag record
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO tags (name)
                VALUES (?)
            """,
                (name,),
            )
            conn.commit()

            # Get the ID of the tag (existing or newly created)
            cursor.execute("SELECT id FROM tags WHERE name = ?", (name,))
            return cursor.fetchone()[0]

    def assign_category_to_image(self, image_id: int, category_id: int) -> bool:
        """
        Assign a category to an image.

        Args:
            image_id: ID of the image
            category_id: ID of the category

        Returns:
            True if successful, False if already exists
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO image_categories (image_id, category_id)
                    VALUES (?, ?)
                """,
                    (image_id, category_id),
                )
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                # Already exists
                return False

    def assign_tag_to_image(self, image_id: int, tag_id: int) -> bool:
        """
        Assign a tag to an image.

        Args:
            image_id: ID of the image
            tag_id: ID of the tag

        Returns:
            True if successful, False if already exists
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO image_tags (image_id, tag_id)
                    VALUES (?, ?)
                """,
                    (image_id, tag_id),
                )
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                # Already exists
                return False

    def update_image_description(self, image_id: int, description: str) -> bool:
        """
        Update the description of an image.

        Args:
            image_id: ID of the image
            description: New description

        Returns:
            True if successful, False if image not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE images 
                SET description = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """,
                (description, image_id),
            )
            conn.commit()
            return cursor.rowcount > 0

    def get_categories(self) -> List[Dict[str, Any]]:
        """
        Get all categories.

        Returns:
            List of category dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories ORDER BY name")
            return [dict(row) for row in cursor.fetchall()]

    def get_tags(self) -> List[Dict[str, Any]]:
        """
        Get all tags.

        Returns:
            List of tag dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tags ORDER BY name")
            return [dict(row) for row in cursor.fetchall()]

    def search_images_by_category(self, category_name: str) -> List[Dict[str, Any]]:
        """
        Search for images by category name.

        Args:
            category_name: Name of the category to search for

        Returns:
            List of image dictionaries matching the category
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT DISTINCT i.*
                FROM images i
                JOIN image_categories ic ON i.id = ic.image_id
                JOIN categories c ON ic.category_id = c.id
                WHERE c.name = ?
                ORDER BY i.created_at DESC
            """,
                (category_name,),
            )

            images = []
            for image_row in cursor.fetchall():
                image_id = image_row["id"]

                # Get categories and tags for each image
                cursor.execute(
                    """
                    SELECT c.id, c.name, c.description
                    FROM categories c
                    JOIN image_categories ic ON c.id = ic.category_id
                    WHERE ic.image_id = ?
                """,
                    (image_id,),
                )
                categories = [dict(row) for row in cursor.fetchall()]

                cursor.execute(
                    """
                    SELECT t.id, t.name
                    FROM tags t
                    JOIN image_tags it ON t.id = it.tag_id
                    WHERE it.image_id = ?
                """,
                    (image_id,),
                )
                tags = [dict(row) for row in cursor.fetchall()]

                images.append(
                    {**dict(image_row), "categories": categories, "tags": tags}
                )

            return images

    def populate_existing_images(self, output_folder: Path) -> int:
        """
        Populate the database with existing images from the output folder.

        Args:
            output_folder: Path to the output folder containing processed images

        Returns:
            Number of images added to the database
        """
        if not output_folder.exists():
            return 0

        added_count = 0
        for image_path in output_folder.glob("*.png"):
            # Check if image already exists in database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id FROM images WHERE filename = ?", (image_path.name,)
                )
                if cursor.fetchone():
                    continue  # Image already exists, skip

            # Add image to database
            # image_id = self.add_image(
            #     filename=image_path.name, file_path=str(image_path), description=None
            # )

            added_count += 1

        return added_count

    def add_outfit(
        self, filename: str, file_path: str, description: Optional[str] = None
    ) -> int:
        """
        Add a new outfit to the database.

        Args:
            filename: Name of the outfit file
            file_path: Full path to the outfit file
            description: Optional description of the outfit

        Returns:
            ID of the created outfit record
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO outfits (filename, file_path, description)
                VALUES (?, ?, ?)
            """,
                (filename, file_path, description),
            )
            conn.commit()
            return cursor.lastrowid

    def get_outfit(self, outfit_id: int) -> Optional[Dict[str, Any]]:
        """
        Get an outfit by ID with its associated clothing items.

        Args:
            outfit_id: ID of the outfit to retrieve

        Returns:
            Dictionary containing outfit data with associated items, or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Get outfit data
            cursor.execute("SELECT * FROM outfits WHERE id = ?", (outfit_id,))
            outfit_row = cursor.fetchone()

            if not outfit_row:
                return None

            # Get associated clothing items
            cursor.execute(
                """
                SELECT i.id, i.filename, i.file_path, i.description, i.created_at
                FROM images i
                JOIN outfit_items oi ON i.id = oi.image_id
                WHERE oi.outfit_id = ?
                ORDER BY i.created_at
            """,
                (outfit_id,),
            )
            items = [dict(row) for row in cursor.fetchall()]

            return {**dict(outfit_row), "items": items}

    def get_all_outfits(self) -> List[Dict[str, Any]]:
        """
        Get all outfits with their associated clothing items.

        Returns:
            List of dictionaries containing outfit data with associated items
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM outfits ORDER BY created_at DESC")
            outfits = []

            for outfit_row in cursor.fetchall():
                outfit_id = outfit_row["id"]

                # Get associated clothing items
                cursor.execute(
                    """
                    SELECT i.id, i.filename, i.file_path, i.description, i.created_at
                    FROM images i
                    JOIN outfit_items oi ON i.id = oi.image_id
                    WHERE oi.outfit_id = ?
                    ORDER BY i.created_at
                """,
                    (outfit_id,),
                )
                items = [dict(row) for row in cursor.fetchall()]

                outfits.append({**dict(outfit_row), "items": items})

            return outfits

    def add_item_to_outfit(self, outfit_id: int, image_id: int) -> bool:
        """
        Add a clothing item to an outfit.

        Args:
            outfit_id: ID of the outfit
            image_id: ID of the clothing item

        Returns:
            True if successful, False if already exists
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO outfit_items (outfit_id, image_id)
                    VALUES (?, ?)
                """,
                    (outfit_id, image_id),
                )
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                # Already exists
                return False

    def remove_item_from_outfit(self, outfit_id: int, image_id: int) -> bool:
        """
        Remove a clothing item from an outfit.

        Args:
            outfit_id: ID of the outfit
            image_id: ID of the clothing item

        Returns:
            True if successful, False if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM outfit_items 
                WHERE outfit_id = ? AND image_id = ?
            """,
                (outfit_id, image_id),
            )
            conn.commit()
            return cursor.rowcount > 0

    def update_outfit_description(self, outfit_id: int, description: str) -> bool:
        """
        Update the description of an outfit.

        Args:
            outfit_id: ID of the outfit
            description: New description

        Returns:
            True if successful, False if outfit not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE outfits 
                SET description = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """,
                (description, outfit_id),
            )
            conn.commit()
            return cursor.rowcount > 0
