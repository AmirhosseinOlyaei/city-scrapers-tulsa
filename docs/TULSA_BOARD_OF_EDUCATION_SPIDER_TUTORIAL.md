# Tulsa Board of Education Spider Tutorial

A step-by-step guide on how the Tulsa Public Schools Board of Education meeting scraper was built using the Diligent Community API.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
   - [What We Built](#what-we-built)
   - [Why JSON API Pattern](#why-json-api-pattern)
2. [Understanding the Target Website](#2-understanding-the-target-website)
   - [Analyzing the API Endpoint](#analyzing-the-api-endpoint)
   - [API Response Structure](#api-response-structure)
   - [Key Data Fields](#key-data-fields)
3. [Building the Spider](#3-building-the-spider)
   - [File Structure](#file-structure)
   - [Spider Configuration](#spider-configuration)
   - [Request Generation](#request-generation)
   - [Parsing the JSON Response](#parsing-the-json-response)
   - [Helper Methods](#helper-methods)
4. [Writing Tests](#4-writing-tests)
   - [Creating JSON Fixtures](#creating-json-fixtures)
   - [Test Structure](#test-structure)
   - [Testing Each Field](#testing-each-field)
5. [Code Review and Lessons Learned](#5-code-review-and-lessons-learned)
   - [Location Parsing Pattern](#location-parsing-pattern)
   - [Date Parsing Strategy](#date-parsing-strategy)
   - [Lessons Learned](#lessons-learned)
6. [Pull Request Process](#6-pull-request-process)
   - [PR Description Template](#pr-description-template)
   - [Manual Testing Steps](#manual-testing-steps)
7. [Key Takeaways](#7-key-takeaways)

---

## 1. Project Overview

### What We Built

We created a scraper for the Tulsa Public Schools Board of Education:

| Spider Name | Agency | Data Source |
|-------------|--------|-------------|
| `tulok_boed` | Tulsa Public Schools Board of Education | Diligent Community API |

This spider scrapes meeting information from the Diligent Community platform, which provides meeting data via a JSON API.

### Why JSON API Pattern

Unlike HTML-based scrapers that parse DOM elements, this spider:
- Consumes a **JSON API** that returns structured meeting data
- Requires **no HTML parsing** — data is already structured
- Is **more reliable** since API responses are consistent
- Disables `ROBOTSTXT_OBEY` since the API endpoint isn't covered by robots.txt

**Benefits:**
- Cleaner parsing logic
- Less brittle than CSS selectors
- Direct access to all meeting fields

---

## 2. Understanding the Target Website

Before writing any code, we analyzed the API structure.

### Analyzing the API Endpoint

**Base URL:**
```
https://tulsaschools.diligent.community/Services/MeetingsService.svc/meetings
```

**URL Pattern with date filter:**
```
https://tulsaschools.diligent.community/Services/MeetingsService.svc/meetings?from={YYYY-MM-DD}&to=9999-12-31
```

**Example:** Meetings from December 1, 2024 onwards:
```
https://tulsaschools.diligent.community/Services/MeetingsService.svc/meetings?from=2024-12-01&to=9999-12-31
```

### API Response Structure

The API returns a JSON array of meeting objects:

```json
[
  {
    "Id": 213,
    "MeetingTypeName": "Regular Meeting",
    "MeetingDateTime": "2026-12-14 17:30",
    "MeetingLocation": "Cheryl Selman Room, Charles C. Mason Education Service Center, 3027 S. New Haven Ave., Tulsa OK",
    "MeetingStatus": null,
    "HasAgenda": true,
    "HasMinutes": false
  },
  ...
]
```

### Key Data Fields

| API Field | Maps To | Example Value |
|-----------|---------|---------------|
| `Id` | Links, Source URL | `213` |
| `MeetingTypeName` | Title | `"Regular Meeting"` |
| `MeetingDateTime` | Start datetime | `"2026-12-14 17:30"` |
| `MeetingLocation` | Location | `"Cheryl Selman Room, ... Tulsa OK"` |
| `HasAgenda` | Links | `true` / `false` |

**Meeting Info Page URL Pattern:**
```
https://tulsaschools.diligent.community/Portal/MeetingInformation.aspx?Org=Cal&Id={meeting_id}
```

---

## 3. Building the Spider

### File Structure

```
city_scrapers/
└── spiders/
    ├── __init__.py
    └── tulok_boed.py        # Board of Education spider

tests/
├── files/
│   └── tulok_boed.json      # JSON fixture from API
└── test_tulok_boed.py       # Test suite
```

### Spider Configuration

```python
# city_scrapers/spiders/tulok_boed.py

import re
from datetime import datetime

import scrapy
from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.relativedelta import relativedelta


class TulokBoedSpider(CityScrapersSpider):
    name = "tulok_boed"
    agency = "Tulsa Public Schools Board of Education"
    timezone = "America/Chicago"
    start_url = "https://tulsaschools.diligent.community/Services/MeetingsService.svc/meetings?from={start_date}&to=9999-12-31"
    agenda_url = "https://tulsaschools.diligent.community/Portal/MeetingInformation.aspx?Org=Cal&Id={}"
    custom_settings = {"ROBOTSTXT_OBEY": False}
```

**Key Configuration Notes:**
- **`timezone`**: `"America/Chicago"` — Tulsa is in Central Time
- **`custom_settings`**: Disables robots.txt since the API isn't covered
- **`start_url`**: Template with `{start_date}` placeholder
- **`agenda_url`**: Template for building meeting links

### Request Generation

Scrape meetings from 2 years ago to the far future:

```python
def start_requests(self):
    """Generate initial requests with formatted start date."""
    start_date = datetime.now().date() - relativedelta(years=2)
    url = self.start_url.format(start_date=start_date.isoformat())
    yield scrapy.Request(url=url, callback=self.parse)
```

**Why 2 years back?**
- Captures historical meetings for archive purposes
- Single request covers past + future (unlike month-by-month scraping)

### Parsing the JSON Response

Build `Meeting` items directly from JSON:

```python
def parse(self, response):
    """
    Parse meeting items from the Diligent Community API.
    Returns JSON array of meeting objects with full details.
    """
    data = response.json()
    for item in data:
        meeting = Meeting(
            title=item.get("MeetingTypeName") or "Board Meeting",
            description="",
            classification=BOARD,
            start=self._parse_start(item),
            end=None,
            all_day=False,
            time_notes="",
            location=self._parse_location(item),
            links=self._parse_links(item),
            source=self._parse_source(item),
        )

        meeting["status"] = self._get_status(meeting)
        meeting["id"] = self._get_id(meeting)

        yield meeting
```

**Key Points:**
- `response.json()` parses JSON directly (no BeautifulSoup/CSS needed)
- Fallback title: `"Board Meeting"` if `MeetingTypeName` is empty
- `classification=BOARD` — all meetings are board meetings

### Helper Methods

**Parse Start Time:**
```python
def _parse_start(self, item):
    """Parse start datetime from MeetingDateTime field.
    Format: '2025-06-16 18:30'
    """
    dt_str = item.get("MeetingDateTime")
    if dt_str:
        try:
            return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return None
    return None
```

**Parse Location (regex-based splitting):**
```python
def _parse_location(self, item):
    """Parse location from MeetingLocation field."""
    location_str = item.get("MeetingLocation", "")
    # Split on street address pattern (starts with number)
    match = re.search(r",\s*(\d+\s+.+)$", location_str)
    if match:
        name = location_str[: match.start()].strip()
        address = match.group(1)
    else:
        name = ""
        address = location_str
    return {"name": name, "address": address}
```

**Location Parsing Logic:**
- Input: `"Cheryl Selman Room, Charles C. Mason Education Service Center, 3027 S. New Haven Ave., Tulsa OK"`
- Regex finds address starting with digits: `3027 S. New Haven Ave., Tulsa OK`
- Everything before is the name: `Cheryl Selman Room, Charles C. Mason Education Service Center`

**Parse Links:**
```python
def _parse_links(self, item):
    """Generate agenda link using meeting ID."""
    meeting_id = item.get("Id")
    if meeting_id:
        return [{"href": self.agenda_url.format(meeting_id), "title": "Agenda"}]
    return []
```

**Parse Source:**
```python
def _parse_source(self, item):
    """Generate source link to meeting information page."""
    meeting_id = item.get("Id")
    if meeting_id:
        return self.agenda_url.format(meeting_id)
    return "https://tulsaschools.diligent.community/Portal/"
```

---

## 4. Writing Tests

### Creating JSON Fixtures

We save the real API response as a test fixture:

```
tests/files/
└── tulok_boed.json    # API response fixture
```

**How to capture:**
```bash
curl "https://tulsaschools.diligent.community/Services/MeetingsService.svc/meetings?from=2024-12-01&to=9999-12-31" \
  > tests/files/tulok_boed.json
```

### Test Structure

```python
# tests/test_tulok_boed.py

from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.tulok_boed import TulokBoedSpider

# Load fixture
test_response = file_response(
    join(dirname(__file__), "files", "tulok_boed.json"),
    url="https://tulsaschools.diligent.community/Services/MeetingsService.svc/meetings?from=2024-12-01&to=9999-12-31",
)
spider = TulokBoedSpider()

# Freeze time to control status calculation
freezer = freeze_time("2025-12-09")
freezer.start()
parsed_items = [item for item in spider.parse(test_response)]
freezer.stop()

# Get first item for field testing
parsed_item = parsed_items[0]
```

**Why `freeze_time`?**
Meeting status depends on current date:
- Future meeting → `tentative`
- Past meeting → `passed`
- Cancelled → `cancelled`

By freezing time, tests are deterministic and repeatable.

### Testing Each Field

```python
def test_count():
    assert len(parsed_items) == 56


def test_title():
    assert parsed_item["title"] == "Regular Meeting"


def test_description():
    assert parsed_item["description"] == ""


def test_classification():
    assert parsed_item["classification"] == BOARD


def test_start():
    assert parsed_item["start"] == datetime(2026, 12, 14, 17, 30)


def test_end():
    assert parsed_item["end"] is None


def test_time_notes():
    assert parsed_item["time_notes"] == ""


def test_id():
    assert parsed_item["id"] == "tulok_boed/202612141730/x/regular_meeting"


def test_status():
    assert parsed_item["status"] == "tentative"


def test_location():
    assert parsed_item["location"] == {
        "name": "Cheryl Selman Room, Charles C. Mason Education Service Center",
        "address": "3027 S. New Haven Ave., Tulsa OK",
    }


def test_source():
    assert (
        parsed_item["source"]
        == "https://tulsaschools.diligent.community/Portal/MeetingInformation.aspx?Org=Cal&Id=213"
    )


def test_links():
    assert parsed_item["links"] == [
        {
            "href": "https://tulsaschools.diligent.community/Portal/MeetingInformation.aspx?Org=Cal&Id=213",
            "title": "Agenda",
        }
    ]


def test_all_day():
    assert parsed_item["all_day"] is False
```

---

## 5. Code Review and Lessons Learned

### Location Parsing Pattern

**Challenge:** Location field contains both venue name and street address in a single string.

**Solution:** Use regex to split on street address pattern (starts with digits):

```python
match = re.search(r",\s*(\d+\s+.+)$", location_str)
```

**Example:**
- Input: `"Venue Name, 123 Main St., City OK"`
- Match: `, 123 Main St., City OK`
- Name: `Venue Name`
- Address: `123 Main St., City OK`

### Date Parsing Strategy

**API Format:** `"YYYY-MM-DD HH:MM"`

**Parsing:**
```python
datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
```

**Error Handling:** Wrap in try/except to handle malformed dates gracefully.

### Lessons Learned

1. **JSON APIs are simpler** — No CSS selectors, no HTML parsing
2. **Use `response.json()`** — Scrapy's built-in JSON parsing
3. **Regex for location splitting** — Pattern: find address by leading digits
4. **Disable robots.txt when needed** — API endpoints often aren't covered
5. **Wide date ranges work** — Single request can cover years of data
6. **Test with real fixtures** — Save actual API responses for tests

---

## 6. Pull Request Process

### PR Description Template

```markdown
## What's this PR do?
Adds a spider to scrape meeting information from Tulsa Public Schools 
Board of Education using the Diligent Community API.

- Spider: `tulok_boed`
- Agency: Tulsa Public Schools Board of Education
- Data source: JSON API

## Why are we doing this?
Requested based on the following spreadsheet: [Scraper Audit]

## Steps to manually test
1. `pipenv sync --dev`
2. `pipenv shell`
3. `scrapy crawl tulok_boed -O test_output.csv`
4. `pytest tests/test_tulok_boed.py -v`

## Are there any smells or added technical debt to note?
- Uses JSON API instead of HTML scraping
- Disables ROBOTSTXT_OBEY for API endpoint access
- Scrapes 2 years of history in single request
```

### Manual Testing Steps

```bash
# Install dependencies
pipenv sync --dev
pipenv shell

# Run spider
scrapy crawl tulok_boed -O test_output.csv

# Check output
cat test_output.csv | head -20

# Run tests
pytest tests/test_tulok_boed.py -v

# Check linting
flake8 city_scrapers/spiders/tulok_boed.py
```

---

## 7. Key Takeaways

| Principle | Application |
|-----------|-------------|
| **JSON over HTML** | When API available, use it |
| **Test with real data** | Save actual API responses as fixtures |
| **Regex for parsing** | Split compound fields like location |
| **Freeze time in tests** | Make status tests deterministic |
| **Handle missing data** | Provide fallbacks for optional fields |
| **Single request** | Wide date ranges reduce complexity |

**Files Created:**

| File | Purpose |
|------|---------|
| `city_scrapers/spiders/tulok_boed.py` | Board of Education spider |
| `tests/test_tulok_boed.py` | Test suite |
| `tests/files/tulok_boed.json` | API response fixture |

---

*This tutorial documents the development process of the Tulsa Public Schools Board of Education spider for the city-scrapers-tulsa project.*
