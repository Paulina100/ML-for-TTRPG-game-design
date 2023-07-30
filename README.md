# Pathfinder Monster Creator
Project supporting pen & paper RPG game design using machine learning. It offers such functionalities as calculating 
monster's level based on its properties and generating suggestions how to increase/decrease its level.

This project was created as the core of the Engineering Thesis titled "Application of machine learning to support 
pen & paper RPG game design".

### Authors
* Paulina Jędrychowska ([github](https://github.com/Paulina100))
* Bogumiła Papiernik ([github](https://github.com/bogumilap))
* Jolanta Śliwa ([github](https://github.com/tunczyk101))

## Table of contents
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [Project Structure](#project-structure)
* [Testing](#testing)

## Technologies
* Python 3.10
* Jupyter Notebook


## Setup
To install required packages, run

    pip install -r requirements.txt


## Features
* calculating level based on given properties
* for given monster and selected different level generating new sets of monster's properties similar to the original one
* searching for similar monsters in Pathfinder's resources
* suggesting hints of properties that can be added to user's monster based on similar monsters

## Project Structure
* `config`: files with environmental variables
* `docker`: Docker-related files
* `notebooks`: Jupyter Notebooks
* `serving`: app's API
* `test`: tests
* `training`: scripts for creating datasets and training model

## Testing
To run prepared tests in `test` directory using:
* terminal: 
  * enter `test` directory:
  ```shell
  cd test
  ```
  * run `pytest` with test file as argument, e.g.:
  ```shell
  pytest test_creating_dataset.py
  ```

* PyCharm: 
  * run file using run button 
