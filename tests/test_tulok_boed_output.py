"""
Validation tests for scraped output.json from tulok_boed spider.
Run after: scrapy crawl tulok_boed -o output.json
"""
import json
from os.path import dirname, exists, join

import pytest

# Load the scraped output if it exists
output_path = join(dirname(__file__), "..", "output.json")

if not exists(output_path):
    pytest.skip(
        "output.json not found. Run: scrapy crawl tulok_boed -o output.json",
        allow_module_level=True,
    )

with open(output_path, "r") as f:
    scraped_items = json.load(f)


def test_items_scraped():
    """Verify items were scraped."""
    assert len(scraped_items) > 0, "No items scraped"


def test_required_fields():
    """Verify all required Meeting fields are present."""
    required_fields = [
        "title",
        "description",
        "classification",
        "start",
        "end",
        "all_day",
        "time_notes",
        "location",
        "links",
        "source",
        "status",
        "id",
    ]
    for item in scraped_items:
        for field in required_fields:
            assert field in item, f"Missing field: {field}"


def test_classification():
    """Verify all items have BOARD classification."""
    for item in scraped_items:
        assert item["classification"] == "Board"


def test_location_structure():
    """Verify location has correct structure."""
    for item in scraped_items:
        assert "name" in item["location"]
        assert "address" in item["location"]
        assert item["location"]["address"] != ""


def test_links_structure():
    """Verify links have correct structure."""
    for item in scraped_items:
        assert isinstance(item["links"], list)
        for link in item["links"]:
            assert "href" in link
            assert "title" in link


def test_start_datetime_format():
    """Verify start datetime is properly formatted."""
    for item in scraped_items:
        assert item["start"] is not None
        # Format: "2025-12-08 17:30:00"
        assert len(item["start"]) == 19


def test_status_values():
    """Verify status is one of valid values."""
    valid_statuses = ["tentative", "confirmed", "passed", "cancelled"]
    for item in scraped_items:
        assert item["status"] in valid_statuses


def test_id_format():
    """Verify ID follows expected format."""
    for item in scraped_items:
        assert item["id"].startswith("tulok_boed/")


def test_source_url():
    """Verify source URLs are valid."""
    for item in scraped_items:
        assert item["source"].startswith("https://tulsaschools.diligent.community/")
