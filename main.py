import sys
from os import path 
from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QLabel, QPushButton, QSpinBox, QTableWidget, QPushButton
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.uic import loadUi
from qdarktheme import setup_theme, enable_hi_dpi
from time import sleep
from appresources import fagainstx
import progress


def get_resource_path(relative_path):
    """
    Get the absolute path to the resource based on whether the script is running as an executable or as a script.
    """
    if getattr(sys, 'frozen', False):
        # Running as an executable, use sys._MEIPASS to access bundled files
        base_path = sys._MEIPASS
    else:
        # Running as a script, use the script's directory
        base_path = path.dirname(path.abspath(__file__))
    
    resource_path = path.join(base_path, relative_path)
    return resource_path


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = loadUi(get_resource_path('StatsMEUI.ui'),self)
        self.tabWidget.setCurrentIndex(1)
        # Create a QFont object and set the font size
        font = QFont()
        font.setPointSize(14)  # Set the font size to 16 points
        self.tableWidget.setFont(font)
        self.tableWidget.setColumnWidth(1, 160)
        self.spinBox_dp.setValue(2)
        self.dp = self.spinBox_dp.value()
        self.handleButtonPressed()
        self.handleUiChanges()
        self.pushButton_estimatefx.setEnabled(False)
        self.pushButton_finally.setEnabled(False)
        self.mean = 0
        self.median = 0
        self.variance = 0
        self.sd = 0
    
    
    def delay_screen(self):
        sleep(0.7)  
        self.tabWidget.setCurrentIndex(1)
        
    def handleUiChanges(self):
        self.tabWidget.tabBar().setVisible(False)
        self.spinBox_dp.valueChanged.connect(self.dp_changed)
        
    def handleButtonPressed(self):
        self.pushButton_addRow.clicked.connect(self.addNewRow)
        self.pushButton_estimate.clicked.connect(self.estimate)
        self.pushButton_estimatefx.clicked.connect(self.checkFStatus)
        self.pushButton_estimateMean.clicked.connect(self.estimateMean)
        self.pushButton_estimateDFM.clicked.connect(self.estimateD)
        self.pushButton_finally.clicked.connect(self.finishAll)
        self.pushButton_start.clicked.connect(self.delay_screen)
        self.pushButton_fagainstx.clicked.connect(self.plotfagainstx)
        self.pushButton_removeRow.clicked.connect(self.removeRow)
    
    def plotfagainstx(self):
        noOfRow = self.tableWidget.rowCount()
        x_axis = []
        y_axis = []
        for i in range(noOfRow):
            val = self.tableWidget.item(i, 2).text()
            x_axis.append(val)
        for i in range(noOfRow):
            val = self.tableWidget.item(i, 3).text()
            y_axis.append(int(val))
        
        plotinst = fagainstx(x_axis, y_axis)
        plotinst.plot()
        
    
      
    def addNewRow(self):
        noOfRow = self.tableWidget.rowCount()
        self.tableWidget.insertRow(noOfRow)
        # Check if the row occupied so as to re-estimatw
        if self.tableWidget.item(0,0) == None:
                return
        self.estimate()
        try:
            self.finishAll()
        except:
            pass
        
    def comparedecimal(self, num):
        if "." in num:
            oldLength = len(num[num.index(".")+1:])
            if (oldLength < self.dp):
                noOfZeros = self.dp - oldLength
                zerosToAdd = "0" * noOfZeros
                return num + zerosToAdd
            else:
                return num
        else:
            return num

    def estimate(self):
        try:
            value = self.tableWidget.item(0, 0).text()
            value = value.split("-")
            value = [i.strip(" ") for i in value]
            a, b = int(value[0]), int(value[1])
            diff = (b - a) + 1
            self.diff = diff
        except AttributeError:
            QMessageBox.critical(self, "Invalid Input", "Class Group cannot be Empty")
            return
        except ValueError:
            QMessageBox.critical(self, "Invalid Input", "Class Group should be in the format\n'A - B' where A is less than B and\nboth variables are integers" )
            return
        except IndexError:
            QMessageBox.critical(self, "Invalid Input - Wrong Format", "Class Group should be in the format\n'A - B' where A is less than B and\nboth variables are integers" )
            return
            
        
        noOfRow = self.tableWidget.rowCount()
        for i in range(noOfRow - 1):
            i += 1
            value = self.tableWidget.item(i - 1, 0).text()
            value = value.split("-")
            value = [n.strip(" ") for n in value]
            a, b = int(value[0]), int(value[1])
            ans = (b+1, b + diff)
            self.tableWidget.setItem( i, 0, QTableWidgetItem(str(ans[0]) + " - " + str(ans[1])))
                
        for i in range(noOfRow):
            value = self.tableWidget.item(i, 0).text()
            value = value.split("-")
            value = [n.strip(" ") for n in value]
            a, b = int(value[0]), int(value[1])
            if a == 0:
                a = 0.5
            ans = (a - 0.5, b + 0.5)
            
            self.tableWidget.setItem( i, 1, QTableWidgetItem(str(ans[0]) + " - " + str(ans[1])))
            item = self.tableWidget.item(i, 1)
            item.setFlags(item.flags() ^ 32)  # 32 is the flag for ItemIsEditable
            ...

        for i in range(noOfRow):
            value = self.tableWidget.item(i, 0).text()
            value = value.split("-")
            value = [n.strip(" ") for n in value]
            a, b = int(value[0]), int(value[1])
            ans = (a + b) / 2
            self.tableWidget.setItem( i, 2, QTableWidgetItem(str(ans)))
            item = self.tableWidget.item(i, 2)
            item.setFlags(item.flags() ^ 32)  # 32 is the flag for ItemIsEditable
          
        # Enable Button that will estiamte fx
        self.pushButton_estimatefx.setEnabled(True)

            
    def checkFStatus(self):
        noOfRow = self.tableWidget.rowCount()

        for i in range(noOfRow):
            try:
                value = self.tableWidget.item(i, 3).text()
                if "." in value:
                    QMessageBox.critical(self, "Error", f"Frequency value in row {i+1} must be an integer not a floating point number")
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(""))    
                    return    
                ans = float(value)
            except AttributeError:
                QMessageBox.critical(self, "Error", f"Frequency value in row {i+1} is Empty")      
                return 
            except ValueError:
                QMessageBox.critical(self, "Error", f"'{value}' is not an integer\nFrequency at row {i+1} must be an integer")      
                return 
            
            estimatefx = ans * float(self.tableWidget.item(i, 2).text())
            numResult = partial(self.comparedecimal, str(estimatefx))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(numResult()))
            
        # Enable Extimate Mean Button
        self.pushButton_estimateMean.setEnabled(True)
        # Enabled Visualize f against x button
        self.pushButton_fagainstx.setEnabled(True)

            
   
    def estimateMean(self):
        self.checkFStatus()
        sumOfX = 0.0
        sumOfFx = 0.0
        
        noOfRow = self.tableWidget.rowCount()
        
        for i in range(noOfRow):         
            value = float(self.tableWidget.item(i, 3).text())
            sumOfX += value
        for i in range(noOfRow):         
            value = float(self.tableWidget.item(i, 4).text())
            sumOfFx += value
            
        self.mean = sumOfFx / sumOfX
        rawMean = str(round(self.mean, self.dp))
        meanToDisplay = partial(self.comparedecimal, rawMean)
        self.mean_label.setText(meanToDisplay())
        self.pushButton_estimateDFM.setEnabled(True)
        
    def dp_changed(self):
        self.dp = int(self.spinBox_dp.value())
        for j in range(3,8):
            if self.tableWidget.item(0, j) is None:
                return
        try:
            self.estimateMean()
            self.estimateD()
            self.finishAll()            
        except:
            ...
    
    def estimateD(self):
        noOfRow = self.tableWidget.rowCount()
        for i in range(noOfRow):
            value = float(self.tableWidget.item(i, 2).text())
            ans = value - self.mean
            dval = round(ans, self.dp)
            dvalToDisplay = partial(self.comparedecimal, str(dval))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(dvalToDisplay()))

        self.pushButton_finally.setEnabled(True)
            
    def estimateD2(self):
        noOfRow = self.tableWidget.rowCount()
        for i in range(noOfRow):
            value = float(self.tableWidget.item(i, 5).text())
            dval = value * value
            dval = round(dval, self.dp)
            dvalToDisplay = partial(self.comparedecimal, str(dval))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(dvalToDisplay()))
            
    def estimateFD2(self):
        noOfRow = self.tableWidget.rowCount()
        for i in range(noOfRow):
            value = float(self.tableWidget.item(i, 6).text())
            value2 = float(self.tableWidget.item(i, 3).text())
            dval = value * value2
            dval = round(dval, self.dp)
            dvalToDisplay = partial(self.comparedecimal, str(dval))
            self.tableWidget.setItem(i, 7, QTableWidgetItem(dvalToDisplay()))
    
    def estimateVariance(self):
        noOfRow = self.tableWidget.rowCount()
        sumall = 0
        sumfreq = 0
        for i in range(noOfRow):
            value = float(self.tableWidget.item(i, 7).text())
            sumall += value
            
        for i in range(noOfRow):
            value = float(self.tableWidget.item(i, 3).text())
            sumfreq += value
            
        self.variance = sumall / sumfreq
        
        self.variance_label.setText(str(round(self.variance, self.dp)))
        
        self.sd = self.variance ** 0.5
        
        varVal = round(self.sd, self.dp)
        varianceToDisplay = partial(self.comparedecimal, str(varVal))
        self.sd_label.setText(varianceToDisplay()) 
        
    def estimateMedian(self):
        noOfRow = self.tableWidget.rowCount()
        N = 0
        median_freq = 0
        for i in range(noOfRow):
            f_val = int(self.tableWidget.item(i, 3).text())
            N += f_val
            
        median_value_range = N / 2
        sum_of_f = 0
        
        for index in range(noOfRow):
            f_val = int(self.tableWidget.item(index, 3).text())
            sum_of_f += f_val
            if sum_of_f >= median_value_range:
                median_freq = f_val
                median_index = index
                break
              
        cum_freq_before = 0
        for m in range(noOfRow):
            f_val = int(self.tableWidget.item(m, 3).text())
            if m == median_index:
                break
            cum_freq_before += f_val
            
        L = float((self.tableWidget.item(median_index, 1).text()).split("-")[0])
        class_width = self.diff 
        
        part1 = (((N/2) - cum_freq_before) / median_freq)
        self.median  = (part1 * class_width) + L
        medianval = round(self.median, self.dp)
        medianToDisplay = partial(self.comparedecimal, str(medianval))
        self.median_label.setText(str(medianToDisplay()))

    def estimateMode(self):
        """
            Mode = L + ((fm-fb)/((fm-fb) + fm -fa)) + C
            
            where:   
                - L is the lower class boundary of the Modal class.
                - fm is the frequancy of the modal class.
                - fb is the frquancy before the modal class.
                - fa is the frequcny after the modal class.
                - C is the class interval of the Distribution
        """
        
        noOfRow = self.tableWidget.rowCount()
        # GEt all frequency in a list and get the maximum and the index of the maximum
        ls_of_frequency = [int(self.tableWidget.item(i, 3).text()) for i in range(noOfRow)]
        fm = max(ls_of_frequency)
        index_fm = ls_of_frequency.index(fm)
        
        fb = int(self.tableWidget.item(index_fm - 1, 3).text())
        fa = int(self.tableWidget.item(index_fm + 1, 3).text())
        
        C = self.diff
        
        L = float(self.tableWidget.item(index_fm, 1).text().split("-")[0])
        
        # Calculation
        change1 = fm - fb
        change2 = fm - fa
        
        parenthensis_cal = (change1 / (change1 + change2))
        self.mode = L + (parenthensis_cal * C)
        
        
        # Set mode value to approparite decimal place(s)
        modeval = round(self.mode, self.dp)
        modeToDisplay = partial(self.comparedecimal, str(modeval))
        self.mode_label.setText(str(modeToDisplay()))
           
            
    def finishAll(self):
        self.estimateD2()
        self.estimateFD2()
        self.estimateMean()
        self.estimateVariance()
        self.estimateMedian()
        self.estimateMode()
        
    def removeRow(self):
        """
        Get and remove unwated row in table widget
        
        """
        
        currentRow = self.tableWidget.currentRow()
        noOfRow = self.tableWidget.rowCount()
        print(currentRow)
        if currentRow > 0:
            self.tableWidget.removeRow(currentRow)
            if self.tableWidget.item(0,0) == None:
                return
            self.estimate()
            try:
                self.finishAll()
            except:
                pass
        elif ((currentRow == -1) or currentRow == 0) and noOfRow != 1:
            self.tableWidget.removeRow(noOfRow-1)
            if self.tableWidget.item(0,0) == None:
                return
            self.estimate()
            try:
                self.finishAll()
            except:
                pass


def main() :
    enable_hi_dpi()
    app = QApplication(sys.argv)
    setup_theme()
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
