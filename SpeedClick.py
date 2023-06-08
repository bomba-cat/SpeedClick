# ______     ______   ______     ______     _____     ______     __         __     ______     __  __    
#/\  ___\   /\  == \ /\  ___\   /\  ___\   /\  __-.  /\  ___\   /\ \       /\ \   /\  ___\   /\ \/ /    
#\ \___  \  \ \  _-/ \ \  __\   \ \  __\   \ \ \/\ \ \ \ \____  \ \ \____  \ \ \  \ \ \____  \ \  _"-.  
# \/\_____\  \ \_\    \ \_____\  \ \_____\  \ \____-  \ \_____\  \ \_____\  \ \_\  \ \_____\  \ \_\ \_\ 
#  \/_____/   \/_/     \/_____/   \/_____/   \/____/   \/_____/   \/_____/   \/_/   \/_____/   \/_/\/_/ 
# ______     ______     ______     __     __     ______     ______     ______    
#/\  == \   /\  == \   /\  __ \   /\ \  _ \ \   /\  ___\   /\  ___\   /\  == \   
#\ \  __<   \ \  __<   \ \ \/\ \  \ \ \/ ".\ \  \ \___  \  \ \  __\   \ \  __<   
# \ \_____\  \ \_\ \_\  \ \_____\  \ \__/".~\_\  \/\_____\  \ \_____\  \ \_\ \_\ 
#  \/_____/   \/_/ /_/   \/_____/   \/_/   \/_/   \/_____/   \/_____/   \/_/ /_/ 

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

import os
import sys


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("SpeedClick")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('images', 'ma-icon-128.png')))
        layout.addWidget(logo)

        layout.addWidget(QLabel("Version Beta 69.69.6969"))
        layout.addWidget(QLabel("Open Source, Code found on GitHub"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('images', 'arrow-180.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join('images', 'arrow-000.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join('images', 'arrow-circle-315.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join('images', 'home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction(QIcon(os.path.join('images', 'cross-circle.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        # Nimmt man diesen code hier hinein kann man für Macs den default MenuBar Weg nehmen da
        # Apple in an sonsten von selber hinein Packt falls das Prefferiert wird.
        # self.menuBar().setNativeMenuBar(False)

        file_menu = self.menuBar().addMenu("&File")

        new_tab_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        open_file_action = QAction(QIcon(os.path.join('images', 'disk--arrow.png')), "Open file...", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save Page As...", self)
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction(QIcon(os.path.join('images', 'question.png')), "About SpeedClick", self)
        about_action.setStatusTip("Find out more about SpeedClick")
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        navigate_speedclick_action = QAction(QIcon(os.path.join('images', 'lifebuoy.png')),
                                            "SpeedClick Homepage", self)
        navigate_speedclick_action.setStatusTip("Go to SpeedClick Homepage")
        navigate_speedclick_action.triggered.connect(self.navigate_SpeedClick)
        help_menu.addAction(navigate_speedclick_action)

        self.add_new_tab(QUrl('https://sites.google.com/view/SpeedClickBrowser'), 'Homepage')

        self.showMaximized()

        self.setWindowTitle("SpeedClick")
        self.setWindowIcon(QIcon(os.path.join('images', 'ma-icon-64.png')))

    def add_new_tab(self, qurl=None, label="Blank"):

        if qurl is None:
            qurl = QUrl('https://duckduckgo.com')

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:  # Kein Tab unter dem Click bereich
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            # Wenn dieses Signal vom jetztigen Tab ist dann einf Ignorieren.
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s - SpeedClick" % title)

    def navigate_SpeedClick(self):
        self.tabs.currentWidget().setUrl(QUrl("https://sites.google.com/view/SpeedClickBrowser"))

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "Hypertext Markup Language (*.htm *.html);;"
                                                  "All files (*.*)")

        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.tabs.currentWidget().setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                                  "Hypertext Markup Language (*.htm *html);;"
                                                  "All files (*.*)")

        if filename:
            html = self.tabs.currentWidget().page().toHtml()
            with open(filename, 'w') as f:
                f.write(html.encode('utf8'))

    def print_page(self):
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.browser.print_)
        dlg.exec_()

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://sites.google.com/view/SpeedClickBrowser"))

    def navigate_to_url(self):  # Kriegt keine URL
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            if str(q).count(".") > 2:
                q.setScheme("http")
            else:
                q = QUrl("https://duckduckgo.com/?q="+q.toString()+"&t=h_&ia=web")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            # Wenn dieses Signal nicht vom jetztigen Tab ist, dann ignorieren
            return
        if q.scheme() == 'https':
            # Secure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-ssl.png')))

        elif q.scheme() == 'http':
            # Insecure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName("SpeedClick")
app.setOrganizationName("SpeedClick")
app.setOrganizationDomain("https://sites.google.com/view/SpeedClickBrowser")

window = MainWindow()

app.exec_()
