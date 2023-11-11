import time
import pyfiglet
from termcolor import colored, cprint

print_yellow = lambda x: cprint(x, 'yellow')
print_red = lambda x: cprint(x, 'red')
print_green = lambda x: cprint(x, 'green')

# Définition du tableau de connexions (Steckerbrett)
def steckerbrett(letter):
    steckerbrett_config = {
        'A': 'N', 'B': 'O', 'C': 'P', 'D': 'Q', 'E': 'R', 'F': 'S', 'G': 'T', 'H': 'U',
        'I': 'V', 'J': 'W', 'K': 'X', 'L': 'Y', 'M': 'Z', 'N': 'A', 'O': 'B', 'P': 'C',
        'Q': 'D', 'R': 'E', 'S': 'F', 'T': 'G', 'U': 'H', 'V': 'I', 'W': 'J', 'X': 'K',
        'Y': 'L', 'Z': 'M'
    }
    return steckerbrett_config.get(letter, letter)

# Définition de la classe Rotor
class Rotor:
    def __init__(self, wiring, notch):
        self.wiring = wiring
        self.notch = notch
        self.position = 0

    def encode(self, letter):
        index = (ord(letter) - ord('A') + self.position) % 26
        return self.wiring[index]

    def encode_reverse(self, letter):
        index = (self.wiring.find(letter) + 26 - self.position) % 26
        return chr(index + ord('A'))

    def step(self):
        self.position = (self.position + 1) % 26
        return self.position == self.notch

# Réflecteur
def reflector(letter):
    reflector_B = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
    index = ord(letter) - ord('A')
    return reflector_B[index]

# Fonction d'encodage pour une lettre
def encode_letter(letter, rotor1, rotor2, rotor3):
    letter = steckerbrett(letter)
    letter = rotor1.encode(letter)
    letter = rotor2.encode(letter)
    letter = rotor3.encode(letter)
    letter = reflector(letter)
    letter = rotor3.encode_reverse(letter)
    letter = rotor2.encode_reverse(letter)
    letter = rotor1.encode_reverse(letter)
    letter = steckerbrett(letter)
    return letter

# Fonction d'encodage pour un message entier
def encode_message(message, rotor1, rotor2, rotor3):
    processed_message = ''
    message = message.upper()

    for letter in message:
        if letter.isalpha():
            if rotor1.step():
                if rotor2.step():
                    rotor3.step()

            encoded_letter = encode_letter(letter, rotor1, rotor2, rotor3)
            processed_message += encoded_letter
        else:
            processed_message += letter

    return processed_message

# Configuration initiale des rotors
rotor_I = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 17)
rotor_II = Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE', 5)
rotor_III = Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO', 22)

# Exemple d'utilisation
if __name__ == "__main__":
    #Affiche le nom de la machine en grand caractere au demarage
    print(colored(pyfiglet.figlet_format("ENIGMA  CLASSIC"),'red'))
    
    # Demander à l'utilisateur de saisir un message    
    print_yellow("1. Chiffrer")
    print_yellow("2. Déchiffrer")
    choice = input("\nChoisissez une option (1 ou 2): ")
    
    # Validation de l'entrée de l'utilisateur pour le choix de l'opération
    if choice not in ('1', '2'):
        print_red("\nChoix invalide. Veuillez entrer '1' pour chiffrer ou '2' pour déchiffrer.\n")
        exit()
    else:
        # Demander à l'utilisateur de saisir un message
        if choice == '1':
            original_message = input(colored("\nEntrez le message à chiffrer: \n","yellow"))
        if choice == '2':
            original_message = input(colored("\nEntrez le message à déchiffrer: \n","yellow"))

    # Configuration des rotors (demandez à l'utilisateur ou fixez-les comme vous le souhaitez)
    # Vous pouvez demander à l'utilisateur de saisir les positions initiales des rotors ici si vous le souhaitez
    rotor_positions = input("Entrez les positions initiales des trois rotors (par exemple, 'A B C' pour les positions 0, 1, 2): ").upper().split()
    if len(rotor_positions) == 3:
        rotor_I.position = ord(rotor_positions[0]) - ord('A')
        rotor_II.position = ord(rotor_positions[1]) - ord('A')
        rotor_III.position = ord(rotor_positions[2]) - ord('A')
    else:
        print("Positions des rotors invalides. Utilisation des positions par défaut 'A B C'.")
        rotor_I.position = 0
        rotor_II.position = 0
        rotor_III.position = 0

    # Encodage et affichage du message codé
    processed_message = encode_message(original_message, rotor_I, rotor_II, rotor_III)
    print(f"Message codé: {processed_message}")

    # Optionnel: démonstration du décodage si nécessaire
    # Si vous voulez montrer le décodage directement après, décommentez le code suivant:
    # print("Décodage du message...")
    rotor_I.position = ord(rotor_positions[0]) - ord('A')
    rotor_II.position = ord(rotor_positions[1]) - ord('A')
    rotor_III.position = ord(rotor_positions[2]) - ord('A')
    
        # Mesurer le temps de début
    start_time = time.time()

    decoded_message = encode_message(processed_message, rotor_I, rotor_II, rotor_III)
    
    # Mesurer le temps de fin
    end_time = time.time()
        
    # Afficher le message traité en fonction du choix
    if choice == '1':
        print_yellow("\nMessage chiffré: ")
        print(processed_message)
        
        #Affiche le nombre de temp que le chiffrement a pris
        print("\n")
        print_green(f"Le chiffrement a pris {(end_time - start_time) * 1000:.2f} millisecondes.")
    else:
        print_yellow("\nMessage déchiffré: ")
        print(processed_message)
        
        #Affiche le nombre de temp que le déchiffrement a pris
        print("\n")
        print_green(f"Le déchiffrement a pris {(end_time - start_time) * 1000:.2f} millisecondes.")
