# Ambrogio

Ambrogio is a framework to create and run procedures.

## Installation

To install Ambrogio, run the following command:

```bash
pip install ambrogio
```

## Usage

### Create a new project

To create a new Ambrogio project run `ambrogio` in CLI and, if no project can be found in the current folder, you will be prompted to confirm you want to create one and to enter its name.

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

To create a new procedure run `ambrogio` in CLI and if no procedure can be found in the project, you will be prompted to confirm you want to create one, otherwise you can select the option to create a new procedure. In both cases, you will be prompted to enter the name and the type of the procedure.

This will create a new file in the `procedures` using the name you entered and the procedure structure from a template.

### Run a procedure

To run a procedure run `ambrogio` in CLI and select the procedure you want to run. You will be prompted to enter the parameters of the procedure if any.

## Procedure types

### Basic procedure

A basic procedure is a procedure that contains a single execution function.

Here is an example of a basic procedure:

```python
from ambrogio.procedures.basic import BasicProcedure
from ambrogio.procedures.param import ProcedureParam

class MyProcedure(BasicProcedure):
    name = 'My Procedure'

    params = [
        ProcedureParam(
            name = 'name',
            type = str,
            value = 'World'
        ),
    ]

    def execute(self):
        name = self.get_param('name').value
        print(f'Hello {name}!')
```

### Step procedure

A step procedure is a procedure that contains multiple execution functions. Each execution function is called a step.

Step can be executed as parallel threads if the `parallel` attribute of the step is set to `True`.

When a step fails, the procedure will stop if the `blocking` attribute of the step is set to `True`.

Here is an example of a step procedure:

```python
from ambrogio.procedures.step import StepProcedure
from ambrogio.procedures.param import ProcedureParam

class MyStepProcedure(StepProcedure):
    name = 'My Step Procedure'

    params = [
        ProcedureParam(
            name = 'final_message',
            type = str,
            value = 'Done!'
        ),
    ]


    def step_1(self):
        print('Step 1')

    def step_2(self):
        print('Step 2')

    def step_3(self):
        print('Step 3')

    def step_4(self):
        print('Step 4')

    def step_5(self):
        print('Step 5')


    def set_up(self):
        self.add_step(self.step_1)
        self.add_step(self.step_2, parallel = True)
        self.add_step(self.step_3, parallel = True)
        self.add_step(self.step_4, parallel = True)
        self.add_step(self.step_5)


    def tear_down(self):
        final_message = self.get_param('final_message').value
        print(final_message)
```

This procedure will execute as follow:

```
                 ┌─ step_2 ─┐
set_up ─ step_1 ─┼─ step_4 ─┼─ step_5 ─ tear_down
                 └─ step_3 ─┘
```

As you can see, the `set_up` and `tear_down` steps are executed sequentially. The `step_1` step is executed sequentially and the `step_2`, `step_3` and `step_4` steps are executed in parallel.

When a sequential step follows some parallel steps, the sequential step will be executed after all the previous parallel steps have finished.