# Ambrogio
A simple framework to handle complex scripts.

## Installation

To install Ambrogio, run the following command:

```bash
pip install ambrogio
```

## Usage

To start an Ambrogio project, run the following command:

```bash
ambrogio
```

If no project can be found in the current folder, then you will be prompted to confirm you want to create one and to enter its name.

This will create a new folder with the following structure:

```bash
.
├── ambrogio.ini
└── procedures
```

The `ambrogio.ini` file is the configuration file for the project. It contains the following sections:

```ini
[settings]
procedure_module = procedures
```

The `procedure_module` is the name of the folder where the procedures are stored.

If no procedure can be found in the current project, you will be directly prompted to enter the name and the type of a new procedure. Otherwise, you will be prompted to select the procedure to execute or to create a new one.

## Procedure types

### Basic procedure

A basic procedure is a procedure that contains a single execution function.

### Step procedure

A step procedure is a procedure that contains multiple execution functions. Each execution function is called a step.

Step can be executed in parallel and in sequence.