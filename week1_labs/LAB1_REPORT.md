# Lab 1 Report: Environment Setup and Python Basics

**Student Name:** Mark Joseph C. Orias
<br/>**Student ID:** 231002285
<br/>**Section:** BSCS3A
<br/>**Date:** Wednesday, August 27, 2025

## Environment Setup

### Python Installation
- **Python Version:** 3.13.5
- **Installation Issues:** There are no any problems met in installing python as the lab has already an existing python installed. Similarly creating a virtual environment and activating it on CMD works perfectly fine.
- **Virtual Environment Created:** ✅ cccs106_env_orias

### VS Code Configuration
- **VS Code Version:** 1.103.1 (user setup)
- **Python Extension:** ✅ Installed and configured
- **Interpreter:** ✅ Set to cccs106_env_orias/Scripts/python.exe

### Package Installation
- **Flet Version:** 0.28.3
- **Other Packages:**
<br/>anyio    4.10.0
<br/>certifi  2025.8.3
<br/>flet     0.28.3
<br/>h11      0.16.0
<br/>httpcore 1.0.9
<br/>httpx    0.28.1
<br/>idna     3.10
<br/>oauthlib 3.3.1
<br/>pip      25.2
<br/>repath   0.9.0
<br/>six      1.17.0
<br/>sniffio  1.3.1

## Programs Created

### 1. hello_world.py
- **Status:** ✅ Completed
- **Features:** Student info display, age calculation, system info
- **Notes:** There are no any challenges met in this program. Before running the program, the user must configure the code and replace the student informations and date of birth in the program. Not doing so will print the default string values such as "Your Full Name" and a random student_id.

### 2. basic_calculator.py
- **Status:** ✅ Completed
- **Features:** Basic arithmetic, error handling, min/max calculation
- **Notes:** There are no any challeges met in this program. The program asks the user for user inputs and provides a calculation result based on the arithmetic operations used in the program. ***Exponentiation calculation*** is also added in this program.

## Challenges and Solutions
Following the guide on LeOns, I encountered issues in selecting the default interpreter in Visual Studio Code. My solution to this problem is by manually selecting the interpreter using ***Control+Shift+P*** **> Python: Select Interpreter** and locating it. Another solution is by creating a temporary python file and as long as the created virtual env is in the workspace--it will automatically select it.

## Learning Outcomes

In this laboratory activity, I learned that virtual environments are important whenever we are creating a new project. This way, there are no conflicts in the packages used in every project. Futhermore, there are instances that a project only works on a specified version of the packages.

## Screenshots
<h3>Exercise 1.1 Deliverable</h3>

**Environment Setup**
![Environment Setup](/week1_labs/lab1_screenshots/environment_setup.png)
<h3>Exercise 1.2 Deliverable</h3>

**Visual Studio Code Setup**
![Visual Studio Code Setup](/week1_labs/lab1_screenshots/vscode_setup.png)
<h3>Exercise 1.3 Deliverable</h3>

**Hello World Output**
![Hello World Output](/week1_labs/lab1_screenshots/hello_world_output.png)
**Basic Calculator Output**

This screenshot shows how the program handles error. *<br/>(1) Normal Calculation <br/>(2) Division by Zero <br/>(3) Invalid input*

![Basic Calculator Output](/week1_labs/lab1_screenshots/basic_calculator_output.png)