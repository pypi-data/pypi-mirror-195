import PySimpleGUI as sg

from ddtank.utils.get_game import get_game
from ddtank.utils.get_script import get_script_name, start_script, stop_script
from ddtank.utils.get_capture import get_point, get_image
from ddtank.utils.get_map import get_map

menu_def = [['游戏', ['窗口识别']],
            ['辅助功能', ['截图取色', '截图取图', '地图识别']]
            ]
layout = [[sg.Menu(menu_def, tearoff=False, pad=(20, 1))],
          [sg.Text('选择游戏窗口'), sg.Combo(values=get_game(True)[1], default_value='请选择游戏窗口', size=(20, 1), key='窗口列表')],
          [sg.Text('选择游戏窗口所执行的脚本内容')],
          [sg.Listbox(values=get_script_name(), size=(32, 12), key='脚本列表')],
          [sg.Button('执行', key='执行', size=(8, 1)), sg.Button('结束', key='结束', size=(8, 1)), sg.Button('退出', key='退出', size=(8, 1))],
          [sg.StatusBar('欢迎使用ddtank', size=(32, 1), relief=sg.RELIEF_SOLID, key='状态栏')]
          ]


class DDTanker:
    def __init__(self):
        self.handle_list, self.title_list = get_game(True)
        self.thread_list = [None] * len(self.handle_list)
        self.window = sg.Window('ddtank脚本执行器', layout)

        while True:
            self.event, self.values = self.window.read()
            if self.event in (None, '退出'):
                break
            elif self.event == '窗口识别':
                self.update_windows()
            elif self.event in ('执行', '结束', '截图取色', '截图取图', '地图识别'):
                if self.event == '截图取色':
                    handle = self.get_handle()
                    if handle:
                        get_point(handle)
                elif self.event == '截图取图':
                    handle = self.get_handle()
                    if handle:
                        image_name = get_image(handle)
                        if image_name:
                            self.window['状态栏'].update(f'截图保存在./image/{image_name}.png')
                elif self.event == '地图识别':
                    handle = self.get_handle()
                    if handle:
                        get_map(handle)
                elif self.event == '执行':
                    handle = self.get_handle()
                    script = self.get_focus_script()
                    if handle and script:
                        index = self.handle_list.index(handle)
                        self.thread_list[index] = start_script(script, handle)
                        self.window['状态栏'].update(f'{self.title_list[index]}执行脚本{script}')
                elif self.event == '结束':
                    handle = self.get_handle()
                    if handle:
                        index = self.handle_list.index(handle)
                        if self.thread_list[index] is not None:
                            stop_res = stop_script(self.thread_list[index])
                            self.thread_list[index] = None
                            if stop_res:
                                self.window['状态栏'].update('强制结束成功')
                            else:
                                self.window['状态栏'].update('该脚本已经结束了')
                        else:
                            self.window['状态栏'].update('此窗口没有正在运行的脚本')

        self.window.close()

    def update_windows(self):
        for thread in self.thread_list:
            if thread is not None:
                self.window['状态栏'].update('当前有游戏窗口脚本运行中，请先结束')
        else:
            self.handle_list, self.title_list = get_game(True)
            self.window['窗口列表'].update('请选择游戏窗口', values=self.title_list)
            self.window['状态栏'].update('重新识别窗口成功')

    def get_handle(self):
        if self.window['窗口列表'].get() not in self.window['窗口列表'].Values:
            self.window['状态栏'].update('当前没有选择游戏窗口')
        else:
            handle_index = self.window['窗口列表'].Values.index(self.window['窗口列表'].get())
            handle = self.handle_list[handle_index]
            return handle

    def get_focus_script(self):
        script = self.values['脚本列表']
        if len(script) > 0:
            return script[0]
        else:
            self.window['状态栏'].update('当前没有选择要执行的脚本')