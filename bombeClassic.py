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
    
# Configuration initiale des rotors
rotor_I = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 17)
rotor_II = Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE', 5)
rotor_III = Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO', 22)

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
    encoded_message = ''
    message = message.upper()

    for letter in message:
        if letter.isalpha():
            if rotor1.step():
                if rotor2.step():
                    rotor3.step()

            encoded_letter = encode_letter(letter, rotor1, rotor2, rotor3)
            encoded_message += encoded_letter
        else:
            encoded_message += letter

    return encoded_message


# Cette fonction tente de trouver la configuration correcte des rotors
# pour un message chiffré, en supposant que nous connaissons une partie du texte en clair (crib).
def find_enigma_settings(encrypted_message, crib):
    for rotor1_start in range(26):
        for rotor2_start in range(26):
            for rotor3_start in range(26):
                # Réinitialiser les rotors à la position de départ testée
                rotor_I.position = rotor1_start
                rotor_II.position = rotor2_start
                rotor_III.position = rotor3_start
                
                # Décoder le message avec les positions actuelles
                decoded_message = encode_message(encrypted_message, rotor_I, rotor_II, rotor_III)
                
                # Vérifier si le crib est dans le message décodé
                if crib in decoded_message:
                    return (rotor1_start, rotor2_start, rotor3_start, decoded_message)
    
    return None  # Aucune configuration valide trouvée

# Utiliser la fonction find_enigma_settings pour essayer de trouver la configuration correcte
if __name__ == "__main__":
    
    #Affiche le nom de la machine en grand caractere au demarage
    print(colored(pyfiglet.figlet_format("BOMBE CLASSIC"),'red'))
    
    # Message chiffré connu (nous supposons qu'il s'agit d'un message que nous avons capturé)
    encrypted_message = input(colored("\nEntrez le message à chiffrer: \n","yellow"))
    
    # Partie du texte en clair que nous supposons connaître ("crib")
    crib = input(colored("\nEntrez un crible (mot susceptible d'exister dans le message): \n","yellow"))

    # Rechercher les réglages Enigma qui donnent le crib dans le message décodé
    settings = find_enigma_settings(encrypted_message, crib)
    
    # Mesurer le temps de debut de l'execution
    start_time = time.time()
    
    if settings:
        rotor1_start, rotor2_start, rotor3_start, decoded_message = settings
        
        print("\n")
        print_yellow(f"Réglages trouvés: Rotor I: {rotor1_start}, Rotor II: {rotor2_start}, Rotor III: {rotor3_start}")
        print(f"Message décodé: {decoded_message}")    
            # Mesurer le temps de fin d'execution
        end_time = time.time()
    
        #Affiche le nombre de temp que le déchiffrement a pris
        print("\n")
        print_green(f"Le déchiffrement a pris {(end_time - start_time) * 1000:.2f} millisecondes.")
    else:
        print_red("Aucun réglage trouvé qui déchiffre le crib correctement.")