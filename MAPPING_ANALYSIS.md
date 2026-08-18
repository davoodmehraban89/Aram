# Mapping Analysis

## Overview
This document provides a deep analysis of the canonical mapping rules found in `data/mappings/mapping_1404.xlsx`.

## 1. Mapping Types
Total logical mapping rules: 497

| Mapping Type | Count | Percentage |
|--------------|-------|------------|
| O | 456 | 91.75% |
| E | 17 | 3.42% |
| OE | 17 | 3.42% |
| e | 5 | 1.01% |
| E2 | 1 | 0.20% |
| Oe | 1 | 0.20% |

## 2. Dimensional Dependency
The mapping workbook demonstrates composite dimensional matching, disproving the assumption that mapping is purely account-based.

- **Unique Account Codes**: 392
- **Accounts with Multiple Rules**: 21
- **Rules dependent on T1_CODE**: 43
- **Rules dependent on T4_CODE**: 66
- **Rules dependent on Current/Capital**: 43
- **Rules using any dimensional combination (T1/T4/CC)**: 66
- **Duplicate Rules**: 0

## 3. Account 8161 Case Study
Account 8161 is heavily multi-dimensional. A simple `account_code -> note` mapper will completely fail for this account.

- **Exact Rule Count**: 66
- **T1-dependent Rules**: 43 (over 32 distinct T1 codes)
- **T4-dependent Rules**: 66 (over 28 distinct T4 codes)
- **Current/Capital-dependent Rules**: 43 (distinguishing 'سرمایه ای' vs 'جاری')
- **Mapping Types used**: O, E
- **Destination Notes**: 19-1, -, 10, 13, 12-1

An account-code-only mapper would assign a single note to all 8161 records, missing the nuance that routes specific T4/T1 combinations to different notes (e.g., separating capital vs. current projects).
