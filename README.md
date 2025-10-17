# Integrative Oncology Services Dataset - Australian Cities

[![Data License](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Data Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()
[![Last Updated](https://img.shields.io/badge/Last%20Updated-October%202025-blue.svg)]()

## Overview

This repository contains a curated dataset of **185 integrative oncology and wellness services** available across seven Australian metropolitan areas: Melbourne, Sydney, Perth, Darwin, Hobart, Brisbane, and Adelaide.

**Visit our website:** [https://afzal0.github.io/cancer-oncology/](https://afzal0.github.io/cancer-oncology/)

## Dataset Summary

| Metric | Value |
|--------|-------|
| Total Services | 185 |
| Cities Covered | 7 |
| Data Fields | 13 |
| Collection Period | August 2025 |
| Verification Date | October 2025 |

### Coverage by City

- **Sydney:** 35 records
- **Melbourne:** 33 records
- **Perth:** 28 records
- **Brisbane:** 27 records
- **Adelaide:** 25 records
- **Hobart:** 21 records
- **Darwin:** 16 records

## Value of the Data

1. **Standardized Registry:** Provides a single, standardized registry of publicly provided integrative oncology services across seven Australian cities, including fields for provider type, eligibility, and cost that are often missing from disparate listings.

2. **Group-Program Focus:** Supplies group-program identifiers (e.g., yoga, meditation, exercise, support groups) to facilitate reproducible service audits of evidence-informed modalities referenced in international guidance.

3. **Verification Status:** Documents verification status through verification notes, enabling transparent reuse and quality appraisal.

## Data Access

### Download Options

- **CSV Format:** [`data/integrative_oncology_services.csv`](data/integrative_oncology_services.csv)
- **Excel Format:** [`Data_final_cleaned.xlsx`](Data_final_cleaned.xlsx)

### Data Structure

Each record includes 13 standardized fields:

| Field | Description |
|-------|-------------|
| `Name` | Service name |
| `Organization` | Parent organization |
| `Provider Type` | Public hospital, NGO, university, council, etc. |
| `Facility Type` | Category of facility |
| `Address` | Street address |
| `Suburb` | Suburb/locality |
| `Postcode` | Australian postcode |
| `Phone` | Contact phone number |
| `Website` | Official website or program page |
| `group_services_standardized` | Controlled terms for group programs (yoga, meditation, exercise, support groups, etc.) |
| `individual_services_standardized` | One-on-one services (massage, acupuncture, psychology, etc.) |
| `associated_services_standardized` | Additional support services (social work, spiritual care) |
| `Verification Notes (as of Oct 2025)` | Quality assurance documentation |

## Documentation

Comprehensive documentation is available:

- **[Data Dictionary](https://afzal0.github.io/cancer-oncology/docs/documentation.html)** - Complete field definitions and controlled vocabularies
- **[Methodology](https://afzal0.github.io/cancer-oncology/docs/documentation.html#methodology)** - Data collection protocol and verification procedures
- **[Limitations](https://afzal0.github.io/cancer-oncology/docs/documentation.html#limitations)** - Known constraints and future updates

## Methodology

### Inclusion Criteria

- Services designed for cancer patients, survivors, or caregivers
- Evidence-informed complementary/supportive activities
- Publicly accessible (public hospital, NGO, or council)
- Active in August 2025
- Sufficient public information to populate required fields

### Data Collection

Multi-pronged approach:
1. Structured web searches with city and service terms
2. Targeted hospital/NGO/council website navigation
3. Professional directories and registries
4. Direct verification in October 2025

### Quality Control

- Duplicate detection and removal
- Internal consistency checks
- External cross-validation with Cancer Council and institutional pages
- Two-researcher independent extraction with consensus reconciliation

## Usage

### For Researchers

```python
import pandas as pd

# Load the dataset
df = pd.read_csv('data/integrative_oncology_services.csv')

# Explore services by city
print(df['Suburb'].value_counts())

# Filter for specific service types
yoga_services = df[df['group_services_standardized'].str.contains('yoga', na=False)]
```

### For Clinicians and Planners

This dataset can be used for:
- Service mapping and gap analysis
- Patient resource directories
- Clinical pathway development
- Health services research
- Policy and planning activities

## Citation

If you use this dataset in your research or practice, please cite:

```
Khan, M.A., Adhinugraha, K.M., Phan, A., Lyu, S., Manger, S., Phan, T., & Taniar, D. (2025).
Dataset of Integrative Oncology and Wellness Services in Major Australian Cities:
A Comprehensive Mapping of Public and NGO-Based Support Services with Emphasis on Group-Based Programs.
Data in Brief.
```

## Authors

- Mohammad Afzal Khan¹
- Kiki Maulana Adhinugraha²
- Albert Phan
- Shiyang Lyu¹
- Sam Manger³
- Thanh Phan
- David Taniar¹

**Affiliations:**
1. Faculty of Information Technology, Monash University, Melbourne, Australia
2. School of Computing and Information Technology, La Trobe University, Melbourne, Australia
3. College of Medicine and Dentistry, James Cook University, Queensland, Australia

**Corresponding Author:** David Taniar - [David.taniar@monash.edu](mailto:David.taniar@monash.edu)

## License

This dataset is released under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

You are free to:
- **Share** — copy and redistribute the material
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit and indicate if changes were made

## Limitations

- Dataset represents a point-in-time snapshot (August-October 2025)
- Some fields (eligibility criteria, operating hours, cost structure) could not be consistently obtained
- Users should verify current service availability directly with providers

## Contributing

We welcome contributions! Please:
- Report service changes or closures
- Submit new services
- Provide data quality feedback
- Suggest additional fields or features

Contact the corresponding author to contribute updates or corrections.

## Related Research

1. Grant, S.J., et al. (2019). Establishing an integrative oncology service in the Australian healthcare setting—The Chris O'Brien Lifehouse Hospital experience. *Supportive Care in Cancer*, 27. doi:10.1007/s00520-018-4460-2

2. Smith, C.A., et al. (2017). Integrative oncology in Australia 2016: Mapping service provision and exploring unmet needs. Western Sydney University. doi:10.4225/35/5977cde41bd1c

3. Lyman, G.H., et al. (2022). Integrative Medicine for Pain Management in Oncology: Society for Integrative Oncology–ASCO Guideline. *Journal of Clinical Oncology*, 40(34), 3818–3843. doi:10.1200/JCO.22.01357

4. Witt, C.M., et al. (2017). A comprehensive definition for integrative oncology. *NCI Monographs*, 2017(52). doi:10.1093/jncimonographs/lgx012

## Acknowledgments

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

## Contact

For questions or feedback about this dataset:

**Email:** [David.taniar@monash.edu](mailto:David.taniar@monash.edu)

---

*Data collected August 2025, verified October 2025*
