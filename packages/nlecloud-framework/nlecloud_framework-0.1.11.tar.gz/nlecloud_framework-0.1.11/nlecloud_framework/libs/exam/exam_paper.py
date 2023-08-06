# _*_ coding:utf-8 _*_
"""
@File: exam_paper.py
@Author: cfp
@Date: 2020-08-21 14:07:08
@LastEditTime: 2023/3/3 9:30
@LastEditors: cfp
@Description: 将题库自动输出为指定的word模板试卷
"""
import re
import os
import random
import copy
import pandas as pd
from pandas.core import series
from tqdm import tqdm
# pip install cytoolz
from cytoolz import pipe
from docxtpl import DocxTemplate


from nlecloud_framework import config




class ExamPaperHelper(object):
    def __init__(self,):
        # 下载模板地址
        self.download_tpl_path = "http://resource.rs.nlecloud.com/file/nlecloud_framework"


    def usage(self):
        """
        :description:输出工具使用手册
        :param args:
        :last_editors: cfp
        :return
        :return:
        """
        print("具体使用方法如下：".center(60,"="))
        print("1、先下载试卷模板文件、答案模板文件和题库模板文件")
        print("试卷模板下载地址：",self.download_tpl_path+"/tpl.docx")
        print("答案模板下载地址：",self.download_tpl_path+"/answer_tpl.docx")
        print("题库模板下载地址：",self.download_tpl_path+"/exam_db_tpl.xlsx")
        print("2、将模板文件放置到client_config.py配置的临时目录下")
        print("3、按要求将题库内容放到题库模板中去")
        print("4、实例化参数运行run方法")
        print("5、你可以自定义单选题和判断题数量，以及职业道德题和专业题的数量")


    def _check_verify(self,df: pd.DataFrame)->pd.DataFrame:
        """
        :description: 检查文档是否符合程序要求
        :param args:
        :last_editors: cfp
        :return
        """
        origin_cloumn = ['question', '题型', 'type', 'A', 'B', 'C', 'D', 'answer']
        excel_column = self.get_cloumn_name(df)
        if set(origin_cloumn) - set(excel_column):
            print("请修改题库列表名称，正确列表名称为：['question', '题型', 'type', 'A', 'B', 'C', 'D', 'answer']")
            exit(886)
        return df


    def _choice_quesion_format(self,item:series.Series):
        """
        :description: 对数据选择题问题进行格式化操作
        :param args:
        :last_editors: cfp
        :return
        """
        # 中括号进行替换
        replace_str = ""
        if re.search("\s+）",item["question"]):
            replace_str = "（"+re.search("\s+）",item["question"]).group()

        if re.search("\s+\)", item["question"]):
            replace_str = "(" + re.search("\s+\)", item["question"]).group()
        item["question"].replace(replace_str,"（  ）")


        # 判断是否存在中括号
        if ("(" not in item["question"] and ")" not in item["question"]) and ("（" not in item["question"] and "）" not in item["question"]):
            # 添加（）
            item["question"] = item["question"] + "（  ）"

        # 判断是否存在句号
        if not item["question"].endswith("。"):
            item["question"] = item["question"] + "。"

    def _data_format(self,df: pd.DataFrame)->pd.DataFrame:
        """
        :description: 进行数据清洗
        :param args:
        :last_editors: cfp
        :return
        """
        # 数据去重复
        df.drop_duplicates()
        # 数据填充
        df.fillna("")
        # 对题库选择题的题目进行格式化处理
        df.apply(self._choice_quesion_format,axis=1)
        return df


    def get_cloumn_name(self,df:pd.DataFrame)->list:
        """
        :description: 获取列名
        :param args:
        :last_editors: cfp
        :return
        """
        print("当前文档列名为:")
        print(df.columns.tolist())
        print("=============================")
        return df.columns.tolist()

    def get_question_db(self,path:str)->pd.DataFrame:
        """
        :description:获取题库
        :param args:
        :last_editors: cfp
        :return
        """
        # 读取文件,数据检测、数据清洗
        df = pipe(path,pd.read_excel,self._check_verify,self._data_format)
        return df


    def product_exam(self,df: pd.DataFrame, zzdy_number_choice, zyt_number_choice, zyt_number_jude, zzdy_number_jude, choice_number) -> (dict, list):
        """
        :description: 产出试卷内容,组装数据
        :param df: 要进行处理的数据
        :param zzdy_number_choice:职业道德选择题数量
        :param zyt_number_choice: 专业题选择题数量
        :param zyt_number_jude: 专业题判断题数量
        :param zzdy_number_jude: 职业道德判断题数量
        :param choice_number: 选择题总数
        :last_editors: cfp
        :return
        """
        # 组装数据
        exam_subject = {"choice": [], "jude": []}
        answer_list = []  # 答案列表

        # 选择题列表
        zzdy_choice = df[(df["type"] == "职业道德题") & (df["题型"] == "选择题")].sample(n=zzdy_number_choice)
        zyt_choice = df[(df["type"] == "专业题") & (df["题型"] == "选择题")].sample(n=zyt_number_choice)

        # 判断题列表
        zzdy_jude = df[(df["type"] == "职业道德题") & (df["题型"] == "判断题")].sample(n=zzdy_number_jude)
        zyt_jude = df[(df["type"] == "专业题") & (df["题型"] == "判断题")].sample(n=zyt_number_jude)

        # 将dataframe数据都放到exam_subject数据中去
        for dfdata in [zzdy_choice, zyt_choice, zzdy_jude, zyt_jude]:
            for i in range(len(dfdata)):
                item = dfdata.iloc[i].to_dict()
                question_type = str(item["题型"]).strip()
                # 判断题目类型
                if question_type == "判断题":
                    # 这里判断题要放到选择题后面，所以index需要加上选择题的数量
                    item["index"] = len(exam_subject["jude"]) + 1 + choice_number
                    exam_subject["jude"].append(copy.deepcopy(item))
                    anser = item["answer"]
                    # 判断题的答案A、B要显示对勾还是x
                    if anser == "A":
                        answer_list.append("√")
                    elif anser == "B":
                        answer_list.append("×")
                elif question_type == "选择题":
                    # 添加索引
                    item["index"] = len(exam_subject["choice"]) + 1
                    exam_subject["choice"].append(copy.deepcopy(item))
                    answer_list.append(item["answer"])
                else:
                    print("出现未知题型！！")
                    print(item)
                    exit(886)

        return exam_subject, answer_list


    def _check_file_exist(self,excel_name,word_name,tpl_name,answer_tpl)->(str,str,str,str):
        """
        :description: 检测文件是否存在
        :param excel_name:
        :param word_name:
        :param tpl_name:
        :param answer_tpl:
        :last_editors: cfp
        :return
        """
        excel_path = os.path.join(config.temp_path, excel_name)
        tpl_path = os.path.join(config.temp_path, tpl_name)
        answer_tpl_path = os.path.join(config.temp_path, answer_tpl)
        word_path = os.path.join(config.temp_path, word_name.split(".")[0] + ".docx")
        if not os.path.exists(excel_path) or not os.path.exists(tpl_path) or not os.path.exists(answer_tpl_path):
            print("当前输入文件不存在请检查：".center(60,"="))
            print("题库路径：",excel_path)
            print("试卷模板路径：",tpl_path)
            print("试卷答案模板路径：",answer_tpl_path)
            self.usage()
            exit(886)

        if not tpl_path.endswith("docx"):
            self.usage()
            exit(886)

        if not word_path.endswith(".docx"):
            print("输出试卷文件名要以.docx文件类型，进行结尾。")
            print("word_name：",word_name)
            exit(886)

        return excel_path,word_path,tpl_path,answer_tpl_path


    def run(self,excel_name:str, word_name:str,tpl_name="tpl.docx",anser_tpl="answer_tpl.docx",choice_number=50,jude_number=25,zzdy_number=5,print_answer=False):
        """
        :description:
        :param excel_name: 题库excel文件名称
        :param word_name: 要进行保存的试卷文件名称
        :param tpl_name: 试卷模板文件名字
        :param anser_tpl: 答案模板文件名字
        :param choice_number: 选择题数量
        :param jude_number: 判断题数量
        :param zzdy_number: 职业道德题数量。比如选择题一共50题，判断题一共20题，职业道德选择和判断加起来要5题，那么就会随机判断选择题+判断题的职业道德数
        :param print_answer: 是否要答案出答案到控制台
        :last_editors: cfp
        :return
        """
        # 判断题库和模板路径是否存在
        excel_path, word_path, tpl_path, answer_tpl_path = self._check_file_exist(excel_name=excel_name,word_name=word_name,tpl_name=tpl_name,answer_tpl=anser_tpl)

        # 题数确定 道德职业题目要5题，可以是判断题+选择一共5道题
        zzdy_number_choice = random.choice(range(1, zzdy_number)) # random随机取1-5之间要出多少选择题，剩下的判断题 （5 - 这个随机值）
        zzdy_number_jude = zzdy_number - zzdy_number_choice
        zyt_number_choice = choice_number - zzdy_number_choice
        zyt_number_jude = jude_number - zzdy_number_jude
        print(f"职业道德选择题一共：{zzdy_number_choice}题,职业道德判断题一共：{zzdy_number_jude}题")
        print(f"专业题选择题：{zyt_number_choice}题,专业题判断题一共：{zyt_number_jude}题")
        print("=============================")

        # 数据获取
        df = self.get_question_db(excel_path)

        # 获得组装好的题目和对应的答案
        exam_subject, answer_list = self.product_exam(df, zzdy_number_choice, zyt_number_choice, zyt_number_jude, zzdy_number_jude, choice_number)

        # 组装答案参数
        answer_struct = {"choice": [], "jude": []}
        for i in range(0, len(answer_list), 10):
            # 这里我们取序列
            max_series = min(len(answer_list) + 1, i + 11)
            step_series_list = list(range(i + 1, max_series))  # [71, 72, 73, 74, 75]
            step_answer_list = answer_list[i:i + 10]  # ['√', '√', '√', '√', '√']
            temp_dict_list = [{"index": k, "value": v} for k, v in zip(step_series_list, step_answer_list)]
            for _ in range(10 - len(temp_dict_list)):
                temp_dict_list.append({"index": "", "value": ""})

            # 判断当前10个答案是判断题还是选择题
            if step_answer_list[0] in "ABCDEFG":
                answer_struct["choice"].append(temp_dict_list)
            elif step_answer_list[0] in "√×":
                answer_struct["jude"].append(temp_dict_list)
            else:
                print("当前无法判断题型！", temp_dict_list)

        # 是否输出答案
        if print_answer:
            print("输出题目答案信息:", end="\n")

        # 渲染数据保存试卷文档
        tpl = DocxTemplate(tpl_path)
        tpl.render({"data": exam_subject})
        tpl.save(word_path)

        answer_tpl = DocxTemplate(answer_tpl_path)
        answer_tpl.render({"answer":answer_struct})
        answer_tpl.save(word_path.split(".docx")[0] + "答案" + ".docx")

