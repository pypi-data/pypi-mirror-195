from collections import deque
import string

# Encryptus v1.0.0
# Author: Hyphonical
# Author Info:
#   - Github:
#       - https://github.com/Hyphonic
#   - Discord:
#       - Hyphonical#1128
# Date: 2023-02-18
# Description: A Simple Encryption Module That Uses A Key To Encrypt And Decrypt Strings.
# License: MIT

@staticmethod
class Encryptus:
    def __init__(self, Key, BypassKeyLength=False): # Please Use A Long Key For Better Encryption. 10-20 Characters Is Recommended. The Longer The Key, The More Secure The Encryption And The Longer It Will Take To Crack.
        if BypassKeyLength is False:
            if len(Key) < 10:
                raise ValueError('Please Use A Longer Key. 10-20 Characters Is Recommended.\nTo Bypass This Error, Please Set The <BypassKeyLength> Argument To <True>.')
        self.Key = Key
        self.Convert = {}
        self.List = list(string.ascii_letters + string.digits + string.punctuation + string.whitespace)
        for _ in range(len(self.List)):
            self.Convert[_+100] = self.List[_]
    
    def GetKey(self):
        self.Encrypted = []
        for _ in self.Key:
            if _ in self.Convert.values():
                for Value in self.Convert:
                    if _ == self.Convert[Value]:
                        self.Encrypted.append(Value)
        return int(''.join([str(_) for _ in self.Encrypted]))

    def AddKey(self, String, Key): # Encryption Method (Add The Encrypted Key To The Encrypted Message)
        return String + Key

    def RemoveKey(self, String, Key):
        return String - Key

    def Encrypt(self, String, Key=None) -> int: # Main Encryption Method
        if Key is None:
            Key = self.GetKey()
        self.Encrypted = []
        for _ in String:
            if _ in self.Convert.values():
                for Value in self.Convert:
                    if _ == self.Convert[Value]:
                        self.Encrypted.append(Value)
            else:
                raise ValueError(f'<{_}> Is An Ivalid Character. Please Use A Diffrent String.\nTo See All Valid Characters, Please Use The <Encryptus.List> Attribute.')
        return self.AddKey(int(''.join([str(_) for _ in self.Encrypted])), Key)

    def Decrypt(self, String, Key=None) -> str: # Main Decryption Method
        if Key is None:
            Key = self.GetKey()
        String = list(str(self.RemoveKey(String, Key)))
        Divided = []; Divided.append([int(''.join(String[_:_+3])) for _ in range(0, len(String), 3)])
        self.Decrypted = []
        for _ in Divided[0]:
            self.Decrypted.append(self.Convert[_])
        return ''.join(self.Decrypted)
    
    def List(self): # List All Valid Characters That Can Be Encrypted And Decrypted
        return self.Convert.values()