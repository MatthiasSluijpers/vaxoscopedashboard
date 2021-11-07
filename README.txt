This package contains all the files to launch the VAXOScopeDashboard. This dashboard is carried out as a result of the Practical Team Project of the course Data Science and Society (INFOMDSS) in the Academic Year 2021-2022. This project contains domain expertise (strategic thinking, understanding context and requirements), computer science (implementing a software artefact), and methodological (mastering methods for analytics) foundations. 

Practical Team Project - Group 16
Last version - 7th of November 2021

VAXOScope Dashboard

This package includes an interactive dashboard and a written report for a Vaccination Dashboard for Campaign Strategists and has as aim to support the stakeholders fighting the COVID-19 pandemic.

FOLDER STRUCTURE
Github: https://github.com/MatthiasSluijpers/vaxoscopedashboard

- Readme.rtf - file which contains the instructions
- Dockerfile - file which launches the docker environment in command / terminal
- docker-compose.yml - file which launches docker image, container, and ports
- index.py - python file which initially runs the dashboard
- requirements.txt - file which contains the used python libraries
- documentation\ - folder with the code descriptions
- report\ - the final report is stored in this folder
- presentations\ - fthe strategy & concept presentation and the final presentation
- figures\ - the used figures are stored here
- apps\ - the initial code (evaluation, modelling, preparation, and visualisation)
- assets\ - javascript & css code for dashboard UI
- data\ - which stores the backup, geometry, predicted, prepared, and raw data

INSTALL MANUAL

1. Install Docker
Please, install docker to launch the VAXOScopeDashboard: https://docs.docker.com/get-docker/

2. Initial Setup
2.1 Open downloaded Github file in Command / Terminal
Enter the following command in the Command / Terminal cd  and include path to the folder with the dowloaded files from GitHub or path to the folder with the files as included in the submitted .zip file

2.2 Build Docker container
Enter the following command in the Command / Terminal docker-compose build

2.3 Launch Docker container
Enter the following command in the Command / Terminal docker-compose up

2.3 Open VAXOScope Dashboard on localhost:5000
Open browser and enter: localhost:5000

BACKGROUND INFORMATION

Python3
https://www.python.org/downloads/

Python Libraries
dash
numpy
pandas
geopandas
dash_bootstrap_components

