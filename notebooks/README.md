# "notebooks" directory

This directory stores all Jupyter Notebook files that have been used as the first step of creating this project. It is 
divided into four subdirectories: `data_analysis`, `items`, `models` and `counterfactuals`.

## Table of contents

* [data_analysis](#data_analysis) - contains files used to analyse data about monsters from Pathfinder and roughly estimate which parts 
of it will not be used in finished project.
    * [abomination_vaults_bestiary_analysis.ipynb](#abomination_vaults_bestiary_analysisipynb)
    * [pathfinder_analysis_of_other_columns.ipynb](#pathfinder_analysis_of_other_columnsipynb)
    * [pathfinder_system_abilities_attributes.ipynb](#pathfinder_system_abilities_attributesipynb)
    * [pathfinder_system_other_columns.ipynb](#pathfinder_system_other_columnsipynb)
    * [pathfinder_items_other_columns.ipynb](#pathfinder_items_other_columnsipynb)
* [items](#items) - contains analysis of chosen monster's items and the way how to extract them while preparing dataset.
    * [melee.ipynb](#meleeipynb)
    * [melee_ranged.ipynb](#melee_rangedipynb)
    * [spells_number.ipynb](#spells_numberipynb)
* [models](#models) - contains machine learning models.
    * [sets of features](#sets-of-features) - describes sets of features used to test machine learning models
        * [basic set of features](#basic-set-of-features)
        * [expanded set of features](#expanded-set-of-features)
        * [full set of features](#full-set-of-features)
    * [linear_regression](#linear_regression)
        * [linear_regression_basic.ipynb](#linear_regression_basicipynb)
        * [linear_regression_expanded.ipynb](#linear_regression_expandedipynb)
        * [linear_regression_full.ipynb](#linear_regression_fullipynb)
        * [linear_regression_summary.ipynb](#linear_regression_summaryipynb)
    * [random_forest](#random_forest)
        * [random_forest_basic.ipynb](#random_forest_basicipynb)
        * [random_forest_expanded.ipynb](#random_forest_expandedipynb)
        * [random_forest_full.ipynb](#random_forest_fullipynb)
        * [random_forest_summary.ipynb](#random_forest_summaryipynb)
    * [lightgbm](#lightgbm)
        * [lightgbm_basic.ipynb](#lightgbm_basicipynb)
        * [lightgbm_expanded.ipynb](#lightgbm_expandedipynb)
        * [lightgbm_full.ipynb](#lightgbm_fullipynb)
        * [lightgbm_summary.ipynb](#lightgbm_summaryipynb)
    * [all_models_summary.ipynb](#all_models_summaryipynb)
* [counterfactuals](#counterfactuals) - contains experiments related to counterfactual explanations
  and `DiCE` - implementation of counterfactual.
  explanations.
    * [orcs](#orcs)
        * [counterfactuals_orcs_basic.ipynb](#counterfactuals_orcs_basicipynb)
        * [counterfactuals_orcs_expanded.ipynb](#counterfactuals_orcs_expandedipynb)
        * [counterfactuals_orcs_full.ipynb](#counterfactuals_orcs_fullipynb)
    * [counterfactuals_introduction.ipynb](#counterfactuals_introductionipynb)

## data_analysis

### abomination_vaults_bestiary_analysis.ipynb
Analysis of `pathfinder_2e_data/abomination-vaults-bestiary.db`.

### pathfinder_analysis_of_other_columns.ipynb

Analysis of some columns from bestiaries.

| column           | usefulness                                                                                                                                                                                                            |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `_id`            | probably not useful                                                                                                                                                                                                   |
| `img`            | not useful                                                                                                                                                                                                            |
| `items`          | analysed in [pathfinder_items_other_columns.ipynb](#pathfinder_items_other_columnsipynb) and ...                                                                                                         |
| `name`           | not useful                                                                                                                                                                                                            |
| `system`         | analysed in [pathfinder_system_abilities_attributes.ipynb](#pathfinder_system_abilities_attributesipynb) and [pathfinder_system_other_columns.ipynb](#pathfinder_system_other_columnsipynb) |
| `type`           | probably useful                                                                                                                                                                                                       |
| `flags`          | not useful                                                                                                                                                                                                            |
| `prototypeToken` | not useful                                                                                                                                                                                                            |


### pathfinder_system_abilities_attributes.ipynb
Analysis of columns `system/abilities` and `system/attributes` from bestiaries.

#### `system/abilities`

| column | usefulness |
|--------|------------|
| `cha`  | useful     |
| `con`  | useful     |
| `dex`  | useful     |
| `int`  | useful     |
| `str`  | useful     |
| `wis`  | useful     |


Each of above subcolumns stores a dict with key `mod` and a numerical value.

#### `system/attributes`

| column        | usefulness      |
|---------------|-----------------|
| `ac`          | useful          |
| `allSaves`    | not useful      |
| `hp`          | useful          |
| `immunities`  | could be useful |
| `initiative`  | not useful      |
| `perception`  | probably useful |
| `speed`       | probably useful |
| `weaknesses`  | probably useful |
| `resistances` | could be useful |
| `hardness`    | could be useful |
| `adjustment`  | not useful      |


### pathfinder_system_other_columns.ipynb

Analysis of columns `system/details`, `system/resources`, `system/saves`, `system/traits` and `system/schema` from bestiaries.

#### `system/details`

| column         | usefulness                               |
|----------------|------------------------------------------|
| `alignment`    | could be useful (but not for regression) |
| `blurb`        | not useful                               |
| `creatureType` | probably useful (but not for regression) |
| `level`        | useful (monster's level)      |
| `privateNotes` | not useful                               |
| `publicNotes`  | not useful                               |
| `source`       | useful (name of monster's bestiary)      |

#### `system/resources`

| column  | usefulness      |
|---------|-----------------|
| `focus` | could be useful |

#### `system/saves`

| column      | usefulness |
|-------------|------------|
| `fortitude` | useful     |
| `reflex`    | useful     |
| `will`      | useful     |

#### `system/traits`

| column      | usefulness                                   |
|-------------|----------------------------------------------|
| `languages` | probably not useful                          |
| `rarity`    | could be useful (but not for regression)     |
| `senses`    | probably not useful (but not for regression) |
| `size`      | could be useful (but not for regression)     |
| `value`     | could be useful (but not for regression)     |
| `attitude`  | could be useful (but not for regression)     |

#### `system/schema`

| column          | usefulness          |
|-----------------|---------------------|
| `version`       | probably not useful |
| `lastMigration` | probably not useful |

### pathfinder_items_other_columns.ipynb

Analysis of columns `items/_id`, `items/img`, `items/name`, `items/sort`, `items/type`, `items/flags`


| column  | usefulness |
|---------|------------|
| `_id`   | not useful |
| `img`   | not useful |
| `name`  | not useful |
| `sort`  | not useful |
| `type`  | useful     |
| `flags` | not useful |


## items

### melee.ipynb

Analyse of melee items which `weaponType` is `melee` and how to extract `melee max bonus` and `average melee damage`

### melee_ranged.ipynb

Analyse of melee items which `weaponType` is `ranged` and how to extract `ranged max bonus` and `average ranged damage`

### spells_number.ipynb

Analyse of spells items and how to count spells with given level for each monster.


## models

### Sets of features

Models were tested with 3 different sets of features,
referred to as: basic, expanded and full.

#### Basic set of features

* abilities:
    * cha
    * con
    * dex
    * int
    * str
    * wis
* attributes
    * hp
    * ac

#### Expanded set of features

* abilities:
    * cha
    * con
    * dex
    * int
    * str
    * wis
* attributes
    * hp
    * ac
    * perception
* saves
    * fortitude
    * reflex
    * will
* resources
    * focus

#### Full set of features

System:

* abilities:
    * cha
    * con
    * dex
    * int
    * str
    * wis
* attributes
    * hp
    * ac
    * perception
    * speed (*land speed*)
        * other speeds: fly, climb, swim
    * num immunities
    * resistances: fire, cold, electricity, acid, piercing, slashing, physical, bludgeoning, mental, poison, all-damage
    * weaknesses: cold-iron, good, fire, cold, area-damage, splash-damage, evil, slashing
* saves
    * fortitude
    * reflex
    * will
* resources
    * focus

Items

* items
    * melee
    * ranged
    * spells nr
    
### linear_regression

#### linear_regression_basic.ipynb

Linear regression for predicting monster's level based on basic set of features.

#### linear_regression_expanded.ipynb

Linear regression for predicting monster's level based on expanded set of features.

#### linear_regression_full.ipynb

Linear regression for predicting monster's level based on full set of features.

#### linear_regression_summary.ipynb

Summary of all linear regression experiments.

### random_forest

#### random_forest_basic.ipynb

Random forest for predicting monster's level based on basic set of features.

#### random_forest_expanded.ipynb

Random forest for predicting monster's level based on expanded set of features.

#### random_forest_full.ipynb

Random forest for predicting monster's level based on full set of features.

#### random_forest_summary.ipynb

Summary of all random forest experiments.

### lightgbm

#### lightgbm_basic.ipynb

LightGBM for predicting monster's level based on basic set of features.

#### lightgbm_expanded.ipynb

LightGBM for predicting monster's level based on expanded set of features.

#### lightgbm_full.ipynb

LightGBM for predicting monster's level based on full set of features.

#### lightgbm_summary.ipynb

Summary of all LightGBM experiments.

### all_models_summary.ipynb

Summary of experiments on all models.


## counterfactuals

### orcs

Analysis of the counterfactual explanations using 3 types of orcs:

* Orc Brute - level 0
* Orc Warrior - level 1
* Orc Warchief - level 2

Counterfactuals for orcs were generated for LightGBM models and 3 different sets of features, referred to as: basic, expanded and full.
([sets of features](#sets-of-features)).

For each orc there were generated counterfactuals for both levels' of remaining 2 monsters.
Results were compared to original monster and the other orc with requested level.

#### counterfactuals_orcs_basic.ipynb

Analysis of counterfactual explanations for orcs using basic set.

#### counterfactuals_orcs_expanded.ipynb

Analysis of counterfactual explanations for orcs using expanded set.

#### counterfactuals_orcs_full.ipynb

Analysis of counterfactual explanations for orcs using full set.

### counterfactuals_introduction.ipynb

Introduction to `DiCE` using bestiaries.

