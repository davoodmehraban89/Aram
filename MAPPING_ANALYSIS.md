# MAPPING ANALYSIS

## Source
File: `data/mappings/مبنای ارتباط حسابها با یادداشتها سال 1404.xlsx` (Sheet: `Data`)

## Structure
This file contains mapping rules linking account codes to specific Notes and defining their behavior (Type O, Oe, E).

## Challenges
1. **Year Specificity**: Only the 1404 mapping is available. It must be versioned. 1402 and 1403 mappings must be assumed identical or reconstructed, which is dangerous. (DOMAIN CONFIRMATION REQUIRED)
2. **Missing Dimensions**: The mapping appears to operate mostly on Account Code. Needs validation against the required T1-T4 dimensions mentioned in the Directive.

## Implementation Path
- Parse the `Data` sheet.
- Model as `MappingRule(company, fiscal_year, account_code, note_reference, mapping_type)`.
- Use this strictly for the 1404 configuration version.
