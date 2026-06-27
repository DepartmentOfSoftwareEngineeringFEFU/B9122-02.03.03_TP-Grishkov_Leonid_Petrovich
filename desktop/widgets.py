from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QFileDialog, QMessageBox, QHBoxLayout
)
import os
import sys
import tempfile
import subprocess

class NumericTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except (ValueError, TypeError):
            return super().__lt__(other)


def try_parse_number(value):
    """Пробует преобразовать значение в int или float. None если не число."""
    if value is None or value == "":
        return None
    try:
        s = str(value)
        if '.' in s or 'e' in s.lower():
            return float(s)
        return int(s)
    except (ValueError, TypeError):
        return None


# def populate_table(table, data, column_names=None):
#     """Заполняет QTableWidget данными из списка словарей."""
#     table.setSortingEnabled(False)
#     table.clear()
#     table.setRowCount(0)
#     table.setColumnCount(0)

#     if not data:
#         table.setColumnCount(1)
#         table.setHorizontalHeaderLabels(["Нет данных"])
#         table.setSortingEnabled(True)
#         return

#     sample = data[0]
#     columns = [k for k in sample.keys() if k != 'id']
#     headers = [column_names.get(c, c) if column_names else c for c in columns]
#     table.setColumnCount(len(columns))
#     table.setHorizontalHeaderLabels(headers)
#     table.setRowCount(len(data))

#     for i, item in enumerate(data):
#         for j, col in enumerate(columns):
#             value = item.get(col, "")
#             numeric_value = try_parse_number(value)
#             if numeric_value is not None:
#                 if isinstance(numeric_value, float):
#                     table_item = NumericTableWidgetItem(f"{numeric_value:.2f}")
#                 else:
#                     table_item = NumericTableWidgetItem(str(numeric_value))
#             else:
#                 table_item = QTableWidgetItem(str(value))
#             table.setItem(i, j, table_item)

#     table.setSortingEnabled(True)
#     table.resizeColumnsToContents()

def populate_table(table, data, column_names=None):
    table.setSortingEnabled(False)
    table.clear()
    table.setRowCount(0)
    table.setColumnCount(0)

    if not data:
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels(["Нет данных"])
        table.setSortingEnabled(True)
        return

    # Порядок колонок — из column_names, если передан
    if column_names:
        columns = list(column_names.keys())
    else:
        sample = data[0]
        columns = [k for k in sample.keys() if k != 'id']

    headers = [column_names.get(c, c) if column_names else c for c in columns]
    table.setColumnCount(len(columns))
    table.setHorizontalHeaderLabels(headers)
    table.setRowCount(len(data))

    for i, item in enumerate(data):
        for j, col in enumerate(columns):
            value = item.get(col, "")
            numeric_value = try_parse_number(value)
            if numeric_value is not None:
                if isinstance(numeric_value, float):
                    table_item = NumericTableWidgetItem(f"{numeric_value:.2f}")
                else:
                    table_item = NumericTableWidgetItem(str(numeric_value))
            else:
                table_item = QTableWidgetItem(str(value))
            table.setItem(i, j, table_item)

    table.setSortingEnabled(True)
    table.resizeColumnsToContents()


def save_table_to_file(parent, table, default_name):
    from PyQt5.QtWidgets import QFileDialog, QMessageBox
    import os

    filepath, _ = QFileDialog.getSaveFileName(
        parent, "Сохранить отчёт",
        os.path.expanduser(f"~\\Desktop\\{default_name}.txt"),
        "Текстовые файлы (*.txt);;CSV (*.csv)"
    )
    if not filepath:
        return

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            headers = [table.horizontalHeaderItem(j).text() for j in range(table.columnCount())]
            f.write('\t'.join(headers) + '\n')
            for i in range(table.rowCount()):
                row = [table.item(i, j).text() if table.item(i, j) else '' for j in range(table.columnCount())]
                f.write('\t'.join(row) + '\n')
        QMessageBox.information(parent, "Готово", f"Отчёт сохранён:\n{filepath}")
    except Exception as e:
        QMessageBox.critical(parent, "Ошибка", f"Не удалось сохранить: {e}")

def save_report(parent, title, table, summary_rows=None, params=None):
    """Сохраняет отчёт в текстовый файл с заголовком, таблицей и итогами."""
    from PyQt5.QtWidgets import QFileDialog, QMessageBox
    from datetime import datetime
    import os

    filepath, _ = QFileDialog.getSaveFileName(
        parent, "Сохранить отчёт",
        os.path.expanduser(f"~\\Desktop\\{title}.txt"),
        "Текстовые файлы (*.txt);;CSV (*.csv)"
    )
    if not filepath:
        return

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            # Шапка
            f.write(f"{'=' * 60}\n")
            f.write(f"  {title}\n")
            f.write(f"  Дата создания: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            if params:
                for key, value in params.items():
                    f.write(f"  {key}: {value}\n")
            f.write(f"{'=' * 60}\n\n")

            # Таблица
            if table.rowCount() > 0:
                headers = [table.horizontalHeaderItem(j).text() for j in range(table.columnCount())]
                col_widths = [len(h) for h in headers]

                for i in range(table.rowCount()):
                    for j in range(table.columnCount()):
                        text = table.item(i, j).text() if table.item(i, j) else ''
                        col_widths[j] = max(col_widths[j], len(text))

                header_line = ' | '.join(h.ljust(col_widths[k]) for k, h in enumerate(headers))
                f.write(header_line + '\n')
                f.write('-' * len(header_line) + '\n')

                for i in range(table.rowCount()):
                    row = [table.item(i, j).text() if table.item(i, j) else '' for j in range(table.columnCount())]
                    f.write(' | '.join(v.ljust(col_widths[k]) for k, v in enumerate(row)) + '\n')

            # Итоги
            if summary_rows:
                f.write('\n' + '-' * 60 + '\n')
                for row in summary_rows:
                    f.write(f"  {row}\n")
                f.write('=' * 60 + '\n')

        QMessageBox.information(parent, "Готово", f"Отчёт сохранён:\n{filepath}")
    except Exception as e:
        QMessageBox.critical(parent, "Ошибка", f"Не удалось сохранить: {e}")




class FileListWidget(QWidget):
    """Виджет для отображения и управления файлами сущности."""

    def __init__(self, api_client, content_type, object_id=None, is_director=True):
        super().__init__()
        self.api = api_client
        self.content_type = content_type
        self.object_id = object_id
        self.is_director = is_director
        self.current_files = []
        self.init_ui()
        if object_id:
            self.load_files()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 0)

        label = QLabel("Прикреплённые файлы:")
        layout.addWidget(label)

        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Имя файла", "Категория", "Размер"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setMaximumHeight(120)
        layout.addWidget(self.table)

        if self.is_director:
            btn_layout = QHBoxLayout()
            btn_add = QPushButton("Загрузить")
            btn_add.clicked.connect(self.add_file)
            btn_open = QPushButton("Открыть")
            btn_open.clicked.connect(self.open_file)
            btn_del = QPushButton("Удалить")
            btn_del.clicked.connect(self.delete_file)
            btn_layout.addWidget(btn_add)
            btn_layout.addWidget(btn_open)
            btn_layout.addWidget(btn_del)
            btn_layout.addStretch()
            layout.addLayout(btn_layout)

    def set_object(self, object_id):
        """Установить ID объекта и загрузить файлы."""
        self.object_id = object_id
        if object_id:
            self.load_files()
        else:
            self.current_files = []
            self._refresh_table()

    def open_file(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите файл")
            return
        file_id = self.current_files[row].get('id')
        original_name = self.current_files[row].get('original_name', 'file')
        
        # Скачиваем файл во временную папку и открываем
        resp = self.api.get(f"files/{file_id}/download/")
        if resp.status_code == 200:
            # Сохраняем во временный файл
            suffix = os.path.splitext(original_name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(resp.content)
                tmp_path = tmp.name
            # Открываем в системном приложении
            if sys.platform == 'win32':
                os.startfile(tmp_path)
            elif sys.platform == 'darwin':
                subprocess.run(['open', tmp_path])
            else:
                subprocess.run(['xdg-open', tmp_path])
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось скачать файл")

    # def load_files(self):
    #     resp = self.api.get("files/")
    #     if resp.status_code == 200:
    #         data = resp.json() if isinstance(resp.json(), list) else resp.json().get('results', [])
    #         self.current_files = [
    #             f for f in data
    #             if f.get('content_type') == self.content_type
    #             and f.get('object_id') == self.object_id
    #         ]
    #         self._refresh_table()
    def load_files(self):
        if not self.object_id:
            return
        resp = self.api.get(f"files/?content_type={self.content_type}&object_id={self.object_id}")
        if resp.status_code == 200:
            data = resp.json() if isinstance(resp.json(), list) else resp.json().get('results', [])
            self.current_files = data
            self._refresh_table()

    def _refresh_table(self):
        self.table.setRowCount(len(self.current_files))
        for i, f in enumerate(self.current_files):
            self.table.setItem(i, 0, QTableWidgetItem(f.get('original_name', '')))
            self.table.setItem(i, 1, QTableWidgetItem(f.get('file_category', '')))
            size = f.get('file', {}).get('size', '') if isinstance(f.get('file'), dict) else ''
            self.table.setItem(i, 2, QTableWidgetItem(str(size)))

    def add_file(self):
        if not self.object_id:
            QMessageBox.warning(self, "Ошибка", "Сначала сохраните объект")
            return
        path, _ = QFileDialog.getOpenFileName(self, "Выбрать файл")
        if not path:
            return
        resp = self.api.upload('files/', {
            'content_type': self.content_type,
            'object_id': self.object_id,
            'file_category': 'other',
            'original_name': path.split('/')[-1],
        }, file_path=path)
        if resp.status_code == 201:
            self.load_files()
        else:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить: {resp.status_code}")

    def delete_file(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите файл")
            return
        file_id = self.current_files[row].get('id')
        resp = self.api.delete(f"files/{file_id}/")
        if resp.status_code == 204:
            self.load_files()
        else:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить: {resp.status_code}")