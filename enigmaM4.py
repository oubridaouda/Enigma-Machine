import time
import pyfiglet
from termcolor import colored, cprint

print_yellow = lambda x: cprint(x, 'yellow')
print_red = lambda x: cprint(x, 'red')
print_green = lambda x: cprint(x, 'green')

# ... (Les classes et fonctions précédentes restent inchangées)

class EnigmaM4:
    def __init__(self, rotor_I, rotor_II, rotor_III, rotor_IV, reflector, plugboard_settings):
        self.rotor_I = rotor_I
        self.rotor_II = rotor_II
        self.rotor_III = rotor_III
        self.rotor_IV = rotor_IV
        self.reflector = reflector
        self.plugboard_settings = plugboard_settings

    def encode(self, message):
        encoded = ''
        for letter in message.upper():
            if letter.isalpha():
                # Passage à travers le tableau de connexions
                letter = self.plugboard_settings.get(letter, letter)
                
                # Passage à travers les rotors (de droite à gauche)
                letter = self.rotor_IV.encode(letter)
                letter = self.rotor_III.encode(letter)
                letter = self.rotor_II.encode(letter)
                letter = self.rotor_I.encode(letter)
                
                # Réflecteur
                letter = self.reflector[ord(letter) - ord('A')]
                
                # Passage à travers les rotors (de gauche à droite, en inversant le processus)
                letter = self.rotor_I.encode_reverse(letter)
                letter = self.rotor_II.encode_reverse(letter)
                letter = self.rotor_III.encode_reverse(letter)
                letter = self.rotor_IV.encode_reverse(letter)
                
                # Retour à travers le tableau de connexions
                letter = self.plugboard_settings.get(letter, letter)
                encoded += letter
                
                # Rotation des rotors après chaque clé
                if self.rotor_III.step():  # Si le rotor III a atteint son notch, le II tournera avec le III lors du prochain appui
                    if self.rotor_II.step():  # Si le rotor II atteint son notch, le I tournera également lors du prochain appui
                        self.rotor_I.step()
            else:
                encoded += letter  # Espace et ponctuation restent inchangés
        return encoded

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
    
# Configuration initiale des rotors et du réflecteur
rotor_I = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 17)  # Rotor I
rotor_II = Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE', 5)   # Rotor II
rotor_III = Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO', 22) # Rotor III
rotor_IV = Rotor('ESOVPZJAYQUIRHXLNFTGKDCMWB', 10)  # Rotor "thin" or Beta rotor for M4
reflector_B_thin = 'ENKQAUYWJICOPBLMDXZVFTHRGS'      # Reflector "thin" B for M4

# Simulation d'un tableau de connexions simplifié
plugboard_settings = {
    'A': 'N', 'N': 'A', 'B': 'O', 'O': 'B', 'C': 'P', 'P': 'C', 'D': 'Q', 'Q': 'D',
    'E': 'R', 'R': 'E', 'F': 'S', 'S': 'F', 'G': 'T', 'T': 'G', 'H': 'U', 'U': 'H',
    'I': 'V', 'V': 'I', 'J': 'W', 'W': 'J', 'K': 'X', 'X': 'K', 'L': 'Y', 'Y': 'L',
    'M': 'Z', 'Z': 'M'
}

# Création de la machine Enigma M4
enigma_M4 = EnigmaM4(rotor_I, rotor_II, rotor_III, rotor_IV, reflector_B_thin, plugboard_settings)

# Exemple d'utilisation
if __name__ == "__main__":
    
    print(colored(pyfiglet.figlet_format("ENIGMA M 4"),'red'))
    
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
    
    # Saisir les positions initiales des rotors pour la machine Enigma M4
    rotor_positions = input(colored("\nEntrez les positions initiales des quatre rotors (par exemple, 'A B C D'): \n","yellow")).upper().split()
    if len(rotor_positions) == 4:
        rotor_IV.position = ord(rotor_positions[0]) - ord('A')
        rotor_III.position = ord(rotor_positions[1]) - ord('A')
        rotor_II.position = ord(rotor_positions[2]) - ord('A')
        rotor_I.position = ord(rotor_positions[3]) - ord('A')
    else:
        print_red("\nPositions des rotors invalides. Utilisation des positions par défaut 'A B C D'.")
        exit()

    # Mesurer le temps de début
    start_time = time.time()

    # Chiffrer le message
    processed_message = enigma_M4.encode(original_message)
    
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