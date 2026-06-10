# malariafit

Shared research code calibrating a Ross-Macdonald malaria transmission model to
cross-sectional prevalence data for a single country.

## Installation

This project uses [renv](https://rstudio.github.io/renv/). After cloning:

```r
renv::restore()
```

## Usage

```r
source("R/model.R")
fit <- fit_prevalence(data = read.csv("prevalence.csv"))
```

## Structure

- `R/model.R` — transmission model and calibration functions
