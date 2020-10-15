def P10(text_to_permute):
    pBox = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    result = ""
    for n in pBox:
        result = result + text_to_permute[n - 1]
        
    return result

def P8(text_to_permute):
    pBox = [6, 3, 7, 4, 8, 5, 10, 9]
    result = ""
    for n in pBox:
        result = result + text_to_permute[n - 1]
        
    return result

def P4(text_to_permute):
    pBox = [2, 4, 3, 1]
    result = ""
    for n in pBox:
        result = result + text_to_permute[n - 1]
        
    return result

def L_Shift(text_to_shift,offset):
    return text_to_shift[offset:] + text_to_shift[:offset]

def round_key_generator(key):
    
    key = P10(key)
    LH = key[:5]
    RH = key[5:]
    combined = L_Shift(LH,1) + L_Shift(RH,1)
    k1 = P8(combined)
    LH = combined[:5]
    RH = combined[5:]
    combined = L_Shift(LH,2) + L_Shift(RH,2)
    k2 = P8(combined)
    
    return [k1,k2]

# print(round_key_generator("1010000010"))
# ['10100100', '01000011']

def IP8(text_to_permute):
    pBox = [2, 6, 3, 1, 4, 8, 5, 7]
    result = ""
    for n in pBox:
        result = result + text_to_permute[n - 1]
        
    return result

def IP8_inv(text_to_permute):
    pBox = [4, 1, 3, 5, 7, 2, 8, 6]
    result = ""
    for n in pBox:
        result = result + text_to_permute[n - 1]
        
    return result


def expansion_PBox(text_to_permute):
    pBox = [4, 1, 2, 3, 2, 3, 4, 1]
    result = ""
    for n in pBox:
        result = result + text_to_permute[n - 1]
        
    return result

def xor(out_expansion, key):
    result = ""
    for y in range(len(out_expansion)):
        if out_expansion[y] == key[y]:
            result = result + '0'
        else:
            result = result + '1'
    return result

def binaryToDecimal(n): 
    return int(n,2) 

def sBox(txt):
    LH = txt[:4]
    RH = txt[4:]
    
    s0_matrix = [
        ["01", "00", "11", "10"], 
        ["11", "10", "01", "00"], 
        ["00", "10", "01", "11"], 
        ["11", "01", "11", "10"]
    ]
    s1_matrix = [
        ["00", "01", "10", "11"], 
        ["10", "00", "01", "11"], 
        ["11", "00", "01", "00"], 
        ["10", "01", "00", "11"]
    ]
    
    row = binaryToDecimal(LH[0] + LH[3])
    col = binaryToDecimal(LH[1] + LH[2])
    
    LH1 = s0_matrix[row][col]
    
    row = binaryToDecimal(RH[0] + RH[3])
    col = binaryToDecimal(RH[1] + RH[2])
    
    RH1 = s1_matrix[row][col]
    
    tmp = LH1+RH1
    
    tmp = P4(tmp)
    
    return tmp
    
def round_des(txt,k):
    
    
    LH = txt[:4]
    RH = txt[4:]
    
    res = expansion_PBox(RH)
    res = xor(res,k)

    res = sBox(res)

    LH = xor(LH,res)
    
    combined = LH+RH
    
    return combined[4:]+combined[:4]
    
def encrypt(plaintext,key):
    
    k1,k2 = round_key_generator(key)
    txt = IP8(plaintext)
    
    round1 = round_des(txt,k1)
    round2 = round_des(round1,k2)
    
    res = IP8_inv(round2[4:]+round2[:4])
    return res

def decrypt(plaintext,key):
    
    k1,k2 = round_key_generator(key)
    txt = IP8(plaintext)

    round1 = round_des(txt,k2)
    round2 = round_des(round1,k1)
    
    res = IP8_inv(round2[4:]+round2[:4])
    return res

plaintext = input("Enter Plain text in 8 digit binary format : ")
key = input("Enter key in 10  digit binary format : ")

enc = encrypt(plaintext,key)  
dec = decrypt(enc,key)
print("Plain Text : ",plaintext)
print("Key : ", key)
print("Encryption : ",enc)

print("Cipher Text : ",plaintext)
print("Key : ", key)
print("Decrytion : ",dec)