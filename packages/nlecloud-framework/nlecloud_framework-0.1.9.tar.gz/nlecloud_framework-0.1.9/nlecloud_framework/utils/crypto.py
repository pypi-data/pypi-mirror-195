# _*_ coding:utf-8 _*_
"""
@File: crypto.py
@Author: cfp
@Date: 2020-08-21 14:07:08
@LastEditTime: 2023/2/22 17:52
@LastEditors: cfp
@Description: 框架加密库
这个工具库提供了对称加密以及非对称加密
其中要注意在非对称加密中，是采用公钥进行加密而私钥进行解密的！！！

1、客户端来了，我发送自己的公钥给你，客户端拿这个公钥信息去验证合法性
2、客户端创建一个对称密钥对、再使用公钥进行加密、发送给服务端
3、服务端接收到了信息，使用私钥进行解密获取到对称加密
4、之间使用对称加密进行通信
"""
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from cryptography.fernet import Fernet
import base64

class CryptoHelper(object):

    @classmethod
    def genRandomKey(cls)->str:
        """
        @description: 生成一个随机的秘钥
        @param :
        @return 返回字符串经过base64的key
        @last_editors: cfp
        """
        key = Fernet.generate_key()
        key_b64 = base64.urlsafe_b64encode(key).decode('utf-8')
        return key_b64


    @classmethod
    def plain_to_ciphert(cls,key:str,plaintext:str)->str:
        """
        @description: 对数据进行加密
        @param key: 秘钥
        @param plaintext:要加密的数据
        @return
        @last_editors: cfp
        """
        # 将key转成字节
        key = base64.urlsafe_b64decode(key)

        # 对数据进行加密
        cipher_suite = Fernet(key)
        plaintext = plaintext.encode("utf8")
        ciphertext = cipher_suite.encrypt(plaintext)
        # 密文转换成base64编码字符串
        ciphertext_b64 = base64.urlsafe_b64encode(ciphertext).decode('utf-8')
        return ciphertext_b64


    @classmethod
    def cipher_to_plain(cls,key:str,ciphertext:str)->str:
        """
        @description:
        @param key: 秘钥
        @param ciphertext:加密的数据
        @return
        @last_editors: cfp
        """
        # 将base64密文解码
        key = base64.urlsafe_b64decode(key)
        ciphertext = base64.urlsafe_b64decode(ciphertext)
        # 创建一个Fernet对象，并使用密钥解密密文
        cipher_suite = Fernet(key)
        plaintext = cipher_suite.decrypt(ciphertext)

        # 打印解密后的数据
        return plaintext.decode("utf8")


    @classmethod
    def create_rsa_pair(cls,is_save=False):
        '''
        创建rsa公钥私钥对
        :param is_save: default:False
        :return: public_key, private_key
        '''
        f = RSA.generate(2048)
        private_key = f.exportKey("PEM")  # 生成私钥
        public_key = f.publickey().exportKey()  # 生成公钥
        if is_save:
            with open("crypto_private_key.pem", "wb") as f:
                f.write(private_key)
            with open("crypto_public_key.pem", "wb") as f:
                f.write(public_key)
        return public_key, private_key

    @classmethod
    def read_public_key(cls,file_path="crypto_public_key.pem") -> bytes:
        """
        :param file_path: 公钥文件路径
        :return:
        """
        with open(file_path, "rb") as x:
            b = x.read()
            return b

    @classmethod
    def read_private_key(cls,file_path="crypto_private_key.pem") -> bytes:
        with open(file_path, "rb") as x:
            b = x.read()
            return b


    @classmethod
    def encryption(cls,text: str, public_key: bytes):
        # 字符串指定编码（转为bytes）
        text = text.encode('utf-8')
        # 构建公钥对象
        cipher_public = PKCS1_v1_5.new(RSA.importKey(public_key))
        # 加密（bytes）
        text_encrypted = cipher_public.encrypt(text)
        # base64编码，并转为字符串
        text_encrypted_base64 = base64.b64encode(text_encrypted).decode()
        return text_encrypted_base64


    @classmethod
    def decryption(cls,text_encrypted_base64: str, private_key: bytes):
        # 字符串指定编码（转为bytes）
        text_encrypted_base64 = text_encrypted_base64.encode('utf-8')
        # base64解码
        text_encrypted = base64.b64decode(text_encrypted_base64)
        # 构建私钥对象
        cipher_private = PKCS1_v1_5.new(RSA.importKey(private_key))
        # 解密（bytes）
        text_decrypted = cipher_private.decrypt(text_encrypted, Random.new().read)
        # 解码为字符串
        text_decrypted = text_decrypted.decode()
        return text_decrypted



if __name__ == '__main__':
    # 1、获取加密秘钥
    key = CryptoHelper.genRandomKey()
    ciphertext = CryptoHelper.plain_to_ciphert(key,plaintext="明文信息")
    plaintext = CryptoHelper.cipher_to_plain(key,ciphertext=ciphertext)
    print("密文：",ciphertext)
    print("明文：",plaintext)

    # 2、非对称加密
    # 生成秘钥对
    public_key, private_key = CryptoHelper.create_rsa_pair(is_save=False)
    # 加密
    text = '123456'
    text_encrypted_base64 = CryptoHelper.encryption(text, public_key)
    print('密文：', text_encrypted_base64)

    # 解密
    text_decrypted = CryptoHelper.decryption(text_encrypted_base64, private_key)
    print('明文：', text_decrypted)
