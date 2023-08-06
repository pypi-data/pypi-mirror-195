#Author: Nataly Nuila
#Author Email: nataly.nuila@gmail.com


from QuantumUniverse import QuantumUniverse

class QuantumGuessGame():
    """The Quantum Guessing Game allows the user to play a guessing game for the four attributes of an
    electron and will be scored depending on how many they get correct.
         Attributes:
             QuantumUniverse - one retrieved by the user
             QuantumUniverse - one generated randomly by the function
         """

    introPrompt = '=========================================================================================\n' \
                'Welcome to the Quantum Universe Guessing Game! The objective of this game is to choose 4 \n' \
                'attributes of an electron and see if you can objectively guess all 4 attributes. \n' \
                'Let\'s first understand what the four attributes of an electron are: (1) The First is the \n' \
                'Principle Quantum Number - this number denotes the number of shells the electron will exist in.\n' \
                'For our game, we will limit the number of shells to n = 5. (2) Second is the Orbital Angular \n' \
                'Momentum Quantum Number - this number will describe the shape of the given orbital (or probability \n' \
                'space where the electron can exist in the orbital).This number will be dependent on the first so will \n'\
                'range l = 0..4. (3)The third will be the Magnetic Quantum Number which refers to the total number of \n' \
                'orbitals in a subshell and the orientation of these orbitals determined y the magnetic quantum number. \n'\
                'This number will be dependent on the second quantum number which will be between -4,..0..4 . Lastly, the\n'\
                'fourth attribute will be the electric spin number. This is the direction of the spin that the electron is\n'\
                'facing, which are either up or down. Wow. Now your a quantum physics expert! Now let\'s see if you can beat\n'\
                'the game in the quantum guessing game ******** \n' \
                'Let\'s get started!! :D'


    def __init__(self):
        self.emptyUniverse = QuantumUniverse(0,0,0,"down")
        self.randomQuantumUniverse = self.emptyUniverse.generateRandomQUniverse()
        self.userQuantumUniverse = self.obtainUserQuantumCard()

    def obtainUserQuantumCard(self):
        """
        This method introduces the game and begins to obtain a user generated Quantum guessing game.
        :return: A user generated Quantum Universe Card
        """
        inputValidated = False
        userPrinciple = 0
        userOrbital = 0
        userMagnetic = 0
        userSpin = ''

        #Introduce the game to the user
        print(self.introPrompt)
        print('=========================================================================================\n')

        #Four validation while loops to create the Quantum Universe Card:

        #1. Retrieve and validate user principle quantum number:
        userPrinciple = int(input("Please select your principle quantum number, 1 - 5: \n"))

        while inputValidated != True:
            correct = self.randomQuantumUniverse.verifyPrinciple(userPrinciple)
            if correct == False:
                print("I am sorry, that is not a valid number. \n")
                userPrinciple = int(input("Please select your principle quantum number, 1 - 5: \n"))
            else:
                inputValidated = True
        print('=========================================================================================\n')
        #reset inputValidated
        inputValidated = False

        orbital = userPrinciple - 1

        #2. Retrieve and validate user orbital quantum number:
        userOrbital = int(input("Please select your orbital quantum number between 0 and {}: \n".format(orbital)))

        while inputValidated != True:
            correct = self.randomQuantumUniverse.verifyOrbital(userPrinciple)
            if correct == False:
                print("I am sorry, that is not a valid number\n")
                userOrbital = int(input("Please select your orbital quantum number between 0 and {}: \n".format(orbital)))
            else:
                inputValidated = True

        print('=========================================================================================\n')
        # reset inputValidated
        inputValidated = False

        #3. Retrieve and validate user magnetic quantum number:
        userMagnetic = int(input("Please select your orbital quantum number between -{} and {}: \n".format(orbital, orbital)))

        while inputValidated != True:
            correct = self.randomQuantumUniverse.verifyMagnetic(userOrbital)
            if correct == False:
                print("I am sorry, that is not a valid number\n")
                userMagnetic = int(input("Please select your orbital quantum number between -{} and {}: \n".format(orbital, orbital)))
            else:
                inputValidated = True

        print('=========================================================================================\n')
        # reset inputValidated
        inputValidated = False

        #4. Retrieve and validate user spin direction:
        userSpin = str(input("Please select your electron spin direction, either UP or DOWN\n"))
        userSpin.lower()

        while inputValidated != True:
            #Check User Input and Format
            if(userSpin == "up"):
                userSpin = "spin up"
            if(userSpin =="down"):
                userSpin = "spin down"


            correct = self.randomQuantumUniverse.verifySpin(userSpin)

            if correct == False:
                print("I am sorry, that is not a valid input.\n")
                userSpin = str(input("Please select your electron spin direction, either UP or DOWN \n"))
                userSpin.lower()
            else:
                inputValidated = True

        print('=========================================================================================\n')

        print("Thank you for your inputs. Time to see how you did! =D ")

        #Once validated return the Quantum Universe Card to play the game.
        return QuantumUniverse(userPrinciple, userOrbital, userMagnetic, userSpin)


    def initiateGame(self):
        """
        Once the user input and computer input has been generated you can initiate the game and see
        how the user did
        :return: None, prints the score for the user
        """
        correct = 0

        # Organize data from user and randomly generated
        userPrinciple = self.userQuantumUniverse.getPrinciple()
        randomPrinciple = self.randomQuantumUniverse.getPrinciple()
        userOrbital = self.userQuantumUniverse.getOrbital()
        randomOrbital = self.randomQuantumUniverse.getOrbital()
        userMagnetic = self.userQuantumUniverse.getMagnetic()
        randomMagnetic = self.randomQuantumUniverse.getMagnetic()
        userSpin = self.userQuantumUniverse.getSpin()
        randomSpin = self.randomQuantumUniverse.getSpin()

        userList = [userPrinciple, userOrbital, userMagnetic, userSpin]
        randomList = [randomPrinciple, randomOrbital, randomMagnetic, randomSpin]

        print("Let\'s see how you did. :D !\n")

        for i in range(0, 4):
            y = i+1
            print(f"For the {y}th quantum number you inputted was {userList[i]} \n")

            print(f"The computer picked {y}th quantum number that is {randomList[i]} \n")
            if userList[i] == randomList[i]:
                print("Congratulations You got it right! :D !! \n")
                correct += 1
            else:
                print("Sorry, you got it wrong. \n")
            if i != 3:
                print("Let's go to the next round!\n")
                print('=========================================================================================\n')
        print('=========================================================================================\n')
        print("Thank you for Playing the Quantum Guessing Game =)\n")
        print("For this game you got:", correct, "right. Great attempt !\n")
        print("See you next time !")
