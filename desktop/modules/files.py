from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog,
    QFormLayout, QComboBox, QLineEdit, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from widgets import populate_table


class FilesModule(QWidget):
    COLUMN_NAMES = {
        'original_name': 'Имя файла',
        'file_category': 'Категория',
        'entity_type': 'Тип объекта',
        'entity_name': 'Объект',
        'uploaded_by_name': 'Загрузил',
        'uploaded_at': 'Дата загрузки',
    }

    CATEGORIES = {
        'drawing': 'Чертёж',
        'contract': 'Договор',
        'model': '3D-модель',
        'program': 'Управляющая программа',
        'report': 'Отчёт',
        'payment': 'Платёжный документ',
        'hr': 'Кадровый документ',
        'equipment': 'Паспорт оборудования',
        'other': 'Прочее',
    }

    def __init__(self, api_client, is_director=True):
        super().__init__()
        self.api = api_client
        self.is_director = is_director
        self.current_data = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        title = QLabel("Файлы")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        if self.is_director:
            btn_layout = QHBoxLayout()
            btn_add = QPushButton("+ Загрузить файл")
            btn_add.clicked.connect(self.add_file)
            btn_edit = QPushButton("Редактировать")
            btn_edit.clicked.connect(self.edit_file)
            btn_layout.addWidget(btn_edit)
            btn_delete = QPushButton("Удалить")
            btn_delete.clicked.connect(self.delete_file)
            btn_layout.addWidget(btn_add)
            btn_layout.addWidget(btn_delete)
            btn_layout.addStretch()
            layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        self.load_data()


    def edit_file(self):
        file_id = self.get_selected_id()
        if not file_id:
            return
        dialog = FileDialog(self.api, file_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()

    def load_data(self):
        resp = self.api.get("files/")
        if resp.status_code == 200:
            raw = resp.json() if isinstance(resp.json(), list) else resp.json().get('results', [])
            allowed = set(self.COLUMN_NAMES.keys()) | {'id'}
            self.current_data = []
            for item in raw:
                item['file_category'] = self.CATEGORIES.get(item.get('file_category', ''), item.get('file_category', ''))
                item['entity_type'] = item.get('content_type_name', '')
                item['entity_name'] = item.get('object_name', '')
                item['uploaded_by_name'] = item.get('uploaded_by_name', '')
                item['uploaded_at'] = item.get('uploaded_at', '')[:10] if item.get('uploaded_at') else ''
                filtered = {k: v for k, v in item.items() if k in allowed}
                self.current_data.append(filtered)
            populate_table(self.table, self.current_data, self.COLUMN_NAMES)
        else:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить: {resp.status_code}")

    def get_selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите файл")
            return None
        return self.current_data[row].get('id')

    def add_file(self):
        dialog = FileDialog(self.api)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()

    def delete_file(self):
        file_id = self.get_selected_id()
        if not file_id:
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить файл?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            resp = self.api.delete(f"files/{file_id}/")
            if resp.status_code == 204:
                self.load_data()
            else:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить: {resp.status_code}")


class FileDialog(QDialog):
    ENTITY_TYPES = {
        'request': 'Заявка',
        'order': 'Заказ',
        'product': 'Изделие',
        'employee': 'Сотрудник',
        'equipment': 'Оборудование',
        'income': 'Доход',
        'expense': 'Расход',
    }

    CATEGORIES = [
        ('drawing', 'Чертёж'),
        ('contract', 'Договор'),
        ('model', '3D-модель'),
        ('program', 'Управляющая программа'),
        ('report', 'Отчёт'),
        ('payment', 'Платёжный документ'),
        ('hr', 'Кадровый документ'),
        ('equipment', 'Паспорт оборудования'),
        ('other', 'Прочее'),
    ]

    def __init__(self, api_client, file_id=None):
        super().__init__()
        self.api = api_client
        self.file_id = file_id
        self.setWindowTitle("Загрузить файл")
        self.setMinimumWidth(450)
        self.file_path = None
        self.init_ui()
        if file_id:
            self._load_file()

    def init_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        self.type_combo = QComboBox()
        for key, label in self.ENTITY_TYPES.items():
            self.type_combo.addItem(label, key)
        form.addRow("Тип объекта", self.type_combo)
        self.type_combo.currentIndexChanged.connect(self._load_objects)

        # self.object_id = QLineEdit()
        # self.object_id.setPlaceholderText("Введите ID объекта")
        # form.addRow("ID объекта", self.object_id)
        self.object_combo = QComboBox()
        self.object_combo.setEditable(True)  # можно искать по тексту
        form.addRow("Объект", self.object_combo)

        self.category_combo = QComboBox()
        for key, label in self.CATEGORIES:
            self.category_combo.addItem(label, key)
        form.addRow("Категория", self.category_combo)

        self.description = QLineEdit()
        form.addRow("Описание", self.description)

        self.file_label = QLabel("Файл не выбран")
        btn_choose = QPushButton("Выбрать файл")
        btn_choose.clicked.connect(self._choose_file)
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(btn_choose)
        form.addRow("Файл", file_layout)

        layout.addLayout(form)
        btn_save = QPushButton("Загрузить")
        btn_save.clicked.connect(self.save)
        layout.addWidget(btn_save)
        self.setLayout(layout)

    def _load_objects(self):
        """Загружает список объектов выбранного типа."""
        entity_type = self.type_combo.currentData()
        self.object_combo.clear()

        endpoint_map = {
            'request': 'requests/',
            'order': 'orders/',
            'product': 'products/',
            'employee': 'employees/',
            'equipment': 'equipment/',
            'income': 'incomes/',
            'expense': 'expenses/',
        }
        endpoint = endpoint_map.get(entity_type)
        if not endpoint:
            return

        resp = self.api.get(endpoint)
        if resp.status_code == 200:
            data = resp.json() if isinstance(resp.json(), list) else resp.json().get('results', [])
            for item in data:
                label = self._format_item(entity_type, item)
                self.object_combo.addItem(label, item.get('id'))

    def _format_item(self, entity_type, item):
        if entity_type == 'request':
            return f"Заявка №{item.get('id')} от {item.get('customer_name', '')}"
        if entity_type == 'order':
            return f"Заказ №{item.get('id')} — {item.get('product_name', '')}"
        if entity_type == 'product':
            return item.get('name', '')
        if entity_type == 'employee':
            return item.get('full_name', '')
        if entity_type == 'equipment':
            return item.get('name', '')
        if entity_type == 'income':
            return f"Доход №{item.get('id')} — {item.get('amount', '')} руб."
        if entity_type == 'expense':
            return f"Расход №{item.get('id')} — {item.get('amount', '')} руб."
        return str(item.get('id', ''))

    def _choose_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выбрать файл")
        if path:
            self.file_path = path
            self.file_label.setText(path.split('/')[-1])

    def save(self):
        if self.file_id:
            # Редактирование метаданных (без замены файла)
            data = {
                'object_id': self.object_combo.currentData(),
                'file_category': self.category_combo.currentData(),
                'description': self.description.text(),
            }
            resp = self.api.put(f"files/{self.file_id}/", data)
            if resp.status_code in [200, 201]:
                self.accept()
            else:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить: {resp.status_code}\n{resp.text}")
        else:
            # Загрузка нового файла
            if not self.file_path:
                QMessageBox.warning(self, "Ошибка", "Выберите файл")
                return
            resp = self.api.upload('files/', {
                'content_type': self.type_combo.currentData(),
                'object_id': self.object_combo.currentData(),
                'file_category': self.category_combo.currentData(),
                'description': self.description.text(),
                'original_name': self.file_path.split('/')[-1],
            }, file_path=self.file_path)

            if resp.status_code == 201:
                self.accept()
            else:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить: {resp.status_code}\n{resp.text}")

    def _load_file(self):
        resp = self.api.get(f"files/{self.file_id}/")
        if resp.status_code == 200:
            d = resp.json()
            idx = self.type_combo.findData(d.get('content_type'))
            if idx >= 0:
                self.type_combo.setCurrentIndex(idx)
            # Загружаем объекты нужного типа, затем выбираем нужный
            self._load_objects()
            obj_id = d.get('object_id')
            if obj_id:
                idx = self.object_combo.findData(obj_id)
                if idx >= 0:
                    self.object_combo.setCurrentIndex(idx)
            idx = self.category_combo.findData(d.get('file_category'))
            if idx >= 0:
                self.category_combo.setCurrentIndex(idx)
            self.description.setText(d.get('description', ''))
            self.file_label.setText(d.get('original_name', ''))