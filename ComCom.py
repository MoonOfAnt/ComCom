from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
import serial
import serial.tools.list_ports
from threading import Thread
import time


# port_list = list(serial.tools.list_ports.comports())
# print(port_list)
# if len(port_list) == 0:
#     print('无可用串口')
# else:
#     for i in range(0, len(port_list)):
#         print(port_list[i])


class Stats:
    PARITY_BOX = {'无': 'N', '奇校验': 'O', '偶校验': 'E'}

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('ComCom.ui')

        self.port_find()
        # self.ui.button.clicked.connect(self.handleCalc)
        self.ui.Button_switch.clicked.connect(self.handle_serial_connect)
        self.ui.Button_2left.clicked.connect(self.handle_motor_2left)
        self.ui.Button_2right.clicked.connect(self.handle_motor_2right)
        self.ui.Button_Send_Text.clicked.connect(self.handle_serial_send_text)
        self.ui.Button_clearsend.clicked.connect(self.handle_clear_send)
        self.ui.Button_clearreceive.clicked.connect(self.handle_clear_receive)

        eval('self.ui.ButtonBox_'+str(0)+'.clicked.connect')(lambda: self.handle_ButtonBox(0))
        eval('self.ui.ButtonBox_'+str(1)+'.clicked.connect')(lambda: self.handle_ButtonBox(1))
        eval('self.ui.ButtonBox_'+str(2)+'.clicked.connect')(lambda: self.handle_ButtonBox(2))
        eval('self.ui.ButtonBox_'+str(3)+'.clicked.connect')(lambda: self.handle_ButtonBox(3))
        eval('self.ui.ButtonBox_'+str(4)+'.clicked.connect')(lambda: self.handle_ButtonBox(4))
        eval('self.ui.ButtonBox_'+str(5)+'.clicked.connect')(lambda: self.handle_ButtonBox(5))
        eval('self.ui.ButtonBox_'+str(6)+'.clicked.connect')(lambda: self.handle_ButtonBox(6))
        eval('self.ui.ButtonBox_'+str(7)+'.clicked.connect')(lambda: self.handle_ButtonBox(7))
        eval('self.ui.ButtonBox_'+str(8)+'.clicked.connect')(lambda: self.handle_ButtonBox(8))
        eval('self.ui.ButtonBox_'+str(9)+'.clicked.connect')(lambda: self.handle_ButtonBox(9))
        eval('self.ui.ButtonBox_'+str(10)+'.clicked.connect')(lambda: self.handle_ButtonBox(10))
        eval('self.ui.ButtonBox_'+str(11)+'.clicked.connect')(lambda: self.handle_ButtonBox(11))
        eval('self.ui.ButtonBox_'+str(12)+'.clicked.connect')(lambda: self.handle_ButtonBox(12))
        eval('self.ui.ButtonBox_'+str(13)+'.clicked.connect')(lambda: self.handle_ButtonBox(13))
        eval('self.ui.ButtonBox_'+str(14)+'.clicked.connect')(lambda: self.handle_ButtonBox(14))
        # for i in range(15):
        #     eval('self.ui.ButtonBox_'+str(i)+'.clicked.connect')(lambda: self.handle_ButtonBox(i))

    def port_find(self):
        port_list = list(serial.tools.list_ports.comports())
        print(port_list)
        if len(port_list) == 0:
            print('无可用串口')
        else:
            for i in range(0, len(port_list)):
                print(port_list[i])
                self.ui.comboBox_PortList.addItems([port_list[i].device])

    def handle_serial_connect(self):
        if self.ui.Button_switch.isChecked():
            try:
                self.serial = serial.Serial(self.ui.comboBox_PortList.currentText(),
                                            baudrate=int(self.ui.comboBox_baudrate.currentText()),
                                            stopbits=int(self.ui.comboBox_stopbits.currentText()),
                                            bytesize=int(self.ui.comboBox_bytesize.currentText()),
                                            parity=self.PARITY_BOX[self.ui.comboBox_parity.currentText()],
                                            timeout=1
                                            )  # 设置并打开串口
                self.thread1 = Thread(target=self.thread_receive)
                self.thread1.start()  # 启动接收显示线程
                self.ui.Label_remind.setText('串口已打开')
            except serial.serialutil.SerialException:
                self.ui.Label_remind.setText('无可用串口!')
                self.ui.Button_switch.setChecked(0)
            else:
                pass
        else:
            try:
                self.serial
            except NameError:
                pass
            else:
                self.serial.close()
                self.ui.Label_remind.setText('串口已关闭')

    def handle_serial_send_text(self):
        text = self.ui.Textedit_2send.toPlainText()
        if self.ui.checkBox_rn.isChecked():
            text = text + '\r\n'
        print(text)
        try:
            self.serial.write(text.encode())
        except(AttributeError, serial.serialutil.PortNotOpenError):
            print('串口未打开')
            self.ui.Label_remind.setText('串口未打开')

    def handle_motor_2left(self):
        print('111111')
        try:
            angles = self.ui.manual_step_angle.value()
            self.serial.write(("motor_2left %d\r\n" % angles).encode())
        except (AttributeError, serial.serialutil.PortNotOpenError):
            print('串口未打开')
            self.ui.Label_remind.setText('串口未打开')

    def handle_motor_2right(self):
        print('222222')
        try:
            angles = self.ui.manual_step_angle.value()
            self.serial.write(("motor_2right %d\r\n" % angles).encode())
        except (AttributeError, serial.serialutil.PortNotOpenError):
            print('串口未打开')
            self.ui.Label_remind.setText('串口未打开')

    def handle_clear_send(self):
        self.ui.Textedit_2send.clear()

    def handle_clear_receive(self):
        self.ui.Textedit_receive.clear()

    def handle_ButtonBox(self, n):
        print(n)
        if self.ui.checkBox_rn2.isChecked():
            self.serial.write((eval('self.ui.lineEdit_' + str(n) + '.text()') + '\r\n').encode())
        else:
            self.serial.write(eval('self.ui.lineEdit_' + str(n) + '.text()').encode())

    def thread_receive(self):
        while True:
            if self.serial.is_open:
                # self.ui.plainTextEdit_receive.appendPlainText("str_receive\r\n")
                # print(self.serial.in_waiting)
                if self.serial.in_waiting:
                    str_receive = self.serial.read_all().decode("gbk")
                    self.ui.Textedit_receive.appendPlainText(str_receive)
                    print('收到数据：', str_receive)
                time.sleep(1)
            else:
                break

    # def handle_ButtonBox(self, n):
    #     print(n)

    # def handleCalc(self):
    #     info = self.ui.textEdit.toPlainText()
    #
    #     salary_above_20k = ''
    #     salary_below_20k = ''
    #     for line in info.splitlines():
    #         if not line.strip():
    #             continue
    #         parts = line.split(' ')
    #
    #         parts = [p for p in parts if p]
    #         name,salary,age = parts
    #         if int(salary) >= 20000:
    #             salary_above_20k += name + '\n'
    #         else:
    #             salary_below_20k += name + '\n'
    #
    #     QMessageBox.about(self.ui,
    #                 '统计结果',
    #                 f'''薪资20000 以上的有：\n{salary_above_20k}
    #                 \n薪资20000 以下的有：\n{salary_below_20k}'''
    #                 )


app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()
