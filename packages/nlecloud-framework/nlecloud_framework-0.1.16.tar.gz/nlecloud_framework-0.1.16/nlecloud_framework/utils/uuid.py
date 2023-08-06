# _*_ coding:utf-8 _*_
"""
@File: uuid.py
@Author: cfp
@Date: 2020-08-21 14:07:08
@LastEditTime: 2023/2/23 10:36
@LastEditors: cfp
@LastModifyTime @Version  @Desciption
@Description: 
"""

# 使用的模块是uuid7
import uuid

class UUIDHelper:
    @classmethod
    def get_uuid(self):
        """
        :Description: 获取uuid4
        :return: uuid字符串
        :last_editors: cfp
        """
        return str(uuid.uuid4())


if __name__ == '__main__':
    print(UUIDHelper.get_uuid())