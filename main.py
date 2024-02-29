import shutil
import os
import json
import sys


run = False # 设置程序状态

def f_v(file_path): # 文件的处理
    with open(file_path, "r", encoding='utf-8', errors='replace') as file:
        text = ""
        error = ""
        for i, line in enumerate(file):
            line = line.strip()
            commane_text = command(line)
            # 使用 json.loads() 而不是 json.load()
            data = json.loads(commane_text) # 修改这里
            if data["error"]:
                error += "\x20"*4 + f"程序在第 {i+1} 行时出现了错误: \n"+"\x20"*8+data["text"]+"\n\n"
            elif not data["error"]:
                text += data["text"] + "\n"
            else:
                error += f"程序在第 {i+1} 行时出现了错误: \n程序遇到了不该出现的错误，这一般出现在调试中，如果你是用户，请向QQ号2704478857反馈这个错误！\n\n"
    if error != "":
        return text + "\n\n错误：\n" + error
    else:
        return text


# 文件名处理
def rename_if_exists(original_name):
    # 修改函数名以避免潜在的混淆
    if os.path.exists(original_name):
        while os.path.exists(original_name):
            name_parts = original_name.split('.')
            original_name = rename_if_exists(name_parts[0] + '[副本].' + name_parts[1])
        return original_name
    else:
        return original_name
    
def return_text(error, text):
    # 直接返回一个字典，而不是字典的列表
    return json.dumps({
        "error": error,
        "text": text
    })

def command(command):
    cmd = command.split() # 分割文本：空格
    cmd_len = len(cmd)
    temp_text = '' # 定义一个空值
    if cmd[0] == 'print':
        # 使用循环拼接文本输出
        for i in range(cmd_len):
            if i != 0: # 跳过指令
                temp_text = temp_text + cmd[i] + "\x20" # 在末尾添加一个空格，如果不加就没有空格
        return return_text(False,temp_text) # 输出列表
    elif cmd[0] == 'copy': # 复制文件
        temp_text = shutil.copy(cmd[1], file(cmd[2]))
        return return_text(False,"复制完成！")
    elif cmd[0] == 'del': # 删除文件
        os.remove(cmd[1])
        return return_text(False, "文件删除成功！") # 修改这里以返回适当的消息
    elif cmd[0] == 'make': # 压缩文件
        # 设置压缩格式
        if cmd[1] == '-zip':
            # ZIP格式
            temp_text = 'zip'
        elif cmd[1] == '-tar':
            # TAR格式
            temp_text = 'tar'
        elif cmd[1] == '-gztar':
            # TAR GZ格式
            temp_text = 'gztar'
        elif temp_text == '-bztar':
            # TAR BZ2格式
            temp_text = 'bztar'
        else:
            return return_text(True,"请使用正确的格式！")
        return return_text(False,shutil.make_archive(cmd[2], temp_text, root_dir=os.getcwd()))
    elif cmd[0] == 'system': # 执行系统命令
        if (os.system(cmd[1]) == 1):
            return return_text(False,"") 
        else:
            return return_text(True, "system命令时，出现了报错，请修改代码")
        
    elif cmd[0] == 'exit': # 退出
        return exit()
    else:
        return return_text(True, "'%s' 不是内部命令。" % cmd[0])


def main():
    # 先判断是否有参数然后判断是否进入循环
    if (len(sys.argv) <= 1):
        print("JVAV v0.01 (by zhanghaoyang")
        while True:
            cmd = input("jvav>")
            command_return = command(cmd)
            data = json.loads(command_return)
            # 解析返回的json
            data = json.loads(command_return)
            if data["error"] == True:
                print("程序出现错误:\n",data["text"])
            elif data["error"] == False:
                print(data["text"])
            else:
                print("程序遇到了不该出现的错误，这一般出现在调试中，如果你是用户，请向QQ号2704478857反馈这个错误！")
    elif (len(sys.argv) == 3):
        for i in range(1, len(sys.argv)):
            if (sys.argv[i] == "-v"):
                return f_v(sys.argv[i+1])

if __name__ == "__main__":
    print(main())
