# ----------------------------------------------------------------------------+
#
# Program:    	ENIGMA 
# Description:  Simulation of enigma machine (German encryption device)
# Auteur:       Laurent FERHI
# Version:      0.15
#
# ----------------------------------------------------------------------------+

# --- DEPEDENCIES ------------------------------------------------------------+

import random as rand
from itertools import permutations

# --- FUNCTIONS --------------------------------------------------------------+

def fab_rotor(lex):
    rotor = [i for i in lex]
    rand.shuffle(rotor)
    return rotor

def fab_reflector(lex):
    if len(lex)%2 != 0:
        print("The lexicon should contain even number of elements")
    lst_ind = [i for i in range(len(lex))]
    new_enum = []
    while len(lst_ind) != 0:
        ind_1 = rand.choice(lst_ind)
        lst_ind.remove(ind_1)
        car_1 = [enum[1] for enum in enumerate(lex) if enum[0] == ind_1]
        ind_2 = rand.choice(lst_ind)
        lst_ind.remove(ind_2)
        car_2 = [enum[1] for enum in enumerate(lex) if enum[0] == ind_2]
        new_enum.append((ind_2, car_1[0]))
        new_enum.append((ind_1, car_2[0]))
    reflect = []    
    for i in range(len(new_enum)):
        for enum in new_enum:
            if i == enum[0]:
                reflect.append(enum[1])
    return reflect

def tunning(rotor, ind):
    return rotor[ind:]+rotor[0:ind]

def rotation(rotor ,i):
    return rotor[-i:]+rotor[:len(rotor)-i]

def letter_perm(lex, couple):
    plug = []
    for cara in lex:
        if cara == couple[0]: 
            plug.append(couple[1])
        elif cara == couple[1]: 
            plug.append(couple[0])
        else: 
            plug.append(cara)
    return plug

def plugboard_setup(lex, lst_echange):
    for element in lst_echange:
        lex = letter_perm(lex, element)
    return lex

def rotors_order_setup(cle_rotors, r1, r2, r3):
    lst_rotors = []
    for numero in list(str(cle_rotors)):
        for enum in enumerate([r1, r2, r3]):
            if (enum[0]+1) == int(numero):
                lst_rotors.append(enum[1])
    return lst_rotors

def cypher(lexicon, plugboard, ls_rot, reflector, cara):
    c_1 = plugboard[lexicon.index(cara)]
    c_2 = (ls_rot[0])[lexicon.index(c_1)]
    c_3 = (ls_rot[1])[lexicon.index(c_2)]
    c_4 = (ls_rot[2])[lexicon.index(c_3)]
    c_5 = reflector[lexicon.index(c_4)]
    c_6 = lexicon[(ls_rot[2]).index(c_5)]
    c_7 = lexicon[(ls_rot[1]).index(c_6)]
    c_8 = lexicon[(ls_rot[0]).index(c_7)]
    c_9 = lexicon[plugboard.index(c_8)]
    return c_9

def enigma(txt, lexicon, machine, settings):
    # Plugboard setup
    plugboard = plugboard_setup(lexicon, settings.get("cablage_plugboard"))
    # Initial setup of rotors
    r1 = tunning(machine.get("rotor_1"), settings.get("indice_r1"))
    r2 = tunning(machine.get("rotor_2"), settings.get("indice_r2"))
    r3 = tunning(machine.get("rotor_3"), settings.get("indice_r3"))
    # Rotors order
    lst_rotors = rotors_order_setup(settings.get("ordre_rotors"), r1, r2, r3)
    # Reflector import
    reflector = machine.get("reflector")
    # Removing spaces in text
    ls_txt = list(txt)
    while " " in ls_txt:
        del ls_txt[ls_txt.index(" ")]
    # Text Encryption
    texte_crypt = []
    i = 1
    for lettre in ls_txt:
        crypt_lettre = cypher(lexicon, plugboard, lst_rotors, reflector, lettre)
        texte_crypt.append(crypt_lettre)
        r1 = rotation(r1,1)
        r2 = rotation(r2,2)
        r3 = rotation(r3,3)
        lst_rotors = rotors_order_setup(settings.get("ordre_rotors"), r1, r2, r3)
        i += 1
        # Space every 4 characters
        if (i-1)%4 == 0:
            texte_crypt.append(" ")
    return "".join(texte_crypt)

# --- MAIN -------------------------------------------------------------------+

lexicon = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Machine build
"""
rotor_1 = fab_rotor(lexicon)
rotor_2 = fab_rotor(lexicon)
rotor_3 = fab_rotor(lexicon)

reflector = fab_reflector(lexicon)

print(rotor_1)
print(rotor_2)
print(rotor_3)
print(reflector)
"""

r1 = ['I', 'V', 'R', 'M', 'Z', 'X', 'F', 'H', 'B', 'U', 'Q', 'A', 'T', 
      'N', 'C', 'G', 'O', 'E', 'P', 'Y', 'D', 'L', 'S', 'J', 'K', 'W']
r2 = ['N', 'A', 'R', 'I', 'S', 'Z', 'C', 'K', 'X', 'H', 'L', 'T', 'G', 
      'Y', 'D', 'U', 'Q', 'W', 'O', 'P', 'E', 'M', 'F', 'V', 'J', 'B']
r3 = ['W', 'T', 'X', 'G', 'M', 'P', 'N', 'A', 'D', 'L', 'B', 'Q', 'O', 
      'Z', 'F', 'R', 'U', 'E', 'I', 'V', 'S', 'K', 'J', 'C', 'H', 'Y']

ref = ['Y', 'R', 'U', 'H', 'Q', 'S', 'L', 'D', 'P', 'X', 'N', 'G', 'O', 
       'K', 'M', 'I', 'E', 'B', 'F', 'Z', 'C', 'W', 'V', 'J', 'A', 'T']

machine = {"rotor_1" : r1, "rotor_2" : r2, "rotor_3" : r3, "reflector" : ref}

# Inputs machine setup
i_r1 = 22
i_r2 = 8
i_r3 = 17

ordre = 213

cab_pl = [["A","D"],["V","K"],["E","L"]]

settings = {"indice_r1" : i_r1, "indice_r2" : i_r2, "indice_r3" : i_r3,
            "ordre_rotors" : ordre, "cablage_plugboard" : cab_pl}

# Main program

texte = "HERE IS A CHECK MESSAGE TO ENCRYPT"

cryptage = enigma(texte, lexicon, machine, settings)
print(cryptage)

decryptage = enigma(cryptage, lexicon, machine, settings)
print(decryptage)

###############################################################################