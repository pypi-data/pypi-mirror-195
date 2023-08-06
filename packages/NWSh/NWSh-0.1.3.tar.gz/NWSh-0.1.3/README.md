# NWShDev
This package provides a set of tools to facilitate the development of the [NWSh](https://github.com/NWSOFT-ORG/NWSh) shell.
# API Documentation
## `NWSh.arguments`
> Provides a set of functions to ask for arguments.
### `NWSh.arguments.Arguments`
> A class to ask for arguments.
#### `NWSh.arguments.Arguments.ask_argument(name, description, type)`
> Asks for arguments, with a name, a description and a type.\
Note: The type can be `string`, `int`, `float`. Conversion is done automatically.
#### `NWSh.arguments.Arguments.get_argument(name)`
> Returns the value of the argument with the given name.
> If the argument is not found, returns `None` and prints an error message.
## `NWSh.commands`
> Provides a set of functions to create commands.
### `NWSh.commands.register_command_subsystem(subsystem, command, func)`
> Registers a command in a subsystem.
> Arguments are not supported yet
### `NWSh.commands.register_command_system(system, command, func)`
> Same as `NWSh.commands.register_command_subsystem`, but for the `System` class.
## `NWSh.printing`
> Provides a set of functions to print messages.
### `NWSh.printing.print_error(subsystem, message)`
> Prints an error message.
### `NWSh.printing.print_info(subsystem, message)`
> Prints an info message.
### `NWSh.printing.print_warning(subsystem, message)`
> Prints a warning message.
### `NWSh.printing.print_result(subsystem, message)`
> Prints a result message.