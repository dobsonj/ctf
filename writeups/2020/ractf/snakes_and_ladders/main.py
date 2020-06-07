def xor(s1,s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

def encrypt(a):
    some_text = a[::2]

    randnum = 14
    text_length = len(some_text)
    endtext = ""
    for i in range(1, text_length + 1):
      weirdtext = some_text[i - 1]
      if weirdtext >= "a" and weirdtext <= "z":
          weirdtext = chr(ord(weirdtext) + randnum)
          if weirdtext > "z":
              weirdtext = chr(ord(weirdtext) - 26)
      endtext += weirdtext
    randtext = a[1::2]

    xored = xor("aaaaaaaaaaaaaaa", randtext)
    hex_xored = xored.encode("utf-8").hex()

    return endtext + hex_xored

def decrypt(msg):
    raise NotImplementedError

def main():
    opt = input("Would you like to [E]ncrypt or [D]ecrypt? ")
    if opt[:1].lower() == "e":
        msg = input("Enter message to encrypt: ")
        print(f"Encrypted message: {encrypt(msg)}")
    elif opt[:1].lower() == "d":
        msg = input("Enter message to decrypt: ")
        print(f"Decrypted message: {decrypt(msg)}")

if __name__ == "__main__":
    main()
