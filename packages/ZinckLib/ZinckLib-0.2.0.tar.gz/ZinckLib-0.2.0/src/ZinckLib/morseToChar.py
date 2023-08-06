def morseToChar(val: str):
    """
    converts a given morse value into the cha value it would represent based on: https://content.instructables.com/F8N/JFGE/KCKIS3RK/F8NJFGEKCKIS3RK.jpg. 

    :param val: The string to convert
    :type val: str

    :return: the converted morse code value or -1 if the provided morse code was not valid
    :rtype: string
    """
    if type(val) is not str:
        raise TypeError('Only strings are allowed')
     
    #tree = "5H4S_V3I_F_U__2E_L_R+__A_P_W_J1!6B=D/X_N_C_K_Y_T7Z_G_Q_M8__O9_0"
    tree = " 5 H 4 S   V 3 I   F   U? _  2 E & L\"  R +.    A   P@  W   J\'1   6-B = D / X   N   C; !K ()Y   T 7 Z  ,G   Q   M:8     O 9   0 "
    pos = int(len(tree)/2)
    i = 0
    testval = val.replace(".", "")
    testval = testval.replace("-", "")
    if testval != "":
        return -1

    while (i <  len(val)):
        if (val[i] == '-'):
            tree = tree[pos:]
            pos = int(len(tree)/2)
            out = tree[pos]
            i = i + 1
        elif(val[i] == '.'):
            tree = tree[:pos]
            pos = int(len(tree)/2)
            out = tree[pos]
            i = i + 1
    if out == " ":
        return -1
    return out
