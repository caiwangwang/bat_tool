import tkinter as tk
import subprocess
import threading
import time
import sys

global dev_status
# 创建一个事件用于线程停止
stop_event = threading.Event()

def check_adb_devices():
    while not stop_event.is_set():  # 检查停止事件
        try:
            # 执行 adb devices 命令
            result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout.strip()

            # 检查输出是否包含已连接设备
            if "device" in output and len(output.splitlines()) > 1:
                dev_status = 1
            else:
                dev_status = 0

        except Exception as e:
            print(f"检测设备时发生错误: {e}")

        time.sleep(10)  # 每 10 秒检测一次

def button_click():
    print("hello")

def create_win_instance(width, height, transparency):
    res = f"{width}x{height}"
    main_win = tk.Tk()
    main_win.title("BAT TOOL")
    main_win.geometry(res)
    # 设置窗口背景透明度，0.0（完全透明）到 1.0（完全不透明）
    main_win.wm_attributes("-alpha", transparency)
    # 顶层显示
    main_win.attributes("-topmost", True)
    return main_win

def add_win_label(win_inst, context, x, y):
    # 添加标签
    label = tk.Label(win_inst, text=context, font=("Arial", 10))
    label.grid(row=x, column=y)
    return label

def add_win_entry(win_inst):
    # 添加文本框
    entry = tk.Entry(win_inst)
    entry.pack()
    return entry

def add_win_button(win_inst, name, func, x, y, w, h, bgcolor="white", fcolor="lightblue"):
    # 创建画布
    canvas = tk.Canvas(win_inst, width=w, height=h, bg=bgcolor)
    canvas.grid(row=x, column=y)

    # 绘制自定义形状（例如，一个长方形， 左上角坐标，和右下角坐标）
    button_shape = canvas.create_rectangle(x, y, w, h, fill=fcolor, outline="black")
    # 在长方形中添加文本
    text = canvas.create_text(w/2, h/2, text=name, fill="black", font=("Arial", 10, "bold"), justify="left")
    # 绑定鼠标事件
    canvas.tag_bind(button_shape, '<Button-1>', lambda event: func())
    canvas.tag_bind(text, '<Button-1>', lambda event: func())

    # button = tk.Button(win_inst, text="remount", command=button_click)
    # button.grid(row=0, column=0, padx=0, pady=0)
    return canvas


if __name__=="__main__":
    dev_status = 0
    win_width = 300
    win_height = 300
    button_w = 80
    button_h = 30
    main_win = create_win_instance(win_width, win_height, 0.8)
    button = add_win_button(main_win, "newscript", button_click, 0, 0, button_w, button_h)
    status_label = add_win_label(main_win, "状态: device offline", win_width, 0)
    # 创建并启动检测线程
    monitor_thread = threading.Thread(target=check_adb_devices)
    monitor_thread.daemon = True  # 设置为守护线程
    monitor_thread.start()

    try:
        while True:
            # 运行主窗口循环
             main_win.mainloop()
    except KeyboardInterrupt:
        print("监控已停止.")
        stop_event.set()  # 设置停止事件
        monitor_thread.join()  # 等待线程结束