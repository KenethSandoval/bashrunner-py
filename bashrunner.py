from argparse import ArgumentParser, REMAINDER
from bashcontainer import ContainerManager, Container
from os.path import expanduser, join

SETTINGS_FILE_NAME = ".bashRunnerSettings.json"


class BashRunner:

    def __init__(self, args, path):
        self.args = args
        self.containerManager = ContainerManager(path)

    # Ejecuta los comandos
    def run(self):
        command = self.args
        print(command)

        if command.current:
            self.__printCurrentContainer()
        elif command.create != None:
            self.__createContainer(command.create)
        elif command.set != None:
            self.__setCurrentContainer(command.set)
        elif command.list:
            self.__getListOfContainer()
        elif command.delete != None:
            self.__deleteContainer(command.delete)

    # Imprime el nombre del contenedor actual
    def __printCurrentContainer(self):
        currentContainer = self.containerManager.currentContainer
        if currentContainer == None:
            print("There is currently no container configured")
        else:
            print("The Current container is %s" % currentContainer)

    # Crea un contenedor vacio
    def __createContainer(self, name):
        if self.containerManager.getContainerIndex(name) != None:
            print("Container already exists %s" % name)
        else:
            newContainer = Container(name, [])
            self.containerManager.containers.append(newContainer)
            self.containerManager.writeSettingsFile()
            print("Container has been created %s" % name)

    # Establece el contendor actual
    def __setCurrentContainer(self, name):
        index = self.containerManager.getContainerIndex(name)
        if index == None:
            print("Cannot configure container %s" % index)
        else:
            self.containerManager.currentContainer = name
            self.containerManager.writeSettingsFile()
            print("The current container is %s" % name)

    # Imprime la lista de contenedores disponibles
    def __getListOfContainer(self):
        containers = self.containerManager.containers
        if len(containers) == 0:
            print("No containers")
        else:
            for container in containers:
                print("- %s" % container.name)

    # Elimina un contenedor
    def __deleteContainer(self, containers):
        if len(containers) == 0:
            if self.containerManager.currentContainer == None:
                containers = []
            else:
                containers = [self.containerManager.currentContainer]

        while len(containers) != 0:
            name = containers.pop(0)
            index = self.containerManager.getContainerIndex(name)

            if index == None:
                print("Container does not exist %s" % name)
            else:
                self.containerManager.containers.pop(index)
                print("Removing... %s" % name)

            if self.containerManager.currentContainer == name:
                self.containerManager.currentContainer = None
                print("Removing with container default %s" % name)
        self.containerManager.writeSettingsFile()
        print("Successfully removed")


# Parser Arguments
#--------------------------------------------------------------------------------------------------------
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
                        type=str)
    parser.add_argument("--add", "-a",
                        nargs=REMAINDER,
                        help="add command to a container")
    return parser.parse_args()

# Main
#--------------------------------------------------------------------------------------------------------


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