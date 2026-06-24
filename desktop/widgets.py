from PyQt5.QtWidgets import QTableWidgetItem


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


def populate_table(table, data, column_names=None):
    """Заполняет QTableWidget данными из списка словарей."""
    table.setSortingEnabled(False)
    table.clear()
    table.setRowCount(0)
    table.setColumnCount(0)

    if not data:
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels(["Нет данных"])
        table.setSortingEnabled(True)
        return

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