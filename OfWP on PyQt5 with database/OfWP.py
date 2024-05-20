import sys
import subprocess
import os
import ctypes
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from interface import Ui_MainWindow
from time import sleep
from datetime import datetime
from database import DataBase

db = DataBase()


# Проверка, запущена ли программа от имени администратора
def is_admin():
    try:
        return os.getuid() == 0

    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


class Program(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.name = None
        self.setupUi(self)
        self.scnd_win = SecondWindow()
        file = open('log.txt', mode='a', encoding='utf8')
        file.write(f'The program was launched. '
                   f'Time: {datetime.now().strftime("%d %b %Y %H:%M:%S")}\n')
        if is_admin():
            self.enter.setEnabled(True)
            self.newuser.setEnabled(True)
            file.write(f'Everything is OK\n')
        else:
            self.welcome.setText('Запустите программу от имени администратора'
                                 ' и повторите попытку! '
                                 'Содержимое недоступно.')
            self.enter.setText('Ошибка входа')
            self.enter.setEnabled(False)
            self.newuser.setEnabled(False)
            file.write(f'The program does NOT run as an administrator. '
                       f'The change is not available.\n')
        self.newuser.clicked.connect(self.add_new_user)
        self.enter.clicked.connect(self.authorization)
        self.del_cur.clicked.connect(self.selective_deletion)
        self.del_all.clicked.connect(self.full_removal)
        self.restore.clicked.connect(self.reinstall)
        self.author.clicked.connect(lambda: self.scnd_win.show())
        file.close()

    def authorization(self):
        if self.enter.text() == 'Войти в аккаунт':
            if db.login(self.login.text(), self.password.text()):
                self.name = self.login.text()
                self.result.setText(f'Здравствуйте, {self.name}! '
                                    f'Теперь вам доступен основной '
                                    f'интерфейс программы')
                self.newuser.setEnabled(False)
                self.del_cur.setEnabled(True)
                self.del_all.setEnabled(True)
                self.restore.setEnabled(True)
                self.enter.setText('Выйти из аккаунта')
                file = open('log.txt', mode='a', encoding='utf8')
                file.write(
                    f'{datetime.now().strftime("%d %b %Y %H:%M:%S")} User '
                    f'"{self.name}" logged in.\n')
                file.close()
                db.user_log_in(self.name)

            else:
                self.result.setText('Неверная пара логина и пароля!')
                self.del_cur.setEnabled(False)
                self.del_all.setEnabled(False)
                self.restore.setEnabled(False)
                file = open('log.txt', mode='a', encoding='utf8')
                file.write(
                    f'{datetime.now().strftime("%d %b %Y %H:%M:%S")} '
                    f'Wrong password! '
                    f'Login: {self.login.text()}, '
                    f'Password: {self.password.text()}\n')
                file.close()
        elif self.enter.text() == 'Выйти из аккаунта':
            self.result.setText('Вы вышли из своего аккаунта.')
            self.enter.setText('Войти в аккаунт')
            self.login.setText('')
            self.password.setText('')
            self.newuser.setEnabled(True)
            self.del_cur.setEnabled(False)
            self.del_all.setEnabled(False)
            self.restore.setEnabled(False)
            file = open('log.txt', mode='a', encoding='utf8')
            file.write(f'{datetime.now().strftime("%d %b %Y %H:%M:%S")} User '
                       f'"{self.name}" logged out.\n')
            file.close()
            self.name = 'None'

    def add_new_user(self):
        if not self.login.text() and not self.password.text():
            self.result.setText('Введите корректное имя пользователя и пароль')
            return
        if db.registration(self.login.text(), self.password.text()):
            self.result.setText(f'Пользователь "{self.login.text()}" с '
                                f'паролем "{self.password.text()}" добавлен')
            file = open('log.txt', mode='a', encoding='utf8')
            file.write(f'{datetime.now().strftime("%d %b %Y %H:%M:%S")} A '
                       f'new account has been created. '
                       f'Login: "{self.login.text()}".\n')
            file.close()
        else:
            self.result.setText('Ошибка! Данный пользователь уже существует')

    def selective_deletion(self):
        apps = ('Microsoft.549981C3F5F10', 'solitaire', 'office', 'onenote',
                'mspaint',
                'skype', 'xbox', 'alarms', 'phone', 'Microsoft.Wallet',
                'notes',
                'soundrecorder', 'windowscommunicationsapps', 'calculator',
                'camera',
                'maps', 'zunevideo', 'people', 'zunemusic', 'ScreenSketch',
                'news',
                'BingWeather', 'MixedReality.Portal', 'bing', 'Getstarted',
                'Microsoft3DViewer', 'GetHelp', 'photos', 'WindowsFeedbackHub',
                'Yandex.Music')
        description = ('Cortana', 'Microsoft Solitaire Collection',
                       'UWP Microsoft Office', "OneNote", 'Paint 3D', 'Skype',
                       "Сервисы Xbox", "Будильники и часы", "Ваш телефон",
                       "Кошелёк Microsoft", "Записки (Sticky Notes)",
                       "Запись голоса",
                       "Календарь и Почта", "UWP Калькулятор", "Камера",
                       "Карты",
                       "Кино и ТВ", "Люди", "Музыка Groove",
                       "Набросок фрагмента на экране", "Новости", "Погода",
                       "Портал смешанной реальности", "Сервисы Bing", "Советы",
                       "Средство 3D-просмотра", "Техническая поддержка",
                       "Фотографии и Видеоредактор", "Центр отзывов",
                       "Яндекс.Музыка")
        self.progress.setValue(0)
        app_list = list()
        for element in self.buttons.buttons():
            if element.isChecked():
                if element.text() == 'Новости':
                    subprocess.Popen(["powershell",
                                      'winget uninstall "windows web '
                                      'experience pack"'],
                                     stdout=subprocess.PIPE,
                                     creationflags=subprocess.CREATE_NO_WINDOW)
                else:
                    # находим пакет в списке по его индексу
                    identifier = description.index(element.text())
                    application = apps[identifier]
                    subprocess.Popen(["powershell",
                                      f'Get-AppxPackage -allusers '
                                      f'*{application}* | Remove-AppxPackage'],
                                     stdout=subprocess.PIPE,
                                     creationflags=subprocess.CREATE_NO_WINDOW)
                app_list.append(element.text())

            self.progress.setValue(self.progress.value() + 100 // len(apps))
        self.progress.setValue(100)

        file = open('log.txt', mode='a', encoding='utf8')
        file.write(
            f'{datetime.now().strftime("%d %b %Y %H:%M:%S")} Applications '
            f'that were deleted by the user "{self.name}": {app_list}.\n')
        file.close()
        db.usr_del_programs(app_list)

    def full_removal(self):
        self.progress.setValue(0)
        subprocess.Popen(["powershell",
                          'Get-AppxPackage -allusers | Remove-AppxPackage'],
                         stdout=subprocess.PIPE,
                         creationflags=subprocess.CREATE_NO_WINDOW)
        file = open('log.txt', mode='a', encoding='utf8')
        file.write(
            f'{datetime.now().strftime("%d %b %Y %H:%M:%S")} All '
            f'applications were deleted by the user "{self.name}".\n')
        file.close()
        db.usr_del_programs('all')
        for i in range(101):
            sleep(0.1)
            self.progress.setValue(i)

    def reinstall(self):
        self.progress.setValue(0)
        subprocess.Popen(["powershell",
                          r'Get-AppxPackage -allusers | foreach '
                          r'{Add-AppxPackage -register '
                          r'"$($_.InstallLocation)\appxmanifest.xml" '
                          r'-DisableDevelopmentMode}'],
                         stdout=subprocess.PIPE,
                         creationflags=subprocess.CREATE_NO_WINDOW)
        file = open('log.txt', mode='a', encoding='utf8')
        file.write(
            f'{datetime.now().strftime("%d %b %Y %H:%M:%S")} All applications '
            f'have been restored by the user "{self.name}".\n')
        file.close()
        db.usr_del_programs('reinstall')
        for i in range(101):
            sleep(0.1)
            self.progress.setValue(i)

    def closeEvent(self, close):
        reply = QMessageBox.question(self, 'Выход', 'Вы уверены, что хотите '
                                                    'выйти из аккаунта и '
                                                    'закрыть окно?',
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            file = open('log.txt', mode='a', encoding='utf8')
            file.write(
                f'{datetime.now().strftime("%d %b %Y %H:%M:%S")} Exit the '
                f'application...\n\n')
            file.close()
            db.close_connection()
            close.accept()
        else:
            close.ignore()


class SecondWindow(QWidget):
    def __init__(self):
        super(SecondWindow, self).__init__()
        self.setFixedSize(600, 600)
        self.setWindowTitle('Разработчик')
        self.pixmap = QPixmap('img.jpg')
        self.image = QLabel(self)
        self.image.move(45, 35)
        self.image.setPixmap(self.pixmap)
        self.text = QLabel(self)
        self.text.setText('Rabinovich Igor')
        self.text.move(520, 585)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Program()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
