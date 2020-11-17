import json
from os.path import isfile

# Clase con las etiquetas del archivo de configuracion


class Labels:
    # Campo de los contenedores
    name = "name"
    commands = "commands"
    # Campo del manejador de contenedores
    currentContainer = "currentContainer"
    containers = "containers"

# Controlador del archivo de configuraciones


class ContainerManager:
    def __init__(self, path):
        self.path = path
        self.currentContainer = None
        self.containers = []

        if not self.__initIfNeeded():
            self.__readSettingsFile()
    # **************************************************************************************************
    # Interno

    # Retorna True si fue necesario inicializar
    def __initIfNeeded(self):
        if isfile(self.path):
            return False
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
        dictionary = json.loads(settingsFile.read())
        self.__loadFromDictionary(dictionary)
        settingsFile.close()

    # **************************************************************************************************
    # Interfaz

    # Guarda las configuraciones en el archivo
    def writeSettingsFile(self):
        settingsFile = open(self.path, "w")
        settingsFile.write(self.__toJsonString())
        settingsFile.close()

# Contenedor de comandos


class Container:
    def __init__(self, name, commands=[]):
        self.name = name
        self.commands = commands

    # **************************************************************************************************
    # Interno

    def loadFromDictionary(dictionary):
        name = dictionary[Labels.name]
        commands = dictionary[Labels.commands]
        return Container(name, commands)

    def toDictionary(self):
        return {Labels.name: self.name, Labels.commands: self.commands}

    # **************************************************************************************************
    # Interfaz

    # Agrega un comando a la lista (en el final)
    def addCommand(self, command):
        self.commands.append(command)


c = ContainerManager("/home/stiveun/Desktop/prueba.json")
