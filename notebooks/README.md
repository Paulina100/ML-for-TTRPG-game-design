# "notebooks" directory
This directory stores all Jupyter Notebook files that have been used as the first step of creating this project. It is 
divided into two subdirectories: `data_analysis` and `models`. TODO

## Table of contents
* [characteristics](#characteristics)
  * [melee.ipynb](#meleeipynb)
  * [melee_ranged.ipynb](#melee_rangedipynb)
  * [spells_number.ipynb](#spells_numberipynb)
* [counterfactuals](#counterfactuals)
  * [orcs](#orcs)
    * [counterfactuals_orcs_8.ipynb](#counterfactuals_orcs_8ipynb)
    * [counterfactuals_orcs_13.ipynb](#counterfactuals_orcs_13ipynb)
    * [counterfactuals_orcs_50.ipynb](#counterfactuals_orcs_50ipynb)
  * [counterfactuals_introduction.ipynb](#counterfactuals_introductionipynb)
* [data_analysis](#data_analysis) - contains files used to analyse data about monsters from Pathfinder and roughly estimate which parts 
of it will not be used in finished project. 
  * [abomination_vaults_bestiary_analysis.ipynb](#abomination_vaults_bestiary_analysisipynb)
  * [pathfinder_analysis_of_other_columns.ipynb](#pathfinder_analysis_of_other_columnsipynb)
  * [pathfinder_system_abilities_attributes.ipynb](#pathfinder_system_abilities_attributesipynb)
  * [pathfinder_system_other_columns.ipynb](#pathfinder_system_other_columnsipynb)
  * [pathfinder_items_other_columns.ipynb](#pathfinder_items_other_columnsipynb)
* [models](#models) - contains machine learning models.
  * [sets of features](#sets-of-features) - describes sets of features used to test machine learning models
    * [basic set of features](#basic-set-of-features)
    * [expanded set of features](#expanded-set-of-features)
    * [full set of features](#full-set-of-features)
  * [lightgbm](#lightgbm)
    * [lightgbm_basic.ipynb](#lightgbm_basicipynb)
    * [lightgbm_expanded.ipynb](#lightgbm_expandedipynb)
    * [lightgbm_full.ipynb](#lightgbm_fullipynb)
    * [lightgbm_summary.ipynb](#lightgbm_summaryipynb)
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
  * [all_models_summary.ipynb](#all_models_summaryipynb)

## characteristics

### melee.ipynb

### melee_ranged.ipynb

### spells_number.ipynb

### data_analysis

## counterfactuals

### orcs

#### counterfactuals_orcs_8.ipynb

#### counterfactuals_orcs_13.ipynb

#### counterfactuals_orcs_50.ipynb

### counterfactuals_introduction.ipynb

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

### lightgbm

#### lightgbm_basic.ipynb
LightGBM for predicting monster's level based on basic set of features.

#### lightgbm_expanded.ipynb
LightGBM for predicting monster's level based on expanded set of features.

#### lightgbm_full.ipynb
LightGBM for predicting monster's level based on full set of features.

#### lightgbm_summary.ipynb
Summary of all LightGBM experiments.

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

### all_models_summary.ipynb
Summary of experiments on all models.
