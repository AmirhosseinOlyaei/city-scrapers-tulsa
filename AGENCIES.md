# Tulsa Agencies

Complete list of agencies to be scraped. Spider prefix: `tulok`

## Agencies (24 total)

| ID | Agency Name | Suggested Spider Name | Website |
|----|-------------|----------------------|---------|
| 1645 | Arts Commission of City of Tulsa (ARTS) | `tulok_arts_commission` | https://www.cityoftulsa.org/government/departments/planning-and-neighborhoods/community-development/tulsa-arts/tulsa-arts-commission/ |
| 1665 | Asian Affairs Commission (AAC) | `tulok_asian_affairs` | https://www.cityoftulsa.org/government/departments/resilience-and-equity/civic-and-community-engagement/commissions/asian-american/ |
| 1666 | Audit Committee of the City of Tulsa (AUDIT) | `tulok_audit_committee` | - |
| 1667 | Beyond Apology Commission (BAC) | `tulok_beyond_apology` | https://www.cityoftulsa.org/beyondcommission |
| 1881 | City of Tulsa | `tulok_city` | - |
| 1670 | City of Tulsa-Rogers County Port Authority (COTRCPA) | `tulok_port_authority` | https://tulsaports.com/board-of-directors/ |
| 1737 | Emergency Medical Services Authority | `tulok_emsa` | https://emsaok.gov/about/ |
| 1739 | Gilcrease Museum Board of Trustees | `tulok_gilcrease` | https://gilcrease.org/about/contact/staff/ |
| 1740 | Greater Tulsa Area African-American Affairs Commission | `tulok_african_american` | https://www.cityoftulsa.org/government/departments/resilience-and-equity/civic-and-community-engagement/commissions/african-american-affairs/ |
| 1644 | Tulsa Animal Welfare Commission | `tulok_animal_welfare` | - |
| 1668 | Tulsa Board of Adjustment (BOA) | `tulok_boa` | https://tulsaplanning.org/boards-commissions/city-of-tulsa-board-of-adjustment/ |
| 1669 | Tulsa Board of Appeals | `tulok_appeals` | - |
| 1846 | Tulsa Board of County Commissioners | `tulok_county_commissioners` | https://www2.tulsacounty.org/government/board-of-county-commissioners/ |
| 1642 | Tulsa City Council | `tulok_city_council` | https://www.tulsacouncil.org/meetings |
| 1671 | Tulsa Civil Service Commission | `tulok_civil_service` | - |
| 1672 | Tulsa Community Development Committee (HUD) | `tulok_community_dev` | https://www.cityoftulsa.org/government/departments/finance/grants/hud-community-development-committee/ |
| 1787 | Tulsa Development Authority | `tulok_dev_authority` | - |
| 1736 | Tulsa Election District Commission | `tulok_election` | - |
| 1738 | Tulsa Ethics Advisory Committee | `tulok_ethics` | - |
| 1788 | Tulsa Parks and Recreation Board | `tulok_parks_rec` | https://www.cityoftulsa.org/government/departments/park-and-recreation/administration/park-board/ |
| 1583 | Tulsa Public Schools Board of Education | `tulok_public_schools` | https://www.tulsaschools.org/about/board-of-education |
| 1742 | Tulsa Stadium Trust | `tulok_stadium_trust` | https://www.cityoftulsa.org/residents/arts-recreation/downtown-tulsa/tulsa-stadium-improvement-district/ |
| 1741 | Tulsa Women's Commission | `tulok_womens` | https://www.cityoftulsa.org/government/departments/resilience-and-equity/civic-and-community-engagement/commissions/tulsa-womens-commission/ |
| 1789 | Union Public Schools Board of Education | `tulok_union_schools` | https://www.unionps.org/about/board-of-education |

## Notes

- Many agencies share the same calendar system at cityoftulsa.org
- Consider using a mixin pattern for agencies with shared URL sources
- Spider naming convention: `tulok_<short_descriptive_name>`
