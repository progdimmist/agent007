from random import randint

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMessageBox


class MyGame:
    __instance = None
    __buf_instance = None

    @staticmethod
    def get_buf():
        return MyGame.__buf_instance

    @staticmethod
    def get_instance():
        return MyGame.__instance

    @staticmethod
    def inst(width: int, height: int, mines_count: int, main_window):
        MyPlayer.player, MyGame.__instance, MyGame.__buf_instance = None, None, None
        MyGame.__instance = MyGame(width, height, mines_count, main_window)
        MyGame.__buf_instance = MyGame(width, height, mines_count, main_window)
        return MyGame.__instance

    def __init__(self, width: int, height: int, mines_count: int, main_window):
        self.__main_window = main_window
        self.__mines_count = mines_count
        self.__width = width
        self.__height = height
        self.__main_window.field.setRowCount(height)
        self.__main_window.field.setColumnCount(width)
        self.__main_window.field.setFixedSize(42 * width, 38 * height)
        self.__count_box = width * height - mines_count - 1
        self.__score = 0
        self.__main_window.BoxesValue.setText(str(self.__count_box))
        self.__main_window.GoalValue.setText(str(int(self.__count_box / 4)))
        self.__main_window.BoxesPercent.setText(str(int((self.__count_box / (width * height) * 100))) + "%")
        self.__main_window.GoalPercent.setText(str(int((self.__count_box / (width * height) * 25))) + "%")
        self.__main_window.BoxesValue.adjustSize()
        self.__main_window.GoalValue.adjustSize()
        self.__main_window.BoxesPercent.adjustSize()
        self.__main_window.GoalPercent.adjustSize()
        self.__main_window.field.setCellWidget(0, 0, MyPlayer.inst(main_window))
        counter_of_mines, k = 0, 1
        for i in range(height):
            for j in range(k, width):
                self.__main_window.field.setCellWidget(i, j, MyCell(randint(1, 7), i, j, main_window))
            k = 0
        while counter_of_mines < mines_count:
            rand_width, rand_height = randint(1, width), randint(1, height)
            self.__main_window.field.setCellWidget(rand_width, rand_height, MyMine(main_window))
            counter_of_mines += 1
        self.__main_window.field.show()

    @property
    def get_mines_count(self) -> int:
        return self.__mines_count

    @property
    def get_width(self) -> int:
        return self.__width

    @property
    def get_height(self) -> int:
        return self.__height

    @property
    def get_field(self):
        return self.__main_window.field

    @staticmethod
    def count_score_and_boxes(boxes: list):
        MyGame.__instance.__count_box -= len(boxes)
        MyGame.__instance.__score += sum(boxes) * 10
        MyGame.__instance.__main_window.BoxesValue.setText(str(MyGame.__instance.__count_box))
        MyGame.__instance.__main_window.ScoreValue.setText(str(MyGame.__instance.__score))
        MyGame.__instance.__main_window.BoxesPercent.setText(str(int(
            MyGame.__instance.__count_box / (MyGame.__instance.__width * MyGame.__instance.__height) * 100)) +
                                                             "%")
        MyGame.__instance.__main_window.BoxesValue.adjustSize()
        MyGame.__instance.__main_window.BoxesPercent.adjustSize()
        MyGame.__instance.__main_window.ScoreValue.adjustSize()


def massageOver():
    msg = QMessageBox()
    msg.setText("<p align='left'>You lose!</p>")
    msg.setWindowTitle("Game over!")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setStyleSheet("background-color: yellow;")
    msg.layout().setContentsMargins(100, 50, 100, 50)
    msg.move(200, 200)
    msg.exec_()


def massageWin():
    msg = QMessageBox()
    msg.setText("<p align='left'>You won!</p>")
    msg.setWindowTitle("Game over!")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setStyleSheet("background-color: red;")
    msg.layout().setContentsMargins(100, 50, 100, 50)
    msg.move(200, 200)
    msg.exec_()


class MyPlayer(QPushButton):
    player = None

    @staticmethod
    def inst(main_window):
        if MyPlayer.player is None:
            MyPlayer.player = MyPlayer(main_window)
        return MyPlayer.player

    def __init__(self, main_window):
        super().__init__(main_window)
        self.setText("⭕")
        self.setFont(QFont('Times', 13, QFont.Black))
        #

        self.__i, self.__j = 0, 0

    @property
    def coord_i(self) -> int:
        return self.__i

    @property
    def coord_j(self) -> int:
        return self.__j

    def move_to(self, cell):
        field = MyGame.get_instance().get_field
        ins = MyGame.get_instance()
        _boxes = []
        diff_row, diff_column = self.__i - cell.coord_i, self.__j - cell.coord_j
        limit_row = self.__i - diff_row * cell.get_count_of_steps
        limit_column = self.__j - diff_column * cell.get_count_of_steps
        self.__i += diff_row
        self.__j += diff_column
        while self.__i != limit_row or self.__j != limit_column:
            self.__i -= diff_row
            self.__j -= diff_column
            _cell = field.cellWidget(self.__i, self.__j)
            if _cell.__class__ == MyMine:
                _cell.setText("💀")
                massageOver()
                break
            if self.__i >= ins.get_height or self.__j >= ins.get_height or self.__i < 0 or self.__j < 0:
                self.__i += diff_row
                self.__j += diff_column
                _cell = field.cellWidget(self.__i, self.__j)
                _cell.setText("💀")
                _cell.__class__ = MyMine
                massageOver()
                break
            if self.__i != limit_row or self.__j != limit_column:
                if _cell.__class__ != MyPlayer:
                    _boxes.append(_cell.get_count_of_steps)
                _cell.setText("🟦")
                if _cell.__class__ != MyPlayer:
                    _cell.__class__ = MyMine
            else:
                _cell.setText("⭕")
        MyGame.count_score_and_boxes(_boxes)


class MyCell(QPushButton):

    def __init__(self, count_steps: int, i: int, j: int, main_window):
        super().__init__(main_window)
        self.setText(str(count_steps))
        self.setFont(QFont('Axon', 13, QFont.Black))
        self.setIconSize(QSize(38, 38))
        self.clicked.connect(self.is_clicked_around_player)
        self.__count_steps, self.__i, self.__j = count_steps, i, j

    @property
    def get_count_of_steps(self) -> int:
        return self.__count_steps

    @property
    def coord_i(self) -> int:
        return self.__i

    @property
    def coord_j(self) -> int:
        return self.__j

    def is_clicked_around_player(self):
        if -1 <= MyPlayer.player.coord_i - self.__i <= 1 and -1 <= MyPlayer.player.coord_j - self.__j <= 1 and self.__class__ != MyMine:
            MyPlayer.player.move_to(self)


class MyMine(QPushButton):

    def __init__(self, main_window):
        super().__init__(main_window)
        self.setText("✖")
        self.setFont(QFont('Times', 18))
        self.setStyleSheet('color: red')
        self.setIconSize(QSize(38, 38))


