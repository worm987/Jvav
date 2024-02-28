import shutil
import os

print("JVAV v0.01 (by zhanghaoyang")

run = False # 设置程序状态

# 文件名处理
def file(name):
    if os.path.exists(name) == True:
        while os.path.exists(name):
            temp_text = name.split('.') # 分割文件名称
            name = file(temp_text[0]+'[副本].'+temp_text[1])
        return name
    elif os.path.exists(name) == False:
        return name
    


def command(command):
    cmd = command.split() # 分割文本：空格
    cmd_len = len(cmd)
    temp_text = '' # 定义一个空值
    if cmd[0] == 'print':
        # 使用循环拼接文本输出
        for i in range(cmd_len):
            if i != 0: # 跳过指令
                temp_text = temp_text + cmd[i] + "\x20" # 在末尾添加一个空格，如果不加就没有空格
        return temp_text # 输出列表
    elif cmd[0] == 'copy': # 复制文件
        temp_text = shutil.copy(cmd[1], file(cmd[2]))
        return '复制完成！'
    elif cmd[0] == 'del': # 复制文件
        return os.remove(cmd[1])
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
            return "错误：请使用正确的格式！"
        return shutil.make_archive(cmd[2], temp_text, root_dir=os.getcwd())
    else:
        return "错误：'%s' 不是内部或外部命令，也不是可运行的程序\n或批处理文件。" % cmd[0]



while run == False: # 判断循环
    cmd = input("jvav>")
    command_return = command(cmd)
    if command_return != None:
        print(command_return+"\n")
