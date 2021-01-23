# ----------------------------------------------------------------------------+
# Program:    	ENIGMA 
# Description:  Simulation of enigma machine (WWII German encryption device)
# Author:       Laurent FERHI
# Version:      1.1
# ----------------------------------------------------------------------------+

import random as rand

def create_rotor(lex):
    """
    Rotor contains all characters from lexicon in random order
    """
    rotor = [i for i in lex]
    rand.shuffle(rotor)
    return rotor

def create_reflector(lex):
    """
    Reflector contains must be symmetrical (if A->W, then W->A)
    """
    if len(lex)%2 != 0:
        print("The lexicon should contain even number of elements")
    lst_ind = [i for i in range(len(lex))] # list of indexes of the lexicon

    # Pair a letter to another and remember the associated indexes
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

    # Populate the reflector with letters on their imposed indexes
    reflect = []    
    for i in range(len(new_enum)):
        for enum in new_enum:
            if i == enum[0]:
                reflect.append(enum[1])
    return reflect

def tunning(rotor, ind):
    """
    Initial position of the rotor
    """
    return rotor[ind:]+rotor[0:ind]

def rotation(rotor ,i):
    """
    Rotations of i positions
    """
    return rotor[-i:]+rotor[:len(rotor)-i]

def letter_perm(lex, couple):
    """
    Letters permutations of the plugboard
    """
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
    """
    Plugboard initial setup
    """
    for element in lst_echange:
        lex = letter_perm(lex, element)
    return lex

def rotors_order_setup(cle_rotors, r1, r2, r3):
    """
    Rotors initial order
    """
    lst_rotors = []
    for numero in list(str(cle_rotors)):
        for enum in enumerate([r1, r2, r3]):
            if (enum[0]+1) == int(numero):
                lst_rotors.append(enum[1])
    return lst_rotors

def encrypt(lexicon, plugboard, ls_rot, reflector, cara):
    """
    Go through plugboard, rotors, reflector and back again
    """
    step_1 = plugboard[lexicon.index(cara)]
    step_2 = (ls_rot[0])[lexicon.index(step_1)]
    step_3 = (ls_rot[1])[lexicon.index(step_2)]
    step_4 = (ls_rot[2])[lexicon.index(step_3)]
    step_5 = reflector[lexicon.index(step_4)]
    step_6 = lexicon[(ls_rot[2]).index(step_5)]
    step_7 = lexicon[(ls_rot[1]).index(step_6)]
    step_8 = lexicon[(ls_rot[0]).index(step_7)]
    step_9 = lexicon[plugboard.index(step_8)]
    return step_9

def enigma(txt, lexicon, machine, settings):
    """
    Process a text to the enigma machine
    """
    # Plugboard setup
    plugboard = plugboard_setup(lexicon, settings.get("plugboard_settings"))
    # Initial setup of rotors
    r1 = tunning(machine.get("rotor_1"), settings.get("index_r1"))
    r2 = tunning(machine.get("rotor_2"), settings.get("index_r2"))
    r3 = tunning(machine.get("rotor_3"), settings.get("index_r3"))
    # Rotors order
    lst_rotors = rotors_order_setup(settings.get("rotors_order"), r1, r2, r3)
    # Reflector import
    reflector = machine.get("reflector")
    # Removing spaces in text
    ls_txt = list(txt)
    while " " in ls_txt:
        del ls_txt[ls_txt.index(" ")]
    # Text Encryption
    texte_crypt = []
    i = 1 # counter for characters spaces
    c_r1,c_r2= 1,1 # counters for rotor rotation
    for lettre in ls_txt:
        crypt_lettre = encrypt(lexicon, plugboard, lst_rotors, reflector, lettre)
        texte_crypt.append(crypt_lettre)
        # Rotations of the rotor
        r1 = rotation(r1,1)
        c_r1 += 1
        # Case r1 did a full rotation
        if c_r1%(len(lexicon)) == 0:
            c_r1 = 1
            r2 = rotation(r2,1)
            c_r2 += 1
        # Case r2 did a full rotation
        if c_r2%(len(lexicon)) == 0:
            c_r2 = 1
            r3 = rotation(r3,1)
        lst_rotors = rotors_order_setup(settings.get("rotors_order"), r1, r2, r3)
        i += 1
        '''
        # Space every 5 characters (uncomment to activet this feature)
        if (i-1)%5 == 0:
            texte_crypt.append(" ")
        '''
    return "".join(texte_crypt)

# --- MAIN -------------------------------------------------------------------+

if __name__ == "__main__":

    lexicon = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ_.")

    ### Machine build
    """
    rotor_1 = create_rotor(lexicon)
    rotor_2 = create_rotor(lexicon)
    rotor_3 = create_rotor(lexicon)

    reflector = create_reflector(lexicon)

    print(rotor_1)
    print(rotor_2)
    print(rotor_3)
    print(reflector)
    """
    r1 = list('USKFEVIYWZTXAGCQNBMODHLR_PJ.')
    r2 = list('XHVNDCRZQPSB_OKT.LUWGJMEFAIY')
    r3 = list('AWYJLFOV_TIQMZERXUSDKBPNGC.H')
    ref = list('.XF_JCYIHELKNMPOZTWRVUSBGQDA')

    machine = {"rotor_1" : r1, "rotor_2" : r2, "rotor_3" : r3, "reflector" : ref}

    ### Inputs machine setup
    i_r1 = 0
    i_r2 = 8
    i_r3 = 17

    order = 213

    plb_setup = [["A","S"],["V","K"],["E","L"]]

    settings = {"index_r1" : i_r1, "index_r2" : i_r2, "index_r3" : i_r3,
                "rotors_order" : order, "plugboard_settings" : plb_setup}

    ### Text encryption
    text = "CONVOY_HAS_BEEN_SPOTTED_IN_LA_ROCHELLE_SECTOR._ATTACK_AT_ONCE."

    encrypted_text = enigma(text, lexicon, machine, settings)
    print(encrypted_text)

    decrypted_text = enigma(encrypted_text, lexicon, machine, settings)
    print(decrypted_text)
