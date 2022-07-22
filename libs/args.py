# Library File
import json

# Config file
config_path = ''
conf = None

# Help Message
help_message_title = 'Help:'
def help_message():
    # Print Help Message
    print(help_message_title)
    for i in range(len(args_name)):
        config = ''
        alt = ''
        # CHeck if arg has config
        if args_has_config[i]:
            config = '  Config: \'' + args_config_name[i]+ '\''
        # CHeck if arg has alt name
        if args_has_alt[i]:
            alt = '  Alt Name: \'' + args_alt_name[i]+ '\''
        # Print Help Message
        if not args_help_hidden[i]:
            print(' ' + args_name[i] + '' + alt + '' + config + '  -  ' + args_help[i])

def ARG_OPTIONAL():
    return 'optional'
def ARG_REQUIRED():
    return 'required'

# Argument Variables
required_arg = []
optional_arg = []

args_name = []
args_alt_value = []
args_has_alt = []
args_alt_name = []
args_help = []
args_has_config = []
args_config_name = []
args_has_value = []
args_value_type = []
args_help_hidden = []

# Add argument
def add_arg(arg_name, optional, arg_alt_value = '', arg_has_alt = False, arg_alt_name = '', arg_help_text = '', has_config = False, config_name = '', has_value = True, value_type = 'string', hidden = False):
    # Check if Argument already exists
    if arg_name in required_arg or arg_name in optional_arg:
        print('Argument already exists')
        # Exit
        return
    # Check if Argument is optional
    if optional == ARG_OPTIONAL:
        try:
            optional_arg.append(arg_name)
        except Exception as e:
            print(e)
            exit()
    # Check if Argument is required
    elif optional == ARG_REQUIRED:
        try:
            required_arg.append(arg_name)
        except Exception as e:
            print(e)
            exit()
    # Add Argument to Arg Lists
    try:
        args_name.append(arg_name)
        args_alt_value.append(arg_alt_value)
        args_has_alt.append(arg_has_alt)
        args_alt_name.append(arg_alt_name)
        args_help.append(arg_help_text)
        args_has_config.append(has_config)
        args_config_name.append(config_name)
        args_has_value.append(has_value)
        args_value_type.append(value_type)
        args_help_hidden.append(hidden)
    except Exception as e:
        print(e)
        exit()

    # Check if optional is set
    #else:
    #    raise 'Invalid argument option \'optional\' Is required, Example: args.ARG_REQUIRED() or args.ARG_OPTIONAL()'

# Check if all required arguments are present, returns True if all are present and False if not
def check_args(argv, list_missing = False):
    missing_arguments = []
    for o in required_arg:
        # Check if Config
        if not config_path == '':
            # Load Config
            f = open(config_path)
            conf = json.loads(f.read())
            f.close()
            # Check if Arg is Present
            if not args_config_name[args_alt_name.index(o)] in conf:
                # Return False
                missing_arguments.append(o)
        # Check if Arg is Present in Argv
        else:
            if not o in argv and not args_alt_name[args_name.index(o)] in argv:
                # Return False
                missing_arguments.append(o)
    if len(missing_arguments) == 0:
        if list_missing:
            return True, missing_arguments
        else:
            return True
    else:
        if list_missing:
            return False, missing_arguments
        else:
            return False

# Get Argument
def get_arg(arg_name, argv):
    # Get Argument index
    if arg_name in required_arg:
        index = args_name.index(arg_name)
    elif arg_name in optional_arg:
        index = args_name.index(arg_name)
    else:
        raise 'Argument does not exist'
    # Check if Config
    if args_has_config[index] and not config_path == '':
        # Load Config
        f = open(config_path)
        conf = json.loads(f.read())
        f.close()
        # Check if Arg is Present
        if args_config_name[index] in conf:
            # Return Arg
            return conf[args_config_name[index]]
    # Check if Arg is Present in Argv
    else:
        if arg_name in argv or args_alt_name[index] in argv:
            if arg_name in argv:
                x = arg_name
            else:
                x = args_alt_name[index]
            if args_has_value[index]:
                # Check if Argv has at least one more item after the argument
                if len(argv)-1 > argv.index(x) and not argv[argv.index(x)+1] in arg_name and not argv[argv.index(x)+1] in arg_name:
                    # Convert to correct type
                    if args_value_type[index] == 'any':
                        return argv[argv.index(x)+1]
                    elif args_value_type[index] == 'int':
                        return int(argv[argv.index(x) + 1])
                    elif args_value_type[index] == 'float':
                        return float(argv[argv.index(arg_name) + 1])
                    elif args_value_type[index] == 'bool':
                        return True
                elif args_value_type[index] == 'any':
                    return True

# Generate Config File Function
def generate_config_file(config_path):
    # Open Config File
    f = open(config_path, 'w')
    # Write Config File
    config_data = {}
    for i in range(len(args_has_config)):
        if args_config_name[i] == '':
            continue
        if args_value_type[i] == 'any':
            config_data[args_config_name[i]] = ''
        elif args_value_type[i] == 'int':
            config_data[args_config_name[i]] = 0
        elif args_value_type[i] == 'float':
            config_data[args_config_name[i]] = 0.0
        elif args_value_type[i] == 'bool':
            config_data[args_config_name[i]] = False
    f.write(json.dumps(config_data, indent=4))
    # Close Config File
    f.close()