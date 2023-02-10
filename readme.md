# **Handlr**

## At a Glance
---

Handlr is the implementation of a networking protocol that functions as a chatroom service. The specification for this protocol was defined by Dr. Eugene Styer's CSC 360 course at Eastern Kentucky University during the Spring of 2023.

Handlr was architected and developed by:

* Sijun Kim

* Jarrett Hale

## Table of Contents
---

* [Environment](#environment) - An overview of the expected runtime environment

* [Running Handlr](#running-handlr) - A step by step process of how to run the project

* [Developing](#developing) - A step by step process to get the environment ready for development

* [venv](#venv) - Some context about how to get a Python virtual environment initially set up

* [Git](#git) - Some context about contributing through Github


## Environment
---

Handlr is expected to run in a Windows environment with Python >3.10 installed.

* Windows 10 or 11
* Python >3.10

## Running Handlr
---

* Install Python >3.10: [Download](https://www.python.org/downloads/)

* Clone this repository

    ```powershell 
    git clone https://github.com/JPTheWeatherMan/Handlr
    ```

* Enter the `/Handlr` directory

    ```powershell
    cd /Handlr
    ```

* Create a Virtual Environment to sandbox package installations

    ```powershell
    python -m venv .venv
    ```

* Install dependencies

    ```powershell
    pip install -r requirements.txt
    ```

* Enter the directory of the service you'd like to run

    ```powershell
    cd client
    ```
    
    ```powershell
    cd server
    ```

* Call `Python` and pass it the main filename and the IP address you are hosting from

    ```powershell
    (.venv) C:\Handlr> python main.py XXX.XX.XXX.XX
    ```
## Developing
---

* Install Python >3.10

    [Download](https://www.python.org/downloads/)

* Clone this repository

    ```powershell
    git clone https://github.com/JPTheWeatherMan/Handlr
    ```

* Enter the `/Handlr` directory

    ```powershell 
    cd /Handlr
    ```

* Create a Virtual Environment to sandbox package installations

    ```powershell
    python -m venv .venv
    ```

* Install dependencies

    ```powershell
    python -m pip install -r requirements.txt
    ```

* Activate the Virtual Environment

    ```powershell 
    .venv\Scripts\activate
    ```

    Note: The files created by venv are excluded from committing to version control in `.gitignore`

* Verify that the Virtual Environment is active

    ```powershell
    where python
    ```

    * You should see the virtual environment at the top of the list

        ex:
        ```
        C:\Users\YOUR_USERNAME\Handlr\.venv\Scripts\python.exe
        C:\Users\YOUR_USERNAME\AppData\Local\Programs\Python\Python310\python.exe
        C:\Users\YOUR_USERNAME\AppData\Local\Microsoft\WindowsApps\python.exe
        ```

    * You should NOT see:

        ```
        C:\Users\YOUR_USERNAME\AppData\Local\Programs\Python\Python310\python.exe
        C:\Users\YOUR_USERNAME\AppData\Local\Microsoft\WindowsApps\python.exe
        ```

* While doing development work ensure that you are calling `python /server/main.py` and `python /client/main.py` from the same terminal where you are in an active virtual environment

* When finished with development deactivate the Virtual Environment and if desired delete `.venv`

    ```powershell
    deactivate
    ```

## `venv`
---

- `venv` requires additional setup on Windows due to the default Powershell execution settings.

- To allow for use of `venv` run the command below, then always trust signatures from python developers

    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```

- [Using pip and virtual environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)

- [Default Powershell script execution policies on Windows 10 & 11](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.3)

## Protocol Specification
---

Fill me out!

* Port: 4269

## Git
---

Fill me out!