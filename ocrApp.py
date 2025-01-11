# -*- coding: utf-8 -*-

import sys
import ctypes
from open_file_dialog import open_file_dialog
from switchpages import *
from crop import open_crop_window
from process_and_extract import *
from process_and_extract import processAndExtract
from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QTimer)
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QGradient, QIcon, QImage, QKeySequence, QLinearGradient, QPainter, QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel, QMainWindow, QPushButton, QSizePolicy, QSpacerItem, QStackedWidget, QTextEdit,QScrollArea, QVBoxLayout, QWidget, QGraphicsDropShadowEffect,QMessageBox)


class Ui_MainWindow(object):
    def call_switch_to_page1(self):
        switch_to_page1(self)  # Pass the MainWindow instance to the function

    def call_switch_to_page2(self):
        switch_to_page2(self)  # Pass the MainWindow instance to the function 

    def call_switch_to_page3(self):
        switch_to_page3(self)  #Pass the MainWindow instance to the function

    def confirm_selection(self):
        #Ensure that an image has been selected
        if hasattr(self, 'selected_image_path') and self.selected_image_path:
            # Get the image path selected in the file picker
            image_path = self.selected_image_path #This should be set during Image Selection

            #Call the external Function to process the image and extract text
            extracted_text = processAndExtract(image_path)

            # If the extracted text is a list, join it into a string
            if isinstance(extracted_text, list):
                medicine_names = extracted_text  #already a list of medicines
            else:
                medicine_names=extracted_text.split('\n') 

            # Populate medicine labels in the left layout (page 3)
            self.populate_medicine_labels(medicine_names)

            # Display extracted text in page3 (QTextEdit)
            # self.display_textedit.setPlainText(extracted_text)

            # Switch to page 3 to show the extracted text
            self.stackedWidget.setCurrentIndex(2)
        else:
            # Handle the case where no image was selected (optional)
            QMessageBox.warning(self, "No Image Selected", "Please select an image first.")  
    

    def show_copied_popup(self):
        # Create the label for the popup
        self.copied_label = QLabel("Text Copied", self)
        self.copied_label.setStyleSheet("background-color: None; color: black; font-size: 14px; padding: 5px;")
        self.copied_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Position the label near the home button
        self.copied_label.move(self.back_pushbutton.x() + self.back_pushbutton.width(), self.back_pushbutton.y())
        
        # Show the label and set a timer to hide it after 2 seconds
        self.copied_label.show()
        QTimer.singleShot(2000, self.copied_label.hide)  # Hide after 2 seconds

    def copy_text(self):

        #get text from the Qtextedit
        text = self.display_textedit.toPlainText()

        #Access the clipboard
        clipboard= QApplication.clipboard()
        clipboard.setText(text)

        self.show_copied_popup()


    def open_crop_window(self):
        if hasattr(self, 'selected_image_path') and self.selected_image_path:
                # Call the crop window and get the cropped image path
            cropped_image_path = open_crop_window(self.selected_image_path)

            if cropped_image_path:
                # Load the cropped image from file into a QPixmap
                cropped_image = QPixmap(cropped_image_path)  # Convert the file path to QPixmap

                # Display the cropped image in the QLabel
                self.preview_image_label.setPixmap(cropped_image)  # Update QLabel with QPixmap
                self.preview_image_label.setScaledContents(True)
                self.preview_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Pass the cropped image to the extraction engine
                extracted_text = processAndExtract(cropped_image_path)

                # Display extracted text in QTextEdit
                self.display_textedit.setPlainText(extracted_text)

                # Switch to page 3 to show the extracted text
                self.stackedWidget.setCurrentIndex(2)
            else:
                print("Cropping was canceled or failed.")
        else:
                # Handle the case where no image was selected
            QMessageBox.warning(self, "No Image Selected", "Please select an image first.")




    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(865, 697)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet(u"QMainWindow{\n"
"background-color: #FFFFFF\n"
"}")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.verticalLayout_3 = QVBoxLayout(self.page_1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 10)
        self.mainHeading_1 = QLabel(self.page_1)
        self.mainHeading_1.setObjectName(u"mainHeading_1")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.mainHeading_1.sizePolicy().hasHeightForWidth())
        self.mainHeading_1.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setFamilies([u"Berlin Sans FB Demi"])
        font.setPointSize(33)
        font.setBold(True)
        font.setItalic(False)
        self.mainHeading_1.setFont(font)
        self.mainHeading_1.setStyleSheet(u"QLabel{\n"
"color:#6B7075\n"
"}")
        self.mainHeading_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainHeading_1.setMargin(0)

        self.verticalLayout_2.addWidget(self.mainHeading_1)

        self.tagline = QLabel(self.page_1)
        self.tagline.setObjectName(u"tagline")
        sizePolicy1.setHeightForWidth(self.tagline.sizePolicy().hasHeightForWidth())
        self.tagline.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(True)
        self.tagline.setFont(font1)
        self.tagline.setStyleSheet(u"QLabel{\n"
"color:#6B7075\n"
"}")
        self.tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.tagline)

        self.line_3 = QFrame(self.page_1)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")

        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.home_image_2 = QLabel(self.page_1)
        self.home_image_2.setObjectName(u"home_image_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.home_image_2.sizePolicy().hasHeightForWidth())
        self.home_image_2.setSizePolicy(sizePolicy2)
        self.home_image_2.setPixmap(QPixmap(r"resource\home_image.png"))
        self.home_image_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.home_image_2)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        
        #Initialize the Stacked widget with pages
        self.stackedWidget= QStackedWidget(self)

        self.pick_image_pushbutton = QPushButton(self.page_1)
        self.pick_image_pushbutton.setObjectName(u"pick_image_pushbutton")
        self.pick_image_pushbutton.clicked.connect(lambda: open_file_dialog(self))
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pick_image_pushbutton.sizePolicy().hasHeightForWidth())
        self.pick_image_pushbutton.setSizePolicy(sizePolicy3)
        self.pick_image_pushbutton.setMinimumSize(QSize(40, 30))
        self.pick_image_pushbutton.setMaximumSize(QSize(170, 90))
        font2 = QFont()
        font2.setFamilies([u"Calibri"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.pick_image_pushbutton.setFont(font2)
        self.pick_image_pushbutton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pick_image_pushbutton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pick_image_pushbutton.setStyleSheet(u"QPushButton\n"
"{\n"
"color:#ffffff;\n"
"background-color:#9c9c9c;\n"
"border-radius:9;\n"
"transition: background-color 0.5s ease-in-out, \n"
"                color 0.5s ease-in-out, \n"
"                padding 0.2s ease-in-out, \n"
"border:1px solid #cccccc;\n"
"}\n"
"QPushButton:hover\n"
"{\n"
"color:#111111;\n"
"background-color:#ffffff;\n"
"transition: background-color 1s ease-in-out, \n"
"            color 1s ease-in-out, \n"
"            padding 0.2s ease-in-out, \n"
"border:1px solid #cccccc\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #38454C;  /* Darker background when pressed */\n"
"    padding-top: 5px;  /* Slightly decrease padding for pressed effect */\n"
"    padding-left: 10px;  /* Slightly decrease padding for pressed effect */\n"
"}")

        self.horizontalLayout_2.addWidget(self.pick_image_pushbutton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.line_4 = QFrame(self.page_1)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_4)

        self.label_3 = QLabel(self.page_1)
        self.label_3.setObjectName(u"label_3")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy4)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_3)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.stackedWidget.addWidget(self.page_1)

        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_5 = QVBoxLayout(self.page_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(40, 20, 40, 20)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, -1, -1, 20)
        self.label_2 = QLabel(self.page_2)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)
        self.label_2.setMaximumSize(QSize(40, 40))
        self.label_2.setStyleSheet(u"QLabel{\n"
"color:#FFFFFF\n"
"}")
        self.label_2.setPixmap(QPixmap(u"resource/fileicon.png"))
        self.label_2.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.label_2)

        self.label = QLabel(self.page_2)
        self.label.setObjectName(u"label")
        font3 = QFont()
        font3.setFamilies([u"Berlin Sans FB Demi"])
        font3.setPointSize(20)
        font3.setBold(True)
        self.label.setFont(font3)
        self.label.setStyleSheet(u"QLabel{\n"
"color:#6B7075\n"
"}")

        self.horizontalLayout_4.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.widget = QWidget(self.page_2)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"QWidget {\n"
"    background-color: #e6f7ff;  /* Light blue color */\n"
"    border-bottom: 1px solid #b3d7ff;  /* Optional border for separation */\n"
"}\n"
"")

        self.horizontalLayout_4.addWidget(self.widget)

        self.home1_pushbutton = QPushButton(self.page_2)
        self.home1_pushbutton.setObjectName(u"home1_pushbutton")
        self.home1_pushbutton.setFont(font2)
        self.home1_pushbutton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.home1_pushbutton.setStyleSheet(u"QPushButton {\n"
"    background-color: #9c9c9c;  /* Default button color */\n"
"    color: white;\n"
"    border-radius: 10px;\n"    
"    padding: 8px;\n"
"}\n"
"\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(255, 255, 255, 0.3);  /* Soft white glow */\n"
"    color: #000000;\n"
"    border: 1px solid #cccccc;\n"
"}")  

        self.home1_pushbutton.clicked.connect(self.call_switch_to_page1)
        

        self.horizontalLayout_4.addWidget(self.home1_pushbutton)
        self.extractedText_pushbutton = QPushButton(self.page_2)
        self.extractedText_pushbutton.setObjectName(u"extractedText_pushbutton")
        self.extractedText_pushbutton.setFont(font2)
        self.extractedText_pushbutton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.extractedText_pushbutton.setStyleSheet(u"QPushButton {\n"
"    background-color: #9c9c9c;  /* Default button color */\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"    padding: 8px;\n"
"}\n"
"\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(255, 255, 255, 0.3);  /* Soft white glow */\n"
"    color: #000000;\n"
"    border: 1px solid #cccccc;\n"
"}")

        self.extractedText_pushbutton.clicked.connect(self.call_switch_to_page3)
        self.horizontalLayout_4.addWidget(self.extractedText_pushbutton)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.line = QFrame(self.page_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.crop_pushbutton = QPushButton(self.page_2)
        self.crop_pushbutton.setObjectName(u"crop_pushbutton")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.crop_pushbutton.sizePolicy().hasHeightForWidth())
        self.crop_pushbutton.setSizePolicy(sizePolicy5)
        self.crop_pushbutton.setMinimumSize(QSize(0, 16))
        self.crop_pushbutton.setMaximumSize(QSize(16777215, 30))
        font4 = QFont()
        font4.setFamilies([u"Bahnschrift SemiCondensed"])
        font4.setPointSize(12)
        self.crop_pushbutton.setFont(font4)
        self.crop_pushbutton.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u"resource/crop.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.crop_pushbutton.setIcon(icon)
        self.crop_pushbutton.setIconSize(QSize(18, 18))
        self.crop_pushbutton.clicked.connect(self.open_crop_window)

        self.verticalLayout.addWidget(self.crop_pushbutton)

        self.preview_frame = QFrame(self.page_2)
        self.preview_frame.setObjectName(u"preview_frame")
        sizePolicy2.setHeightForWidth(self.preview_frame.sizePolicy().hasHeightForWidth())
        self.preview_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.preview_frame.setStyleSheet(u"QFrame {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0, x2: 1, y2: 1,\n"
"        stop: 0 #c0c0c0,\n"
"        stop: 1 #e0e0e0\n"
"    );\n"
"	border:2px black;\n"
"    border-radius: 10px;\n"
"}\n"
"")
        self.preview_layout= QVBoxLayout(self.preview_frame)
        # Add QLabel to preview_frame
        self.preview_image_label = QLabel(self.preview_frame)
        self.preview_image_label.setObjectName("image_label")
        self.preview_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_image_label.setStyleSheet("background-color: #f0f0f0; border-radius: 8px;")  # Optional background color for visibility
        self.preview_image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.preview_image_label.setText("No Image Selected")  # Optional: Set placeholder text

        self.preview_layout.addWidget(self.preview_image_label)

        self.preview_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.preview_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.preview_frame)


        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(20, 30, 20, 50)
        self.confirm_pushbutton = QPushButton(self.page_2)
        self.confirm_pushbutton.setObjectName(u"confirm_pushbutton")
        sizePolicy3.setHeightForWidth(self.confirm_pushbutton.sizePolicy().hasHeightForWidth())
        self.confirm_pushbutton.setSizePolicy(sizePolicy3)
        self.confirm_pushbutton.setMinimumSize(QSize(120, 0))
        self.confirm_pushbutton.setMaximumSize(QSize(160, 16777215))
        self.confirm_pushbutton.setFont(font2)
        self.confirm_pushbutton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.confirm_pushbutton.setStyleSheet(u"QPushButton {\n"
"    background-color: #9c9c9c;  /* Default button color */\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"    padding: 8px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"   background-color: rgba(255, 255, 255, 0.3);  /* Soft white glow */\n"
"    color: #000000;\n"
"    border: 1px solid #cccccc;\n"
"}")
        self.confirm_pushbutton.clicked.connect(self.confirm_selection)

        self.horizontalLayout_5.addWidget(self.confirm_pushbutton)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.line_2 = QFrame(self.page_2)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.label_contact = QLabel(self.page_2)
        self.label_contact.setObjectName(u"label_contact")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_contact.sizePolicy().hasHeightForWidth())
        self.label_contact.setSizePolicy(sizePolicy6)
        self.label_contact.setStyleSheet(u"")
        self.label_contact.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout.addWidget(self.label_contact)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")

        self.verticalLayout.addLayout(self.verticalLayout_9)

        self.frame_2 = QFrame(self.page_2)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frame_2)


        self.verticalLayout_5.addLayout(self.verticalLayout)
        self.stackedWidget.addWidget(self.page_2)
        
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")

        self.page_3_layout=QVBoxLayout(self.page_3)
        self.page_3_layout.setSpacing(0)
        self.page_3_layout.setContentsMargins(10, 10, 10, 10)

        heading_font=QFont()
        heading_font.setFamilies([u"Berlin Sans FB Demi"])
        heading_font.setPointSize(33)
        heading_font.setBold(True)
        heading_font.setItalic(False)

        # Create and configure the heading label
        self.heading_label = QLabel("RxVision")
        self.heading_label.setFont(heading_font)
        self.heading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.heading_label.setStyleSheet("color: #6B7075;")
        self.heading_label.setFixedHeight(60) #fixed height for the header
        self.page_3_layout.addWidget(self.heading_label)

        # Create a horizontal layout for left and right panels
        self.content_layout = QHBoxLayout()

        #Create a left Panel
        self.left_scroll_area= QScrollArea()
        self.left_scroll_area.setWidgetResizable(True)
        self.left_panel=QWidget()
        self.left_layout=QVBoxLayout(self.left_panel)
        self.left_panel.setStyleSheet("background-color: #f0f0f0; border-radius: 8px;")
        self.left_layout.setSpacing(10)
        self.left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Optionally add a stretch to push items to the top
        self.left_layout.addStretch()
        self.left_panel.setLayout(self.left_layout)

        #Create a right Panel
        self.right_panel=QWidget()
        self.right_layout=QVBoxLayout(self.right_panel)
        self.right_panel.setStyleSheet("background-color: #f0f0f0; border-radius: 8px;")

        #Add both the panel to the main widget
        self.content_layout.addWidget(self.left_panel,35)
        self.content_layout.addWidget(self.right_panel,65)

        # Add content layout to a middle widget
        self.middle_widget = QWidget()
        self.middle_layout = QVBoxLayout(self.middle_widget)
        self.middle_layout.setContentsMargins(0, 0, 0, 0)
        self.middle_layout.addLayout(self.content_layout)

        # Add the content layout to the main page layout
        self.page_3_layout.addWidget(self.middle_widget)

        self.footer_page3=QWidget()
        self.footer_page3_layout=QVBoxLayout(self.footer_page3)
        self.footer_page3_layout.setContentsMargins(0,0,0,0)

        self.footer_label= QLabel("Contact Us @: janhavipal353@gmail.com/aujale30@gmail.com")
        footerfont=QFont()
        footerfont.setFamilies([u"Arial"])
        footerfont.setPointSize(9)

        self.footer_label.setFont(footerfont)
        self.footer_label.setStyleSheet("color: #6B7075;")
        self.footer_page3_layout.addWidget(self.footer_label)
        self.footer_page3.setFixedHeight(50)
        self.page_3_layout.addWidget(self.footer_page3,0)

        self.stackedWidget.addWidget(self.page_3)

        self.verticalLayout_4.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"RxVision", None))
#if QT_CONFIG(whatsthis)
        self.centralwidget.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>QStackedWidget</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.mainHeading_1.setText(QCoreApplication.translate("MainWindow", u"RxVision", None))
        self.tagline.setText(QCoreApplication.translate("MainWindow", u"\"Effortlessly extract text from any image with our advanced OCR technology\"", None))
        self.home_image_2.setText("")
        self.pick_image_pushbutton.setText(QCoreApplication.translate("MainWindow", u"Pick an Image", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"All Rights Reserved", None))
        self.label_2.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"RxVision", None))
        self.home1_pushbutton.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.extractedText_pushbutton.setText(QCoreApplication.translate("MainWindow", u"Extracted text Display", None))
        self.crop_pushbutton.setText(QCoreApplication.translate("MainWindow", u"Crop", None))
        self.confirm_pushbutton.setText(QCoreApplication.translate("MainWindow", u"Confirm Selection", None))
        self.label_contact.setText(QCoreApplication.translate("MainWindow", u"Contact Us @: janhavipal353@gmail.com / aujale30@gmail.com", None))

    def populate_medicine_labels(self,medicine_names):
        font5 = QFont()
        font5.setFamilies([u"Calibri"])
        font5.setPointSize(13)
        font5.setBold(False)
        font5.setItalic(False)

        #clear existing labels
        while self.left_layout.count():
            item = self.left_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        #Add medicine label or display no medicine detected
        if medicine_names:
            for index,name in enumerate (medicine_names):
                label= QLabel(f"{index + 1}. {name}")  #Add Numbering
                label.setFont(font5)
                label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                label.setStyleSheet("QLabel{background-color: #ffffff; border: 1px solid #cccccc; border-radius:8px; padding:10px}"
                                    "QLabel:hover{background-color: #cdcece;color:#ffffff}"
                                    )
                
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.left_layout.addWidget(label)
        else:
            no_medicine_label = QLabel("No medicine detected")
            no_medicine_label.setFont(font5)
            no_medicine_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            no_medicine_label.setStyleSheet("QLabel{background-color: #ffffff; border: 1px solid #cccccc; border-radius:8px; padding:10px}"
                                    "QLabel:hover{background-color: #cdcece;color:#ffffff}"
                                    )
            no_medicine_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.left_layout.addWidget(no_medicine_label)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.pick_image_pushbutton.clicked.connect(self.open_file_dialog)
        # Set window title
        self.setWindowTitle("OCR Application")
        
        # Set window icon
        self.setWindowIcon(QIcon(r"resource\windowicon.ico"))


if __name__ == "__main__":
        app= QApplication(sys.argv)
        window= MainWindow()

        window.show()
        sys.exit(app.exec())