import yaml

class bcolors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

def parse_yaml(config_path):
    config_file = yaml.safe_load(open(config_path, "r"))
    return config_file

def start_log(config_file):
    print(f"{bcolors.RED}---------------------------------------{bcolors.ENDC}")
    for i in config_file:
        print(f"{bcolors.RED}{i}{bcolors.ENDC} : {bcolors.GREEN}{config_file[i]}{bcolors.ENDC}")
    print(f"{bcolors.RED}---------------------------------------{bcolors.ENDC}")