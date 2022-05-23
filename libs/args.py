# Library File
import json

from defer import return_value

# Config file
config_path = ''
conf = None

def ARG_OPTIONAL():
    return 'optional'
def ARG_REQUIRED():
    return 'required'

# Argument Variables
required_arg = []
optional_arg = []

args_alt_value = []
args_optionals = []
args_help = []
args_has_config = []
args_config_name = []

# Add argument
def add_arg(arg_name, optional, arg_alt_value = '', arg_missing_text = '', has_config = False, config_name = '', has_value = False):
    # Check if Argument already exists
    if arg_name in required_arg or arg_name in optional_arg:
        print('Argument already exists')
        # Exit
        return
    # Check if Argument is optional
    if optional == ARG_OPTIONAL():
        try:
            optional_arg.append(arg_name)
            args_alt_value.append(arg_alt_value)
            args_optionals.append(arg_alt_value)
            args_help.append(arg_missing_text)
            args_has_config.append(has_config)
            args_config_name.append(config_name)
        except Exception as e:
            print(e)
    # Check if Argument is required
    elif optional == ARG_REQUIRED():
        try:
            required_arg.append(arg_name)
            args_alt_value.append(arg_alt_value)
            args_alt_value.append(arg_alt_value)
            args_help.append(arg_missing_text)
            args_has_config.append(has_config)
            args_config_name.append(config_name)
        except Exception as e:
            print(e)

    # Check if optional is set
    else:
        raise 'Invalid argument option \'optional\' Is required, Example: args.ARG_REQUIRED() or args.ARG_OPTIONAL()'

# Check if all required arguments are present, returns True if all are present and False if not
def check_args(argv):
    for o in required_arg:
        # Check if Config
        if not config_path == '':
            # Load Config
            f = open(config_path)
            conf = json.loads(f.read())
            f.close()
        # Check Arguments
        if not o in argv:
            if args_has_config and not config_path == '':
                if not args_config_name[required_arg.index(o)] in conf:
                    return False
            else:
                print(args_help[required_arg.index(o)])
            return False
    return True

# Get Argument
def get_arg(arg_name, argv):
    # Check if Argument is Required
    if arg_name in required_arg:
        # Check if Config
        if args_has_config[required_arg.index(arg_name)] and not config_path == '':
            # Load Config
            f = open(config_path)
            conf = json.loads(f.read())
            f.close()
            # Check if Arg is Present
            if args_config_name[required_arg.index(arg_name)] in conf:
                # Return Arg
                return conf[args_config_name[required_arg.index(arg_name)]]
        # Check if Arg is Present in Argv
        else:
            if arg_name in argv and argv[argv.index(arg_name) + 1] not in required_arg and argv[argv.index(arg_name) + 1] not in optional_arg and argv[argv.index(arg_name) + 1] != '':
                return argv[argv.index(arg_name) + 1]
            else:
                return args_alt_value[required_arg.index(arg_name)]
    elif arg_name in optional_arg:
        if args_has_config[optional_arg.index(arg_name)]:
            f = open(config_path)
            conf = json.loads(f.read())
            f.close()
            if args_config_name[optional_arg.index(arg_name)] in conf:
                return conf[args_config_name[optional_arg.index(arg_name)]]
        else:
            if arg_name in argv and argv[argv.index(arg_name) + 1] not in required_arg and argv[argv.index(arg_name) + 1] not in optional_arg and argv[argv.index(arg_name) + 1] != '':
                return argv[argv.index(arg_name) + 1]
            else:
                return args_alt_value[optional_arg.index(arg_name)]