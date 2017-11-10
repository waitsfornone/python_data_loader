This is a portfolio project that came out of real-life requirements.

1 -- Have a small-footprint remote app that can read data from a database and send a file to an API

2 -- Have the remote API receive files to be stored for processing (processor not in scope)

3 -- The API will store the instructions and manage the remote app's workload

4 -- The remote app will poll at regular intervals a REST API to check for jobs

5 -- The remote app will run each job it receives in a separate process

6 -- The API will have a user interface for creating the Instruction objects (job) and track/maintain their schedule.


Basic Operation:

- The remote machine sends a request to the API

- It receives back a job

- A new process is created to run that job

- The job extracts data and sends it to the API

- The remote machine then waits until the next scheduled run and again looks for a job.


The main goal of this is to require very little interaction on the remote machine with regards to the data transfer. Outside of the schedule for making the initial request, all parts of the pipeline are managed on the server side of the equation.


Short TODO on the basic functionality:

Job control

    -- Need to get each run on a separate PID (threading isn't the correct answer)

    -- Needs to be able to handle X number of jobs coming down (currently only 1)

    -- Needs to call Uploader after each run (not currently uploading automatically)


Data Job

    -- Needs to handle more than PostgreSQL


File Uploader

    -- Should read a single file, not a directory


Multi File Uploader

    -- Create new function for multiple files with proper logging, etc.