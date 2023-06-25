# Pathfinder Monster Creator
Project supporting pen & paper RPG game design using machine learning. It offers such functionalities as calculating 
monster's Challenge Rating (CR) based on its properties and generating suggestions how to increase/decrease its CR.

This project was created as the core of the Engineering Thesis titled "Application of machine learning to support 
pen & paper RPG game design".

### Authors
* Paulina Jędrychowska ([github](https://github.com/Paulina100))
* Bogumiła Papiernik ([github](https://github.com/bogumilap))
* Jolanta Śliwa ([github](https://github.com/tunczyk101))

## Table of contents
* [Features](#features)
* [Project Structure](#project-structure)
* [Technologies](#technologies)
* [Setup](#setup)
* [Testing](#testing)


## Features
* calculating Challenge Rating based on given properties
* for given monster and selected different CR generating new sets of monster's properties similar to the original one
* searching for similar monsters in Pathfinder's resources
* suggesting hints of properties that can be added to user's monster based on similar monsters


## Project Structure
* `config`: files with environmental variables
* `docker`: Docker-related files
* `notebooks`: Jupyter Notebooks
* `serving`: app's API and UI
* `test`: tests
* `training`: scripts for creating datasets and training model


## Technologies
* Python 3.10
* Jupyter Notebook
* React.js
* Docker


## Setup
### Prerequisite
To start this application you will need Docker with Docker Compose.

### Starting app
In the `docker` directory there are two Docker images - first, it is necessary to build them:
```shell
docker build . -f docker/Dockerfile_server
docker build . -f docker/Dockerfile_frontend
```

After the build is finished, run command:
```shell
docker-compose up -d
```
Server should now be available on [localhost:8000](http://localhost:8000) and the frontend view - on [localhost:3000](http://localhost:3000/).

Please ensure that your browser has enabled the CSS `:has` selector, especially if you are using Firefox.

### Stopping app
To stop the app, run:
```shell
docker-compose down
```

### Debugging
To ensure the containers are running correctly, you can run:
```shell
docker ps
```

You can also check logs of each of the containers by running:
```shell
docker logs <container> -f
```
where instead of `<container>` type container's name or prefix of its ID.


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
