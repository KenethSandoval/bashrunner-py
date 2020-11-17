from argparse import ArgumentParser

def parseArguments():
    parser = ArgumentParser()
    parser.add_argument("--current")   
    return parser.parse_known_args()

args = parseArguments()
