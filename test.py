import args
import sys
import os

#args.config_path = os.path.dirname(os.path.realpath(__file__)) + '/config.json'

args.add_arg('--help', args.arg_optional(), has_config=True, config_name='test')
if not args.check_args(sys.argv):
    exit()
print(args.get_arg('--help', sys.argv))