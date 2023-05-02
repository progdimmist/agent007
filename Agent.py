import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow
from Game import MyGame


class MainForm(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()

    isGame = False

    def reset_my_game(self):
        if self.isGame:
            self.RulesWindow.hide()
            MyGame.inst(MyGame.get_buf().get_width, MyGame.get_buf().get_height,
                        MyGame.get_buf().get_mines_count, self)

    def small_field_clicked(self):
        self.RulesWindow.hide()
        MyGame.inst(10, 10, 5, self)
        self.isGame = True

    def medium_field_clicked(self):
        self.RulesWindow.hide()
        MyGame.inst(15, 15, 7, self)
        self.isGame = True

    def large_field_clicked(self):
        self.RulesWindow.hide()
        MyGame.inst(20, 20, 10, self)
        self.isGame = True

    def show_rules(self):
        self.RulesWindow.show()
        with open('Rules.html', 'r', encoding='utf-8') as f:
            html_text = f.read()
        self.RulesWindow.setText(html_text)

    def hide_rules(self):
        self.RulesWindow.hide()

    def init_ui(self):
        loadUi('MyMainForm.ui', self)
        self.RulesWindow.hide()
        self.field.hide()
        self.MenuForWindow.setFixedWidth(16777216)
        self.SmallFieldAction.triggered.connect(self.small_field_clicked)
        self.MediumFieldAction.triggered.connect(self.medium_field_clicked)
        self.LargeFieldAction.triggered.connect(self.large_field_clicked)
        self.ShowAction.triggered.connect(self.show_rules)
        self.HideAction.triggered.connect(self.hide_rules)
        self.ResetButton.clicked.connect(self.reset_my_game)
        self.showMaximized()


if __name__ == "__main__":
    MY_APP = QApplication(sys.argv)
    MY_FORM = MainForm()
    sys.exit(MY_APP.exec_())
