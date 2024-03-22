# Data Analytics for Advertising to Bike Share Users

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/elsdes3/data-insights-for-bikeshare-advertising)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/elsdes3/data-insights-for-bikeshare-advertising/main/notebooks/01-get-data/notebooks/01_get_data.ipynb)
![CI](https://github.com/elsdes3/data-insights-for-bikeshare-advertising/workflows/CI/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/mit)
![OpenSource](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
![prs-welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)

# [Table of Contents](#table-of-contents)

1. [About](#about)
   - [Overview](#overview)
   - [Stakeholder or Business User](#stakeholder)
   - [Intended Audience for Stakeholder](#target-audience)
   - [Project Resources](#project-resources)
2. [Pre-Requisites for Developers](#pre-requisites-for-developers)
3. [Project Organization](#project-organization)

## [About](#about)

### [Overview](#overview)

This project uses Python code to extract insights about bike share ridership in Toronto for a marketing team at Mega Marketers LLC. The team will be launching a digital advertising campaign on the faces of bike share stations across the city in order to grow enrollment in and increase awareness of a local [SCS program](https://en.wikipedia.org/wiki/Continuing_education) for one of their clients (Mega City University, MCU). As part of the campaing, the team is looking to target working professionals and the strong reported uptake of bike sharing among this demographic ([1](https://www.washington.edu/news/2020/05/14/bike-commuting-accelerated-when-bike-share-systems-rolled-into-town/), [2](https://bikesharetoronto.com/faq/)<sup>[1](#myfootnote1)</sup>) has led them to identify bike share users as the target audience for this campaign. The insights extracted here will help the team design a campaign to reach Bike Share Toronto users with this campaign.

<a id="myfootnote1">1</a>: see **ABOUT BIKE SHARE TORONTO** > **What should you use bike share for?**

### [Stakeholder](#stakeholder)

The stakeholder or business user for this project is the marketing team at Mega Marketers LLC.

### [Target Audience](#target-audience)

The audience for the marketing campaign is users of Bike Share Toronto.

### [Project Resources](#project-resources)

See the project documentation [here](https://natural-globe-b44.notion.site/Bike-Share-Toronto-Insights-for-Ads-3ce12f99c1034c4d9d057e43bd97e9de?pvs=4).

## [Pre-Requisites for Developers](#pre-requisites-for-developers)

### [Data](#data)
1. Inside `data/raw/` create the subfolder path `systems/toronto`.
2. Download the following datasets manually and store them in `data/raw/systems/toronto`
   - Toronto bike share ridership data from the [Toronto Open Data portal](https://open.toronto.ca/dataset/bike-share-toronto-ridership-data/) for the following years
     - 2018 (*bikeshare-ridership-2018*)
     - 2019 (*bikeshare-ridership-2019*)
     - 2020 (*bikeshare-ridership-2020*)
     - 2021 (*bikeshare-ridership-2021*)
     - 2022 (*bikeshare-ridership-2022*)
     - 2023 (*bikeshare-ridership-2023*)
   - Census tract boundaries [from Statistics Canada](https://www150.statcan.gc.ca/n1/en/catalogue/92-179-X). For download instructions, see the **Data Retrieval** page in the **Manually Downloaded** section from the project documentation.

## [Project Organization](#project-organization)

    ├── .gitignore                    <- files and folders to be ignored by version control system
    ├── .pre-commit-config.yaml       <- configuration file for pre-commit hooks
    ├── .github
    │   ├── workflows
    │       └── main.yml              <- configuration file for CI build on Github Actions
    ├── LICENSE
    ├── Makefile                      <- Makefile with commands like `make lint` or `make get-data`
    ├── README.md                     <- The top-level README for developers using this project.
    ├── data
    │   ├── processed                 <- The final, canonical data sets for modeling.
    │   └── raw                       <- The original, immutable data dump.
    ├── notebooks                     <- analysis files for all workflow steps
    |   └── 01-get-data               <- single workflow step
    |       ├── .dockerignore         <- files and folders to be ignored by container build
    |       ├── .environment.yml      <- environment configuration file with package metadata
    |       ├── Dockerfile            <- container definition file
    |       └── notebooks             <- Analysis notebooks. Naming convention is `01_<short-description>.ipynb`
    │
    ├── reports                       <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures                   <- Generated graphics and figures to be used in reporting
    │
    ├── docker-compose.yml            <- container configuration for all workflow steps.
    ├── utils.sh                      <- utility to start & clean up container outputs for a single workflow step.
    ├── tox.ini                       <- tox file with settings for running tox; see https://tox.readthedocs.io/en/latest/
    └── src                           <- Source code for use in this project.
        │
        ├── __init__.py               <- Makes `src` a Python module
        └──                           <- Scripts to retrieve and process raw data and run analysis on processed data

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
# data-insights-for-bikeshare-advertising
