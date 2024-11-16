# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
import numpy as np
import math
import time
from sympy import *
from scipy.special import perm,comb
import ast
from PySide6.QtCharts import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from modules import *
from widgets import *

os.environ["QT_FONT_DPI"] = "96"  # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None


# 被积函数

def fun(Fx,values):
    y_values = [Fx(x) for x in values]
    return y_values

def CreateFx(FxString):
    x = symbols('x')
    expr = sympify(FxString)
    Fx = lambdify(x, expr, modules=['numpy'])
    return Fx


def save_coordinates(x_values, y_values):
    """
    存储坐标值到文件。

    参数:
    x_values (list): x坐标值列表。
    y_values (list): y坐标值列表。
    filename (str): 存储坐标值的文件名。
    """
    with open(r'./graphics_info.csv', 'w') as f:
        for x, y in zip(x_values, y_values):
            f.write(f"{x},{y}\n")

def data_display(self):
    """
    电脑信息的数据展示
    :return:
    """
    # 清空之前的系列数据
    self.seriesS.clear()
    # 获取已经记录好的数据并展示
    # 设置一个flag
    with open(r'./graphics_info.csv', 'r') as f:
        reader = f.readlines()
        for line in reader:
            date_point = line.replace('\n', '').split(',')
            # 横坐标
            col = float(date_point[0])
            # 纵坐标
            row = float(date_point[1])
            self.seriesS.append(col, row)

    self.chart = QChart()  # 创建 Chart
    self.chart.setTitle("函数图")
    self.chart.addSeries(self.seriesS)
    self.chart.createDefaultAxes()
    widgets.graphicsView.setChart(self.chart)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "计算方法大作业"
        description = "Calculation method"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        # 新增切换模式界面按钮
        widgets.btn_message.clicked.connect(self.buttonClick)
        # 新增计算方法界面按钮
        widgets.btn_calculate.clicked.connect(self.buttonClick)
        widgets.count1.clicked.connect(self.buttonClick)
        widgets.count2.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)

        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)

        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        # 路径冻结，防止打包成exe后路径错乱
        if getattr(sys, 'frozen', False):
            absPath = os.path.dirname(os.path.abspath(sys.executable))
        elif __file__:
            absPath = os.path.dirname(os.path.abspath(__file__))
        useCustomTheme = True
        self.useCustomTheme = useCustomTheme
        self.absPath = absPath
        themeFile = os.path.abspath(os.path.join(absPath, "themes\py_dracula_light.qss"))
        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU

        if btnName == "btn_save":
            # print("Save BTN clicked!")
            QMessageBox.information(self,"提示","该功能暂未实现",QMessageBox.Yes)

        if btnName == "btn_message":
            if self.useCustomTheme:
                themeFile = os.path.abspath(os.path.join(self.absPath, "themes\py_dracula_dark.qss"))
                UIFunctions.theme(self, themeFile, True)
                # SET HACKS
                AppFunctions.setThemeHack(self)
                self.useCustomTheme = False
            else:
                themeFile = os.path.abspath(os.path.join(self.absPath, "themes\py_dracula_light.qss"))
                UIFunctions.theme(self, themeFile, True)
                # SET HACKS
                AppFunctions.setThemeHack(self)
                self.useCustomTheme = True

        if btnName == "btn_calculate":
            widgets.stackedWidget.setCurrentWidget(widgets.calculater)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU
            self.seriesS = QLineSeries()
            self.seriesS.setName("fun")


        if btnName == "count1":
            a = int(widgets.lineEdit_4.text())
            b = int(widgets.lineEdit_7.text())
            n = int(widgets.lineEdit_11.text())
            integ = self.compoundTrapezoidFormula(fun, b, a, n)
            QMessageBox.information(self,"提示",f"{integ}",QMessageBox.Yes)
            data_display(self)

        if btnName == "count2":
            a = int(widgets.lineEdit_5.text())
            b = int(widgets.lineEdit_8.text())
            n = int(widgets.lineEdit_12.text())
            integ = self.compositeSimpsonformula(fun, a, b, n)
            QMessageBox.information(self,"提示",f"{integ}",QMessageBox.Yes)


        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

    # 复合辛普森公式

    def compositeSimpsonformula(self,fun, a, b, n):
        if n <= 0:
            return 0
        x = widgets.lineEdit_3.text()
        h = (b - a - 10 ** (-20)) / (2 * n)
        value = np.array([a + 10 ** (-20) + h * i for i in np.arange(2 * n + 1)])
        fx = fun(CreateFx(x),value)
        save_coordinates(value, fx)
        Integ = fx[0] + fx[2 * n]
        Integ = Integ + 4 * np.sum(np.array(fx[1:2 * n:2])) + 2 * np.sum(np.array(fx[2:2 * n:2]))
        Integ = Integ * h / 3
        return Integ

    # 复合梯形公式

    def compoundTrapezoidFormula(self,fun, b, a, n):
        if n <= 0:
            return 0
        x = widgets.lineEdit_2.text()
        h = (b - a - 10 ** (-20)) / n
        value = np.array([a + 10 ** (-20) + h * i for i in np.arange(n + 1)])
        fx = fun(CreateFx(x),value)
        save_coordinates(value,fx)
        Integ = fx[0] + fx[n]
        Integ = Integ + 2 * sum(np.array(fx[1:n]))
        Integ = Integ / 2 * h
        return Integ

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
