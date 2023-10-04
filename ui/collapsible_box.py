from PyQt5 import QtCore, QtWidgets

class NoteList(QtWidgets.QWidget):
    page_changed = QtCore.pyqtSignal(str)
    def __init__(self, title="", items=[], parent=None):
        super(NoteList, self).__init__(parent)
        
        self.title = title
        self.items = items
        self.is_collapsed = True

        self.setMaximumWidth(200)
        self.setMinimumWidth(0)

        # Create the main layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # widget dari note
        self.toggle_button = QtWidgets.QPushButton(self.title, self)
        self.toggle_button.setMinimumSize(50, 30)
        self.toggle_button.setMaximumHeight(30)
        self.toggle_button.clicked.connect(self.toggle_list)

        self.add_page_button = QtWidgets.QPushButton(self)
        self.add_page_button.clicked.connect(self.add_item)

        self.button_container = QtWidgets.QSplitter(self)
        self.button_container.setOrientation(QtCore.Qt.Horizontal)
        self.button_container.setMaximumHeight(50)
        self.button_container_layout = QtWidgets.QHBoxLayout(self.button_container)
        self.button_container_layout.setSpacing(0)
        self.button_container_layout.setContentsMargins(0,0,0,0)
        self.button_container_layout.addWidget(self.toggle_button, 4)
        self.button_container_layout.addWidget(self.add_page_button, 1)

        self.layout.addWidget(self.button_container)

        # buat menyimpan page
        self.item_pages = []
        self.list_frame = QtWidgets.QFrame(self)
        self.list_layout = QtWidgets.QVBoxLayout()
        self.list_layout.setContentsMargins(0, 5, 0, 5)
        self.list_layout.setSpacing(1)
        self.list_frame.setLayout(self.list_layout)
        self.layout.addWidget(self.list_frame)
        self.list_frame.hide()

        # animasi list
        self.toggle_animation = QtCore.QParallelAnimationGroup(self)
        animation = QtCore.QPropertyAnimation(self.list_frame, b"maximumHeight")
        animation.setStartValue(0)
        animation.setEndValue(16777215)
        animation.setDuration(300)
        animation = QtCore.QPropertyAnimation(self.list_frame, b"minimumHeight")
        animation.setStartValue(0)
        animation.setEndValue(50)
        animation.setDuration(300)
        self.toggle_animation.addAnimation(animation)

    # untuk menutup dan membuka note
    def toggle_list(self):
        self.is_collapsed = not self.is_collapsed

        if not self.is_collapsed:
            self.animation_done()

        self.toggle_animation.setDirection( QtCore.QAbstractAnimation.Forward if not self.is_collapsed else 
                                           QtCore.QAbstractAnimation.Backward )

        self.toggle_animation.start()

        self.toggle_animation.finished.connect(self.animation_done)

    def animation_done(self):
        self.list_frame.setVisible(not self.is_collapsed)
        for page in self.item_pages:
            page.setVisible(not self.is_collapsed)

    def pages_clicked(self):
        page = self.sender()
        self.page_changed.emit(page.objectName())

    def add_item(self, item_text:str = None, data:list = None):
        if not item_text or item_text == "":
            item_text = "Page-" + str(len(self.item_pages) + 1)

        page = Page(self)
        page.set_title(item_text)
        page.set_page_num(len(self.item_pages) + 1)
        page.setMinimumHeight(20)
        if data:
            page.get_rowcol(data[0], data[1])
            page.get_page_num(data[2])
        self.list_layout.addWidget(page)
        self.item_pages.append(page)
        self.list_frame.setMinimumHeight(self.list_layout.count() * 20)
        
        # change list_frame animation
        animetion = self.toggle_animation.animationAt(0)
        animetion.setEndValue(self.list_frame.minimumHeight())

        animation = QtCore.QPropertyAnimation(page, b"minimumHeight")
        animation.setStartValue(0)
        animation.setEndValue(20)
        animation.setDuration(300)
        self.toggle_animation.addAnimation(animation)
        
        animation = QtCore.QPropertyAnimation(page, b"maximumHeight")
        animation.setStartValue(0)
        animation.setEndValue(20)
        animation.setDuration(300)
        self.toggle_animation.addAnimation(animation)

        page.clicked.connect(lambda: self.page_changed.emit(item_text))

        if self.is_collapsed:
            page.hide()

        return page
    
    def remove_item(self, name:str):
        for index, page in enumerate(self.item_pages):
            if page.objectName() == name:
                page.deleteLater()
                self.item_pages.pop(index)
                # delete animation
                animation = self.toggle_animation.animationAt(index + 2)
                self.toggle_animation.removeAnimation(animation)
                animation = self.toggle_animation.animationAt(index + 3)
                self.toggle_animation.removeAnimation(animation)
                self.list_frame.setMinimumHeight(self.list_layout.count() * 20)
                break

    def get_num_pages(self):
        return len(self.item_pages)
    
    def get_pages(self):
        return self.item_pages
    
    def set_title(self, title:str):
        self.title = title
        self.toggle_page.setText(title)

    def get_pages(self):
        return self.item_pages

    def get_page_index(self, name) -> int:
        for index, page in enumerate(self.item_pages):
            if page.objectName() == name:
                return index
        return -1


class Page(QtWidgets.QPushButton):
    page_deleted = QtCore.pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super(Page, self).__init__(*args, **kwargs)
        self._rowcol = (3, 2)
        self._page_num = 1

    def showContextMenu(self, pos):
        menu = QtWidgets.QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == delete_action:
            self.page_deleted.emit(self.objectName())
            self.deleteLater()

    def set_rowcol(self, rowcol:tuple):
        self._rowcol = rowcol

    def get_rowcol(self) -> tuple:
        return self._rowcol
    
    def get_row(self) -> int:
        return self._rowcol[0]
    
    def get_col(self) -> int:
        return self._rowcol[1]
    
    def set_page_num(self, num:int) -> None:
        self._page_num = num

    def get_page_num(self) -> int:
        return self._page_num
    
    def set_title(self, title:str) -> None:
        self.setText(title)
        self.setObjectName(title)