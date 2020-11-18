import json
from os.path import isfile
from sys import exit

# Labels
#--------------------------------------------------------------------------------------------------------
class Labels:
    # Campo de los contenedores
    name = "name"
    commands = "commands"
    # Campo del manejador de contenedores
    currentContainer = "currentContainer"
    containers = "containers"

# Container Manager
#--------------------------------------------------------------------------------------------------------

class ContainerManager:
    def __init__(self, path):
        if path == None or len(path) == 0:
            print("Error...")
            exit()

        self.path = path
        self.currentContainer = None
        self.containers = []

        if not self.__initIfNeeded():
            self.__readSettingsFile()

    # Internal
    # --------------------------------------------------------------------------------------------------------

    # Retorna True si fue necesario inicializar
    def __initIfNeeded(self):
        if isfile(self.path):
            return False
        print("Creando archivo de configuraciones del Container manager")
        self.writeSettingsFile()
        return True

    # Lee la informacion desde un diccionario
    def __loadFromDictionary(self, dictionary):
        self.currentContainer = dictionary[Labels.currentContainer]
        containers = dictionary[Labels.containers]
        self.containers = [
            Container.loadFromDictionary(x) for x in containers]

   # Convierte los datos de la clase en un diccionario
    def __toDictionary(self):
        return {
            Labels.currentContainer: self.currentContainer,
            Labels.containers: [x.toDictionary() for x in self.containers]
        }

    # Convierte la informacion de la clase en un diccionario
    def __toJsonString(self):
        return json.dumps(self.__toDictionary(), indent=4)

    # Lee el archivo de configuraciones
    def __readSettingsFile(self):
        settingsFile = open(self.path, "r")
        try:
            dictionary = json.loads(settingsFile.read())
            self.__loadFromDictionary(dictionary)
        except:
            print("El archivo de configuración del Container Manager esta corrupto")
            exit()
        settingsFile.close()

    # Interfaz
    #--------------------------------------------------------------------------------------------------------

    # Guarda las configuraciones en el archivo
    def writeSettingsFile(self):
        settingsFile = open(self.path, "w")
        settingsFile.write(self.__toJsonString())
        settingsFile.close()

    # Retorn el indice de un contenedor dado su nombre si es posible.
    # defualt: None
    def getContainerIndex(self, containerName):
        for (i, x) in enumerate(self.containers):
            if x.name == containerName:
                return i
        return None

# Command Container
#--------------------------------------------------------------------------------------------------------
class Container:
    def __init__(self, name, commands=[]):
        self.name = name
        self.commands = commands

    # Interfaz
    #--------------------------------------------------------------------------------------------------------

    def loadFromDictionary(dictionary):
        name = dictionary[Labels.name]
        commands = dictionary[Labels.commands]
        return Container(name, commands)

    def toDictionary(self):
        return {Labels.name: self.name, Labels.commands: self.commands}

    # Agrega un comando a la lista (en el final)

    def addCommand(self, command):
        self.commands.append(command)


c = ContainerManager("/home/stiveun/Desktop/prueba.json")
