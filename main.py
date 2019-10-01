from PySide2 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QComboBox,QMessageBox,QAction
import sys,os
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from ui  import Ui_MainWindow

# Create Application
app = QtWidgets.QApplication(sys.argv)
# init



MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
# Logic
filesCount=0
images = []
prices= []

imageFolder = ""
driver = webdriver.Chrome()
driver.get("https://tap.az/elanlar/new")
#Contacts
def infodialog():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Creator: Ilkin Aslanli\n+(994)51-622-23-23")
    msg.setWindowTitle("Info")
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
# Message Box
def showdialog(msge):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(msge)
    msg.setWindowTitle("Info")
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()

# Working with Folders
def selImgFolder():
    try:

        global images
        global imageFolder
        global filesCount
        global prices
        imageFolder = QFileDialog.getExistingDirectory()
        ui.label_10.setText(imageFolder)
        files = os.listdir(imageFolder)
        for file in files:
            if (file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png')):
                prices.append(file.split('.')[0])
                filesCount+=1
                images.append(file)
        print(prices,filesCount)
    except Exception as e:
        showdialog(str(e))

# Getting categorues after clicking and solve CheckBox and RadioButton clicking
def clickToRightCategory():

    try:
        category = Select(driver.find_element_by_name("lot[category_path]"))
        category.select_by_index(15)

        def getCategories():

            driver.implicitly_wait(10)
            obj = driver.find_element_by_name("lot[property_set][755]")
            pod_category = str(obj.text).split('\n')
            for item in pod_category:
                ui.comboBox.addItem(item)

        getCategories()
    except Exception as e:
        showdialog(str(e))

def checkBoxSolve():
    try:
        while (True):
            try:
                driver.find_element_by_id("lot_property_set_761").click()
                driver.find_element_by_name("lot[service]").click()
                driver.find_element_by_id("lot_contact_attributes_update_user").click()

                break
            except:
                continue
    except Exception as e:
        showdialog(str(e))

# Handling Errors
def errorCheck():
    try:
        errors=""
        if not ui.lineEdit.text() or not ui.lineEdit_2.text() or not ui.lineEdit_4.text() or not ui.textEdit.toPlainText() or not ui.lineEdit_5.text() or not ui.label_10.text() or ui.comboBox.currentIndex()==1:
            errors+="Elan tam doldurulmayib"

        return  errors
    except Exception as e:
        showdialog(str(e))

# Adding Information on WebSite
def addingInfo():
    ui.pushButton.setEnabled(False)
    errors = errorCheck()
    if not errors:

        for i in range(0, filesCount):

            try:

                clickToRightCategory()
                checkBoxSolve()
                driver.implicitly_wait(10)
                category = Select(driver.find_element_by_name("lot[property_set][755]"))
                category.select_by_index(ui.comboBox.currentIndex())

                driver.find_element_by_id('lot_price').clear()
                driver.find_element_by_id('lot_price').send_keys(prices[i])

                driver.find_element_by_id('lot_body').clear()
                driver.find_element_by_id('lot_body').send_keys(ui.textEdit.toPlainText())

                driver.find_element_by_name('lot[title]').clear()
                driver.find_element_by_name('lot[title]').send_keys(ui.lineEdit.text())

                driver.find_element_by_name('lot[contact_attributes][name]').clear()
                driver.find_element_by_name('lot[contact_attributes][name]').send_keys(ui.lineEdit_2.text())

                driver.find_element_by_name('lot[contact_attributes][phones_separated]').clear()
                driver.find_element_by_name('lot[contact_attributes][phones_separated]').send_keys(ui.lineEdit_3.text())

                driver.find_element_by_name('lot[contact_attributes][email]').clear()
                driver.find_element_by_name('lot[contact_attributes][email]').send_keys(ui.lineEdit_4.text())

                driver.find_element_by_class_name('pond-new-img-field').send_keys(imageFolder+'/'+images[i])
                time.sleep(int(ui.lineEdit_5.text()))
                driver.find_element_by_name('button').click()
                ui.label_11.setText(str(i+1) + "/" + str(filesCount))

                driver.get("https://tap.az/elanlar/new")
            except Exception as e:
                showdialog(str(images[0]+" Elave olunmadi:"+e))
        ui.pushButton.setEnabled(True)
        driver.get("https://tap.az/elanlar/new")
    else:
        showdialog(errors)
        ui.pushButton.setEnabled(True)









clickToRightCategory()
 
ui.toolButton.clicked.connect(selImgFolder)
ui.pushButton.clicked.connect(addingInfo)
ui.pushButton_2.clicked.connect(infodialog)



#Run
sys.exit(app.exec_())

