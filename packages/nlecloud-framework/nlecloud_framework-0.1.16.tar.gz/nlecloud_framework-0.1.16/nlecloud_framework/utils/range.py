# _*_ coding:utf-8 _*_
"""
@File: range.py
@Author: cfp
@Date: 2020-08-21 14:07:08
@LastEditTime: 2023/3/3 9:31
@LastEditors: cfp
@Description: 
"""

#range不可以使用小数作为步长，实现一个可迭代对象可以实现小数步长
class RangeHelper():
    def __init__(self, start, end, step):
        self.start = start - step
        self.end = end
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        self.start += self.step
        if self.start >= self.end:
            raise StopIteration
        return self.start


if __name__ == '__main__':
    for i in RangeHelper(1,3,0.5):
        print(i)
    print(RangeHelper(1,3,0.5)) # <__main__.RangeHelper object at 0x0000027B595CCFD0>
    print(list(RangeHelper(1,3,0.5))) # [1.0, 1.5, 2.0, 2.5]
