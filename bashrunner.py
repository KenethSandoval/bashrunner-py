from argparse import ArgumentParser

def parseArguments():
    parser = ArgumentParser()
    parser.add_argument("--current",
                        action="store_true",
                        help="Displays the name of the current container")
    parser.add_argument("--delete", "-d",
                        nargs="*",
                        help="Delete current container")
    parser.add_argument("--create", "-c",
                        type=str,
                        help="Create a container")
    parser.add_argument("--set", "-s",
                        type=str,
                        help="Configure a container")
    parser.add_argument("--dump",
                        nargs="*",
                        help="View the content a container ")
    parser.add_argument("--list", "-l",
                        action="store_true",
                        help="View the list of container")
    parser.add_argument("--run", "-r",
                        nargs="*",
                        help="Run a container")
    parser.add_argument("--workspace", "-w",
                        type=str) # agregar help
    parser.add_argument("--add", "-a",
                        nargs="*",
                        help="add command to a container")
    return parser.parse_known_args()

args = parseArguments()
print(args)
