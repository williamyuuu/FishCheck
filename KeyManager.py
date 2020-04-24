import random


class KeyManager:

    def __init__(self, keys_file = "keys"):
        self.keys_file = keys_file

    def __writeTo(self, input):
        f = open(self.keys_file + ".txt", "w+")
        f.write(input)
        f.close()

    def __appendTo(self, input):
        f = open(self.keys_file + ".txt", "a+")
        f.write(input)
        f.close()

    def __readFrom(self):
        f = open(self.keys_file + ".txt", "r+")
        return f.readlines()

    #public methods

    #places top key to the bottom
    def rotate_key(self):
        keys = self.__readFrom()
        temp = keys.pop(0)
        keys.append(temp)
        self.__writeTo("")
        for x in keys:
            self.__appendTo(x)

    #randomly shuffles all API keys
    def shuffle_key(self):
        keys = self.__readFrom()
        random.shuffle(keys)
        self.__writeTo("")
        for x in keys:
            self.__appendTo(x)

    #returns the first key of the list
    def get_key(self):
        key = self.__readFrom()
        return key[0].rstrip()

    #returns the amount of keys
    def get_key_count(self):
        keys = self.__readFrom()
        return len(keys)

    #returns a random API key fom the list
    def get_random_key(self, range):
        keys = self.__readFrom()
        rand = random.randint(0, range)
        return keys[rand].rstrip()

    #rotates and grab top key
    def get_next_key(self):
        self.rotate_key()
        return self.get_key()


