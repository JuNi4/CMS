# Library File
import json

# Config file
config_path = ''

def arg_optional():
    return 'optional'
def arg_required():
    return 'required'

required_arg = []
optional_arg = []

args_alt_value = []
args_optionals = []
args_help = []
args_has_config = []
args_config_name = []

# Add argument
def add_arg(arg_name, optional, arg_alt_value = '', arg_missing_text = '', has_config = False, config_name = ''):
    if arg_name in required_arg or arg_name in optional_arg:
        print('Argument already exists')
        return
    if optional == arg_optional():
        optional_arg.append(arg_name)
        args_alt_value.append(arg_alt_value)
        args_optionals.append(arg_alt_value)
        args_help.append(arg_missing_text)
        args_has_config.append(has_config)
        args_config_name.append(config_name)
    elif optional == arg_required():
        required_arg.append(arg_name)
        args_alt_value.append(arg_alt_value)
        args_alt_value.append(arg_alt_value)
        args_help.append(arg_missing_text)
        args_has_config.append(has_config)
        args_config_name.append(config_name)
    else:
        raise 'Invalid argument option at required'

# Check if all required arguments are present, returns True if all are present and False if not
def check_args(argv):
    for o in required_arg:
        # Config
        if not config_path == '':
            f = open(config_path)
            conf = json.loads(f.read())
            f.close()
        # Check
        if o not in argv:
            if args_has_config:
                if args_config_name[required_arg.index(o)] in conf:
                    pass
                else:
                    return False
            else:
                print(args_help[required_arg.index(o)])
            return False
    return True

def get_arg(arg_name, argv):
    if arg_name in required_arg:
        if args_has_config[required_arg.index(arg_name)]:
            f = open(config_path)
            conf = json.loads(f.read())
            f.close()
            if args_config_name[required_arg.index(arg_name)] in conf:
                return conf[args_config_name[required_arg.index(arg_name)]]
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