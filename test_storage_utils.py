from io import BytesIO
from unittest import TestCase
from zipfile import ZipFile

from storage_utils import build_zip, format_bytes, get_file_category


class StorageUtilsTests(TestCase):
    def test_format_bytes(self) -> None:
        self.assertEqual(format_bytes(0), "0 B")
        self.assertEqual(format_bytes(1024), "1.0 KB")

    def test_format_bytes_rejects_negative_values(self) -> None:
        with self.assertRaises(ValueError):
            format_bytes(-1)

    def test_get_file_category_is_case_insensitive(self) -> None:
        self.assertEqual(get_file_category("photo.JPG"), "jpg")
        self.assertEqual(get_file_category("README"), "No extension")

    def test_build_zip_sanitizes_paths_and_disambiguates_duplicates(self) -> None:
        archive_bytes = build_zip(
            [
                ("folder/photo.jpg", b"first"),
                ("another\\photo.jpg", b"second"),
                ("../notes.txt", b"notes"),
            ]
        )

        with ZipFile(BytesIO(archive_bytes)) as archive:
            self.assertEqual(
                archive.namelist(),
                ["photo.jpg", "photo (2).jpg", "notes.txt"],
            )
            self.assertEqual(archive.read("photo (2).jpg"), b"second")
