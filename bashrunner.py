from argparse import ArgumentParser
from bashcontainer import ContainerManager, Container
from os.path import expanduser, join

SETTINGS_FILE_NAME = ".bashRunnerSettings.json"

class BashRunner:

    def __init__(self, args, path):
        self.args = args
        self.containerManager = ContainerManager(path)

    # Ejecuta los comandos
    def run(self):
        (command, args) = self.args
        print(command)
        print(args)
        if command.current:
           self.__printCurrentContainer()
        
        elif command.create != None:
           self.__createContainer(command.create) 

    # Imprime el nombre del contenedor actual
    def __printCurrentContainer(self):
        currentContainer = self.containerManager.currentContainer
        if currentContainer == None:
            print("There is currently no container configured")
        else:
            print("Current container %s" % currentContainer)

    # Crea un contenedor vacio
    def __createContainer(self, name):
        if self.containerManager.getContainerIndex(name) != None:
         print("Container already exists %s" % name)
        else:
            newContainer = Container(name, [])
            self.containerManager.containers.append(newContainer)
            self.containerManager.writeSettingsFile()
            print("Container has been created %s" % name)

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

def main():
    args = parseArguments()

    # Genera la ruta del archivo de configuracion
    global SETTINGS_FILE_NAME
    home = expanduser("~")
    settingFilePath = join(home, SETTINGS_FILE_NAME)
    bashRunner = BashRunner(args, settingFilePath)
    bashRunner.run()

if __name__ == "__main__":
    main()
