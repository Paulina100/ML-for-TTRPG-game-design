# Pathfinder Monster Creator
Project supporting pen & paper RPG game design using machine learning. It offers such functionalities as calculating 
monster's Challenge Rating (CR) based on its properties and generating new, similar monsters with a different CR value 
modified by user.

This project was created as the core of the Engineering Thesis titled "Application of machine learning to support 
pen & paper RPG game design".

## Authors
* Paulina Jędrychowska
* Bogumiła Papiernik
* Jolanta Śliwa

## Table of contents
* [Technologies](#technologies)
* [Features](#features)
* [Project Structure](#project-structure)

## Technologies
* Python 3.8 or higher
* Jupyter Notebook

## Features
* calculating Challenge Rating based on given properties
* for given monster and selected different CR generating new sets of monster's properties similar to the original one
* searching for similar monsters in Pathfinder's resources
* suggesting hints of properties that can be added to user's monster based on similar monsters

## Project Structure
* `config`: files with environmental variables
* `docker`: Docker-related files
* `notebooks`: Jupyter Notebooks
* `serving`: app's API
* `test`: tests
* `training`: scripts for creating datasets and training model