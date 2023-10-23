# "notebooks" directory
This directory stores all Jupyter Notebook files that have been used as the first step of creating this project. It is 
divided into two subdirectories: `data_analysis` and `models`.

## Table of contents
* `data_analysis` - contains files used to analyse data about monsters from Pathfinder and roughly estimate which parts 
of it will not be used in finished project. 
  * [abomination_vaults_bestiary_analysis.ipynb](#data_analysisabomination_vaults_bestiary_analysisipynb)
  * [pathfinder_analysis_of_other_columns.ipynb](#data_analysispathfinder_analysis_of_other_columnsipynb)
  * [pathfinder_system_abilities_attributes.ipynb](#data_analysispathfinder_system_abilities_attributesipynb)
  * [pathfinder_system_other_columns.ipynb](#data_analysispathfinder_system_other_columnsipynb)
  * [pathfinder_items_other_columns.ipynb](#data_analysispathfinder_items_other_columnsipynb)
* `models` - contains machine learning models.
  * [system_linear_regression.ipynb](#modelssystem_linear_regressionipynb)
  * [system_random_forest.ipynb](#modelssystem_random_forestipynb)
  * [LightGBM.ipynb](#modelslightgbmipynb)


## data_analysis/abomination_vaults_bestiary_analysis.ipynb
Analysis of `pathfinder_2e_data/abomination-vaults-bestiary.db`.

## data_analysis/pathfinder_analysis_of_other_columns.ipynb
Analysis of some columns from bestiaries.

| column           | usefulness                                                                                                                                                                                                            |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `_id`            | probably not useful                                                                                                                                                                                                   |
| `img`            | not useful                                                                                                                                                                                                            |
| `items`          | analysed in [pathfinder_items_other_columns.ipynb](#data_analysispathfinder_items_other_columnsipynb) and ...                                                                                                         |
| `name`           | not useful                                                                                                                                                                                                            |
| `system`         | analysed in [pathfinder_system_abilities_attributes.ipynb](#data_analysispathfinder_system_abilities_attributesipynb) and [pathfinder_system_other_columns.ipynb](#data_analysispathfinder_system_other_columnsipynb) |
| `type`           | probably useful                                                                                                                                                                                                       |
| `flags`          | not useful                                                                                                                                                                                                            |
| `prototypeToken` | not useful                                                                                                                                                                                                            |


## data_analysis/pathfinder_system_abilities_attributes.ipynb
Analysis of columns `system/abilities` and `system/attributes` from bestiaries.

### `system/abilities`
| column | usefulness |
|--------|------------|
| `cha`  | useful     |
| `con`  | useful     |
| `dex`  | useful     |
| `int`  | useful     |
| `str`  | useful     |
| `wis`  | useful     |


Each of above subcolumns stores a dict with key `mod` and a numerical value. 

### `system/attributes`

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


## data_analysis/pathfinder_system_other_columns.ipynb
Analysis of columns `system/details`, `system/resources`, `system/saves`, `system/traits` and `system/schema` from bestiaries.

### `system/details`
| column         | usefulness                               |
|----------------|------------------------------------------|
| `alignment`    | could be useful (but not for regression) |
| `blurb`        | not useful                               |
| `creatureType` | probably useful (but not for regression) |
| `level`        | useful (monster's level)      |
| `privateNotes` | not useful                               |
| `publicNotes`  | not useful                               |
| `source`       | useful (name of monster's bestiary)      |

### `system/resources`
| column  | usefulness      |
|---------|-----------------|
| `focus` | could be useful |

### `system/saves`
| column      | usefulness |
|-------------|------------|
| `fortitude` | useful     |
| `reflex`    | useful     |
| `will`      | useful     |

### `system/traits`
| column      | usefulness                                   |
|-------------|----------------------------------------------|
| `languages` | probably not useful                          |
| `rarity`    | could be useful (but not for regression)     |
| `senses`    | probably not useful (but not for regression) |
| `size`      | could be useful (but not for regression)     |
| `value`     | could be useful (but not for regression)     |
| `attitude`  | could be useful (but not for regression)     |

### `system/schema`
| column          | usefulness          |
|-----------------|---------------------|
| `version`       | probably not useful |
| `lastMigration` | probably not useful |

## data_analysis/pathfinder_items_other_columns.ipynb
Analysis of columns `items/_id`, `items/img`, `items/name`, `items/sort`, `items/type`, `items/flags`


| column  | usefulness |
|---------|------------|
| `_id`   | not useful |
| `img`   | not useful |
| `name`  | not useful |
| `sort`  | not useful |
| `type`  | useful     |
| `flags` | not useful |




## models/system_linear_regression.ipynb
Linear regression for predicting monster's level (stored originally in `system/details/level`) based on 
`system/abilities`, `system/attributes/hp` and `system/attributes/ac`.

## models/system_random_forest.ipynb
Random forest for predicting monster's level (stored originally in `system/details/level`) based on 
`system/abilities`, `system/attributes/hp` and `system/attributes/ac`.

## models/LightGBM.ipynb
LightGBM for predicting monster's level (stored originally in `system/details/level`) based on 
`system/abilities`, `system/attributes/hp`, `system/attributes/ac`, `system/attributes/perception`,
`system/saves` and `system/resources/focus`.
