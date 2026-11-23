# Lotto Lab — Development Roadmap

## Project Goal

Build a reproducible Western 649 lottery data application that collects, validates, stores, and analyzes historical draw data, generates number combinations, and evaluates strategies through backtesting.

**Important:** Historical lottery results do not reliably predict future independent draws. The goal is to compare strategies against random selection, not to claim a guaranteed prediction advantage.

## Development Phases

### Phase 1 — Data Foundation
**Status: Mostly Complete**

- [x] Set up Python project structure
- [x] Implement web data fetching and parsing
- [x] Create SQLite database
- [x] Implement duplicate and conflict handling
- [x] Implement basic number frequency analysis
- [x] Implement historical PDF extraction and parsing

### Phase 2 — Data Quality & Validation
**Status: In Progress**

- [x] Validate lottery numbers and draw dates
- [x] Preserve invalid records as errors
- [x] Reconcile PDF records against SQLite data
- [x] Verify duplicate dates in historical data
- [x] Calculate validation pass rate
- [x] Add initial data quality unit test
- [ ] Test empty datasets and edge cases
- [ ] Implement reusable duplicate-date detection
- [ ] Check missing draws against expected draw schedules
- [ ] Generate a consolidated Data Quality Report

**Completion criteria:** Data quality issues can be identified and reported automatically.

### Phase 3 — Reliable ETL Pipeline
**Status: Planned**

- [ ] Integrate extraction, validation, and storage
- [ ] Add structured logging and error handling
- [ ] Support safe, repeatable execution
- [ ] Implement command-line execution
- [ ] Add automated pipeline tests

**Completion criteria:** The pipeline runs reliably with minimal manual intervention.

### Phase 4 — Statistical Analysis
**Status: Planned**

- [ ] Analyze rolling number frequencies
- [ ] Analyze odd/even distributions
- [ ] Analyze number sums and consecutive numbers
- [ ] Analyze number pairs
- [ ] Build reproducible statistical reports and visualizations

**Completion criteria:** Historical patterns can be explored and explained through reproducible analysis.

### Phase 5 — Number Generation Engine
**Status: Planned**

- [ ] Implement random number generation
- [ ] Implement rule-based generation
- [ ] Implement frequency-weighted generation
- [ ] Validate generated combinations
- [ ] Design a common interface for strategy comparison

**Completion criteria:** Multiple strategies generate valid Western 649 combinations.

### Phase 6 — Backtesting & Simulation
**Status: Planned**

- [ ] Implement walk-forward backtesting
- [ ] Prevent future-data leakage
- [ ] Evaluate match counts and prize categories
- [ ] Compare strategies against random baselines
- [ ] Evaluate costs, payouts, and variability

**Completion criteria:** Strategies can be evaluated fairly using historical data.

### Phase 7 — Application & Dashboard
**Status: Planned**

- [ ] Build a Streamlit application
- [ ] Display historical data and quality metrics
- [ ] Visualize statistical analyses
- [ ] Add number generation controls
- [ ] Display backtesting results

**Completion criteria:** Users can explore data, generate combinations, and review strategy performance through a user interface.

### Phase 8 — Deployment & Portfolio
**Status: Planned**

- [ ] Configure automated tests with GitHub Actions
- [ ] Prepare deployment configuration
- [ ] Deploy the application
- [ ] Document installation and usage
- [ ] Finalize README and architecture documentation
- [ ] Exclude copyrighted source files and local databases from public commits

**Completion criteria:** The project is reproducible, documented, and accessible.

---

## Current Focus

**Phase 2 — Data Quality & Validation**

Next task: Step 34-10B — Add pytest coverage for empty datasets in `tests/test_data_quality.py`.

## Development Principles

1. Prioritize data correctness over prediction claims.
2. Keep code modular, testable, and reproducible.
3. Handle invalid data explicitly rather than silently discarding it.
4. Prevent data leakage in strategy evaluation.
5. Update this roadmap when a development phase is completed.