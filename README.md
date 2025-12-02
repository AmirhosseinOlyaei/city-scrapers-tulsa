# City Scrapers - Tulsa

Web scrapers for public meetings in Tulsa, Oklahoma.

**Spider prefix**: `tulok`

## Agencies (24 total)

| Agency Name | Scraper Name | Website |
|-------------|--------------|---------|
| Arts Commission of City of Tulsa (ARTS) | `tulok_arts_commission` | [Link](https://www.cityoftulsa.org/government/departments/planning-and-neighborhoods/community-development/tulsa-arts/tulsa-arts-commission/) |
| Asian Affairs Commission (AAC) | `tulok_asian_affairs` | [Link](https://www.cityoftulsa.org/government/departments/resilience-and-equity/civic-and-community-engagement/commissions/asian-american/) |
| Audit Committee of the City of Tulsa (AUDIT) | `tulok_audit_committee` | - |
| Beyond Apology Commission (BAC) | `tulok_beyond_apology` | [Link](https://www.cityoftulsa.org/beyondcommission) |
| City of Tulsa | `tulok_city` | - |
| City of Tulsa-Rogers County Port Authority (COTRCPA) | `tulok_port_authority` | [Link](https://tulsaports.com/board-of-directors/) |
| Emergency Medical Services Authority | `tulok_emsa` | [Link](https://emsaok.gov/about/) |
| Gilcrease Museum Board of Trustees | `tulok_gilcrease` | [Link](https://gilcrease.org/about/contact/staff/) |
| Greater Tulsa Area African-American Affairs Commission | `tulok_african_american_affairs` | [Link](https://www.cityoftulsa.org/government/departments/resilience-and-equity/civic-and-community-engagement/commissions/african-american-affairs/) |
| Tulsa Animal Welfare Commission | `tulok_animal_welfare` | - |
| Tulsa Board of Adjustment (BOA) | `tulok_board_of_adjustment` | [Link](https://tulsaplanning.org/boards-commissions/city-of-tulsa-board-of-adjustment/) |
| Tulsa Board of Appeals | `tulok_board_of_appeals` | - |
| Tulsa Board of County Commissioners | `tulok_county_commissioners` | [Link](https://www2.tulsacounty.org/government/board-of-county-commissioners/) |
| Tulsa City Council | `tulok_city_council` | [Link](https://www.tulsacouncil.org/meetings) |
| Tulsa Civil Service Commission | `tulok_civil_service` | - |
| Tulsa Community Development Committee (HUD) | `tulok_community_dev` | [Link](https://www.cityoftulsa.org/government/departments/finance/grants/hud-community-development-committee/) |
| Tulsa Development Authority | `tulok_dev_authority` | - |
| Tulsa Election District Commission | `tulok_election_district` | - |
| Tulsa Ethics Advisory Committee | `tulok_ethics` | - |
| Tulsa Parks and Recreation Board | `tulok_parks_rec` | [Link](https://www.cityoftulsa.org/government/departments/park-and-recreation/administration/park-board/) |
| Tulsa Public Schools Board of Education | `tulok_public_schools` | [Link](https://www.tulsaschools.org/about/board-of-education) |
| Tulsa Stadium Trust | `tulok_stadium_trust` | [Link](https://www.cityoftulsa.org/residents/arts-recreation/downtown-tulsa/tulsa-stadium-improvement-district/) |
| Tulsa Women's Commission | `tulok_womens_commission` | [Link](https://www.cityoftulsa.org/government/departments/resilience-and-equity/civic-and-community-engagement/commissions/tulsa-womens-commission/) |
| Union Public Schools Board of Education | `tulok_union_schools` | [Link](https://www.unionps.org/about/board-of-education) |

## Setup

```bash
pipenv install --dev
```

## Running Scrapers

```bash
# Run a specific scraper
pipenv run scrapy crawl tulok_city_council

# Run all scrapers
pipenv run scrapy list | xargs -I {} pipenv run scrapy crawl {}
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
