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

class MyProcedure(BasicProcedure):
    name = 'My Procedure'

    def execute(self):
        print('Hello World!')
```

### Step procedure

A step procedure is a procedure that contains multiple execution functions. Each execution function is called a step.

When a step is added to a procedure using the `add_step` method, it can take the following arguments:

- `function`: the function to execute.
- `name`: the name of the step. If not specified, the name of the function will be used.
- `parallel`: if set to `True`, the step will be executed in parallel with the previous step. If set to `False`, the step will be executed sequentially after the previous step. Default value is `False`.
- `blocking`: if set to `True`, the procedure will stop if the step fails. If set to `False`, the procedure will continue to execute the next steps. Default value is `True`.
- `params`: an optional `dict` containing the parameters to pass to the step function.

Here is an example of a step procedure:

```python
from ambrogio.procedures.step import StepProcedure

class MyStepProcedure(StepProcedure):
    name = 'My Step Procedure'


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
        print('Done!')
```

This procedure will execute as follow:

```
                 ┌─ step_2 ─┐
set_up ─ step_1 ─┼─ step_3 ─┼─ step_5 ─ tear_down
                 └─ step_4 ─┘
```

As you can see, `set_up` and `step_1` are executed sequentially, then `step_2`, `step_3` and `step_4` are executed in parallel and finally `step_5` and `tear_down` are executed sequentially.

When a sequential step follows some parallel steps, the sequential step will be executed after all the previous parallel steps have finished.

If add_step is called during a step execution, the step will be appended to the end of the step list.

## Procedure parameters

A procedure parameter is a parameter that can be passed to a procedure when it is executed.

When you create a new procedure, you can define the parameters it can take. Here is an example of a procedure with two parameters:

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
        ProcedureParam(
            name = 'times',
            type = int,
            value = 1
        ),
    ]

    def execute(self):
        name = self.get_param('name').value
        times = self.get_param('times').value
        for i in range(times):
            print(f'Hello {name}!')
```

When you run this procedure, you will be prompted to enter the values of the parameters:

```
Enter the value for 'name' (str): World
Enter the value for 'times' (int): 3
```

Then the procedure will be able to access the values of the parameters:

```python
name = self.get_param('name').value
times = self.get_param('times').value
```

Parameters can be of the following types:

- `bool`
- `int`
- `float`
- `str`
- `Path`(from `pathlib`)

## Procedure prompt and log

You can use the `prompt` and `logger` properties of a procedure to prompt the user and log messages during the execution of the procedure.

You should avoid using the `prompt`during the execution of a parallel step, as it runs in a different thread and the prompt will not work properly.

Here is an example of a procedure that uses the `prompt` and `logger` properties:

```python
from ambrogio.procedures.basic import BasicProcedure

class MyProcedure(BasicProcedure):
    name = 'My Procedure'

    def execute(self):
        name = self.prompt.text('Enter your name:')
        self.logger.info(f'Hello {name}!')
```

Available prompt methods:

- `confirm`: prompt the user to confirm an action. Returns `True` if the user confirms, `False` otherwise.
- `text`: prompt the user to enter a text. Returns the text entered by the user.
- `editor`: prompt the user to enter a text using an editor. Returns the text entered by the user.
- `path`: prompt the user to enter a path. Returns a pathlib `Path` object.
- `password`: prompt the user to enter a password. Returns the password entered by the user.
- `checkbox`: prompt the user to select one or more options from a list passed using the `choices` argument. Returns a list of the selected options.
- `list`: prompt the user to select one option from a list passed using the `choices` argument. Returns the selected option.

`checkbox` and `list` can be used to select from a list of options passed using the `choices` argument. The options can be a list of strings or a list of tuples containing the label and the value of the option. The label is the string displayed to the user and the value is the value returned by the prompt method.

All prompt methods can take the following arguments:

- `default`: the default value to return if the user does not enter anything.
- `validate`: a function that takes the value entered by the user as argument and returns `True` if the value is valid, `False` otherwise.

Available logger methods:

- `debug`: log a debug message.
- `info`: log an info message.
- `warning`: log a warning message.
- `error`: log an error message.
- `critical`: log a critical message.
