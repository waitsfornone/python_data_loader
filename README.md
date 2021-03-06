This is a portfolio project that came out of real-life requirements.

1. Have a small-footprint remote app that can read data from a database and send a file to an API
2. Have the remote API receive files to be stored for processing (processor not in scope)
3. The API will store the instructions and manage the remote app's workload
4. The remote app will poll at regular intervals a REST API to check for jobs
5. The remote app will run each job it receives in a separate process
6. The API will have a user interface for creating the Instruction objects (job) and track/maintain their schedule.


# Basic Operation:

* The remote machine sends a request to the API
* It receives back a job
* A new process is created to run that job
* The job extracts data and sends it to the API
* The remote machine then waits until the next scheduled run and again looks for a job.


The main goal of this is to require very little interaction on the remote machine with regards to the data transfer. Outside of the schedule for making the initial request, all parts of the pipeline are managed on the server side of the equation.

## NOTE: The sample dataset is stored in git-lfs and that extension is needed to clone the repo

# HOW TO RUN:

This repo provides the remote data extract code, and a sample server to check it out with. 

* The Flask sample server is found in `sample_server/app.py`
* The Flask database is in `data/instructions.db`
* The sample dataset is in `data/sample_data.db`

To start up the Scheduler and watch it run, execute `python foreman.py`

Also, each piece can be run separately

* Scheduled Job -- `python data_loader.py`
* Data Extract -- `python data_job.py`
* File Upload -- `python file_uploader.py`