# Handlr
## At a Glance
Handlr is the implementation of a networking protocol that functions as a chatroom service. The specification for this protocol was defined by Dr. Eugene Styer's CSC 360 course at Eastern Kentucky University during the Spring of 2023.

Handlr was architected and developed by:
* Sijun Kim
* Jarrett Hale

# Environment
Handlr is expected to run in a Windows environment with Python >3.10 installed.
* Handlr was 
* python?
    - `venv` for a virtual environment so that packages are installed in the project scope and not in the global scope
        - `venv` requires additional setup on Windows due to the default Powershell execution settings.
        - To allow for use of `venv` run the command below, then always trust signatures from python developers
        >`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
        - [Using pip and virtual environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
        - [Powershell execution policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.3)

# Running Handlr
* Clone this repository

&ensp; 
        
  
