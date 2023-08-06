#Author: Nataly Nuila
#Author Email: nataly.nuila@gmail.com

from random import randrange

class QuantumUniverse():
    """The Quantum Universe Creates all possible states of the "cards"
    that will be utilized in the game.

     Attributes:
     principle (pcp) = Principle quantum number: (a value n, 1-5)
     orbital (oam) = Orbital angular momentum quantum number: (a value l, 0-4, n-1)
     magnetic (mqn) = magnetic quantum number: (ml: -l, ..., 0,....l)
     spin (sqn) = spin quantum number: (ms, +1/2 , -1/2)
     """

    def __init__(self, pcp, oam, mqn, sqn):
        """
        :param pcp: this will be a value from 1-5
        :param oam: this will be a value between 0 - pcp-1
        :param mqn: this will be a value between -oam, .. , +oam
        :param sqn: this will be a value +1/2 or -1/2
        """
        self.principle = pcp
        self.orbital = oam
        self.magnetic = mqn
        self.spin = sqn
        self.validPrinciple = list(range(1, 6))
        self.validSpin = ['spin up', 'spin down']


    def verifyPrinciple(self, principle):
        """
        This method verifies the correctness of the values for principle
        :return: True or false
        """
        if principle in self.validPrinciple:
            return True
        else:
            return False

    def verifyOrbital(self, principle):
        """
        This method verifies the correctness of the values of orbital
        :return: True or False
        """
        n = principle
        # valid orbital number is between 0...n-1
        if self.orbital in list(range(0, n)):
            return True
        else:
            return False

    def verifyMagnetic(self, orbital):
        """
        This method verifies the correctness of the values of the magnetic quantum number
        :return: True or False
        """
        n = orbital
        if self.magnetic in list(range(-n, n+1)):
            return True
        else:
            return False

    def verifySpin(self, spin):
        """
        This method verifies the correctness of the values of the magnetic quantum number
        :return: True or False
         """
        if spin in self.validSpin:
            return True
        else:
            return False

    def getPrinciple(self):
        """
         This method will return Principle value
        :return: principle
        """
        return self.principle

    def getOrbital(self):
        """
         This method will return Orbital value
        :return: orbital
        """
        return self.orbital

    def getMagnetic(self):
        """
         This method will return Magnetic value
        :return: magentic
        """
        return self.magnetic

    def getSpin(self):
        """
         This method will return Spin value
        :return: spin
        """
        return self.spin

    def generateRandomQUniverse(self):
        """
        This method will return a quantum Universe "card"
        that will be utilized to play the quantum universe guessing game.
        :return: will randomnly generate a Quantum Universe "card" to have the player guess
        """
        validQuantumUniverse = False

        #While loop is only done for validation, but should only iterate once
        while(validQuantumUniverse != True):

            #Generate a vlid randomPrinciple value from 0-5
            randomPrinciple = randrange(1, 6)
            #Generate a valid randomOrbital from 0 to randomPrinciple-1
            randomOrbital = randrange(0, randrange(1, 6))

            #randomly choose a magnetic value from -randomOrbital to randomOrbital (included)
            randomMagnetic = randrange(-randomOrbital, randomOrbital+1)

            spinChoice = randrange(0, 2)

            #Randomly choose a spin value:
            randomSpin = self.validSpin[spinChoice]

            #If this outputs to true, all values are valid and we can return the Quantum Universe card

            if (self.verifyPrinciple(randomPrinciple) & self.verifyOrbital(randomPrinciple)
                    & self.verifyMagnetic(randomOrbital) & self.verifySpin(randomSpin)):
                validQuantumUniverse = True
                randomCard = QuantumUniverse(randomPrinciple, randomOrbital, randomMagnetic, randomSpin)

        return randomCard
