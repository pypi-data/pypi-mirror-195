import openai
import asyncio
import httpx
from nlecloud_framework.utils.prt_cmd_color import *

openai.api_key = "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"

h = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {openai.api_key}'
}
d = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "请解释同步请求和异步请求的区别"}],
    "max_tokens": 100,
    "temperature": 0
}
u = 'https://api.openai.com/v1/chat/completions'


class ChatGPT:
    def __init__(self, chat_list=[]) -> None:
        # 初始化对话列表
        self.chat_list = []

        # 异步访问

    async def ask_async(self, prompt):

        d["messages"][0]["content"] = prompt
        async with httpx.AsyncClient() as client:
            resp = await client.post(url=u, headers=h, json=d)
            result = resp.json()
            print(result)

            # 显示接口返回

    def show_conversation(self, msg_list):
        msg_list = msg_list[len(msg_list) - 2:len(msg_list)]
        for msg in msg_list:
            if msg['role'] == 'user':
                print(f"Me: {msg['content']}")
            else:
                # printGreen("")
                printBlue(f"ChatGPT:{msg['content']}")
                # print("\033[0;32;40mChatGPT:\033[0m",end="")
                # print(f"\033[0;34;40m{msg['content']}\033[0m")
                # print(f"ChatGPT: \033[0;31;42m{msg['content']}\033[0m\n")

    def ask(self, prompt):
        self.chat_list.append({"role": "user", "content": prompt})
        # self.chat_list.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.chat_list)
        answer = response.choices[0].message['content']
        # 添加历史对话，形成上下文关系
        self.chat_list.append({"role": "assistant", "content": answer})
        # self.chat_list.append({"role": "assistant", "content": answer})
        self.show_conversation(self.chat_list)


if __name__ == '__main__':
    chat = ChatGPT()
    while True:
        question = input("请输入你的问题：").strip()
        chat.ask(question)
        # asyncio.run(chat.ask_async())



    # chat.ask("你是一位南宋词人，词风婉约，有点类似李清照女士，请使用蝶恋花词牌描写北国春光")
    # chat.ask("请使用另外一种粗狂阳刚的风格再写一遍上面的词")
    # asyncio.run(chat.ask_async("请解释同步请求接口和异步请求接口的区别"))