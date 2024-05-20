import subprocess
from tkinter import *

FONT = "Verdana 12 bold"  # шрифт
BACKGROUND = "#262622"  # цвет фона
FONT_COLOR = "#F3F1ED"  # цвет текста
ACTIVE = "#CD5C5C"  # цвет активного состояния

window = Tk()
window.title('Optimization of Windows programs')
window.config(bg=BACKGROUND)
window.geometry('710x670')
window.resizable(False, False)

ox, oy = 20, 10
check_button_list = list()
apps = ('Microsoft.549981C3F5F10', 'solitaire', 'office', 'onenote', 'mspaint',
        'skype', 'xbox', 'alarms', 'phone', 'Microsoft.Wallet', 'notes',
        'soundrecorder', 'windowscommunicationsapps', 'calculator', 'camera',
        'maps', 'zunevideo', 'people', 'zunemusic', 'ScreenSketch', 'news',
        'BingWeather', 'MixedReality.Portal', 'bing', 'Getstarted',
        'Microsoft3DViewer', 'GetHelp', 'photos', 'WindowsFeedbackHub',
        'Yandex.Music')

description = ('Cortana', 'Microsoft Solitaire Collection',
               'UWP Microsoft Office', "OneNote", 'Paint 3D', 'Skype',
               "Сервисы Xbox", "Будильники и часы", "Ваш телефон",
               "Кошелёк Microsoft", "Записки (Sticky Notes)", "Запись голоса",
               "Календарь и Почта", "UWP Калькулятор", "Камера", "Карты",
               "Кино и ТВ", "Люди", "Музыка Groove",
               "Набросок фрагмента на экране", "Новости", "Погода",
               "Портал смешанной реальности", "Сервисы Bing", "Советы",
               "Средство 3D-просмотра", "Техническая поддержка",
               "Фотографии и Видеоредактор", "Центр отзывов", "Яндекс.Музыка")


class CheckbuttonVar(Checkbutton):
    def __init__(self, *args, **kwargs):
        self._var = BooleanVar()
        super().__init__(*args, variable=self._var, **kwargs)

    @property
    def is_checked(self):
        return self._var.get()

    @is_checked.setter
    def is_checked(self, value):
        self._var.set(value)


def selective_deletion():
    for i, cb in enumerate(check_button_list):
        if cb.is_checked:
            if cb["text"] == 'Новости':
                subprocess.Popen(["powershell",
                                  'winget uninstall "windows web experience '
                                  'pack"'], stdout=subprocess.PIPE,
                                 creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen(["powershell",
                                  f'Get-AppxPackage -allusers *{apps[i]}*'
                                  ' | Remove-AppxPackage'],
                                 stdout=subprocess.PIPE,
                                 creationflags=subprocess.CREATE_NO_WINDOW)


def full_removal():
    subprocess.Popen(["powershell",
                      'Get-AppxPackage -allusers | Remove-AppxPackage'],
                     stdout=subprocess.PIPE,
                     creationflags=subprocess.CREATE_NO_WINDOW)


def restore():
    subprocess.Popen(["powershell",
                      r'Get-AppxPackage -allusers | foreach {Add-AppxPackage '
                      r'-register "$($_.InstallLocation)\appxmanifest.xml" '
                      r'-DisableDevelopmentMode}'],
                     stdout=subprocess.PIPE,
                     creationflags=subprocess.CREATE_NO_WINDOW)


for app in description:
    tmp = CheckbuttonVar(window, selectcolor=BACKGROUND,
                         activeforeground=ACTIVE,
                         activebackground=BACKGROUND, bg=BACKGROUND,
                         fg=FONT_COLOR, text=app,
                         onvalue=True, offvalue=False, font=FONT)
    tmp.place(x=ox, y=oy)
    if oy == 430:
        ox, oy = 370, 10
    else:
        oy += 30
    check_button_list.append(tmp)


lbl_remove = Label(window, bg=BACKGROUND, fg='#B22222',
                   text='''ВНИМАНИЕ! Это действие также
удалит магазин Microsoft.''',
                   font=FONT)
lbl_notrec = Label(window, bg=BACKGROUND, fg='#B22222',
                  text='Не рекомендуется для Windows 11', font='Verdana 9')
lbl_restore = Label(window, bg=BACKGROUND, fg='#008000',
                    text='''  Все приложения будут загружены
на компьютер заново.''',
                    font=FONT)
lbl_name = Label(window, bg=BACKGROUND, fg='#696969',
                 text='© developed by Igor Rabinovich')
btn_selective = Button(window, bg='#FF4500', fg=FONT_COLOR,
                       text="Удалить выбранные приложения",
                       command=selective_deletion, font=FONT,
                       activebackground=ACTIVE, relief=FLAT)
btn_remove_all = Button(window, bg='#B22222', fg=FONT_COLOR,
                        text="Удалить все UWP приложения",
                        command=full_removal, font=FONT,
                        activebackground=ACTIVE, relief=FLAT)
btn_restore_all = Button(window, bg='#008000', fg=FONT_COLOR,
                         text="Восстановить все UWP приложения",
                         command=restore, font=FONT,
                         activebackground='#90EE90', relief=FLAT)


btn_selective.place(x=190, y=480)
btn_remove_all.place(x=20, y=550)
btn_restore_all.place(x=340, y=550)
lbl_remove.place(x=15, y=590)
lbl_notrec.place(x=45, y=630)
lbl_restore.place(x=340, y=590)
lbl_name.place(x=530, y=650)

window.mainloop()
