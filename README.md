# Ambrogio
A simple framework to handle complex scripts.

## Installation

To install Ambrogio, run the following command:

```bash
pip install ambrogio
```

## Usage

### Create a new project

To create a new project, run the following command:

```bash
ambrogio init
```

You will be prompted to enter the name of the project.

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

### Create a new procedure

To create a new procedure, run the following command:

```bash
ambrogio create
```

You will be prompted to enter the name and the type of the procedure. The procedure will be created in the `procedures` folder.

### Run a procedure

To run a procedure, run the following command:

```bash
ambrogio start
```

You will be prompted to select the procedure to execute.

## Procedure types

### Basic procedure

A basic procedure is a procedure that contains a single execution function.

### Step procedure

A step procedure is a procedure that contains multiple execution functions. Each execution function is called a step.

Step can be executed in parallel and in sequence.