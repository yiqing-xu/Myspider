import tkinter as tk
from tkinter import ttk
import pypinyin
import requests
import json
import tkinter.font as tkFont


class Express(object):

    def __init__(self, window, comboxlist, e):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }
        self.url = "https://www.kuaidi100.com/query"
        self.window = window
        self.comboxlist = comboxlist
        self.e = e

    def main(self):
        b = tk.Button(self.window, text="查  询", width=15, height=2, font=("黑体", 15), command=self.insert)
        b.place(x=380, y=20, anchor='nw')

        self.window.mainloop()

    def query(self):
        ex_cpy = self.get_type()
        odd_num = self.e.get()
        post_data = {
            "type": ex_cpy,
            "postid": odd_num
        }
        response = requests.post(self.url, data=post_data, headers=self.headers)
        res = json.loads(response.content.decode("utf-8"))
        if res["status"] == "200":
            data = res["data"]
            info = str()
            for i in data:
                info = info + i["time"] + i["context"] + "\n\n"
            return info
        else:
            return "未查询到正确的快递信息，\n请输入正确的快递单号"

    def get_type(self):
        value = self.comboxlist.get()
        if value == "京东":
            return "jd"
        else:
            var = "".join(i[0] for i in pypinyin.pinyin(value, style=pypinyin.NORMAL))
            return var

    def insert(self):
        t = tk.Text(self.window, font=("黑体", 10))
        t.place(x=30, y=90, anchor='nw')
        t.delete('1.0', 'end')
        t.insert("insert", self.query())


if __name__ == '__main__':
    window = tk.Tk()
    window.title("快递查询")
    window.geometry("623x450")
    window.resizable(0, 0)

    ft = tkFont.Font(family='Fixdsys', size=13, weight=tkFont.BOLD)

    comboxlist = ttk.Combobox(window, width=15, font=ft)
    comboxlist["value"] = ("圆通", "中通", "韵达", "申通", "邮政国内", "邮政EMS", "天天", "顺丰", "京东")
    comboxlist.current(0)
    comboxlist.place(x=120, y=20, anchor='nw')

    hint = tk.Label(window, text="快递公司", font=ft)
    hint.place(x=30, y=20, anchor='nw')
    hint = tk.Label(window, text="快递单号", font=ft)
    hint.place(x=30, y=50, anchor='nw')

    e = tk.Entry(window, width=17, font=ft)
    e.place(x=120, y=50, anchor='nw')

    express = Express(window, comboxlist, e)
    express.main()


