# student-app

## Overview

This is a Python application that combines student and room data from two separate JSON files (`students.json` and `rooms.json`). The application assigns each student to their respective room and exports the resulting data structure. The output can be generated in either JSON or XML format via command-line arguments.

The project uses modern Python practices, including `pydantic` for robust data validation and `uv` for efficient dependency management.

## Installation

This project uses `uv` for dependency and environment management. Follow these steps to set up the project:

1.  **Install uv** (if you haven't already):
    ```bash
    curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
    ```
    *(Note: Refer to the official `uv` documentation for installation instructions on your specific operating system.)*

2.  **Navigate to the project directory**:
    ```bash
    cd path/to/your/student-app
    ```

3.  **Install dependencies and the project itself**:
    This command will create a virtual environment, install the required packages (`pydantic` and `dicttoxml`), and install the `student-app` package in editable mode.
    ```bash
    uv pip install -e .
    ```

## Usage

The application is designed to be run from the command line. It requires two input files (`students.json` and `rooms.json`) and an optional output format.

### Command-line Arguments

-   `--students [path]`: The path to the students JSON file. (Required)
-   `--rooms [path]`: The path to the rooms JSON file. (Required)
-   `--format [json|xml]`: The desired output format. Defaults to `json`.

### Examples

**1. Exporting to JSON (Default)**

Run the following command from the project root directory:

```bash
uv run merge-rooms --students students.json --rooms rooms.json