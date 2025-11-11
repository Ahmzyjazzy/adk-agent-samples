# Windows Setup Guide

This guide provides detailed instructions for setting up the Naija Tax Agent development environment on Windows.

## Prerequisites Installation

### 1. Install Make for Windows

Make is required to run the project's build automation commands. There are two ways to install Make on Windows:

#### Option A: Using Chocolatey (Recommended)

1. First, install [Chocolatey](https://chocolatey.org/install) if you haven't already:
   - Open PowerShell as Administrator
   - Run the following command:
     ```powershell
     Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
     ```

2. Install Make using Chocolatey:
   ```powershell
   choco install make
   ```

#### Option B: Using GnuWin32

1. Download the Make installer from [GnuWin32](http://gnuwin32.sourceforge.net/packages/make.htm)
2. Run the installer
3. Add the Make installation path to your system's PATH environment variable:
   - Usually located at `C:\Program Files (x86)\GnuWin32\bin`
   - Open System Properties → Advanced → Environment Variables
   - Add the path to the "Path" variable under System Variables

### 2. Install Python 3.11 or higher

1. Download Python 3.11+ from the [official Python website](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation

### 3. Install uv Package Manager

uv is a fast Python package installer and resolver. Install it using pip:

```powershell
pip install uv
```

## Verifying Installation

Open a new Command Prompt or PowerShell window and verify the installations:

```powershell
# Check Make installation
make --version

# Check Python installation
python --version

# Check uv installation
uv --version
```

## Running the Project

Once everything is installed:

1. Clone the repository:
   ```powershell
   git clone https://github.com/ahmzyjazzy/adk-agent-samples.git
   cd adk-agent-samples
   ```

2. Install dependencies:
   ```powershell
   make install
   ```

3. Start the development server:
   ```powershell
   make dev
   ```

4. Launch the playground interface:
   ```powershell
   make playground
   ```

## Troubleshooting

### Common Issues

1. **'make' is not recognized as an internal or external command**
   - Solution: Ensure Make was installed correctly and added to PATH
   - Try closing and reopening your terminal

2. **Python command not found**
   - Solution: Verify Python is in your PATH
   - Try using `python3` instead of `python`

3. **Permission errors when running commands**
   - Solution: Run your terminal as Administrator

For additional help, please [open an issue](https://github.com/ahmzyjazzy/adk-agent-samples/issues) on our GitHub repository.