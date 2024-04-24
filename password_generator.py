import random
import string
import pyperclip
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, \
    QSpinBox, QPushButton, QCheckBox, QLineEdit
from zxcvbn import zxcvbn


class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('Генератор паролей')
        self.layout = QVBoxLayout()
        self.setup_password_options()

        # Кнопка генерации
        self.generate_button = QPushButton('Сгенерировать пароль')
        self.generate_button.clicked.connect(self.generate_password)

        # Поле вывода пароля
        self.password_lineedit = QLineEdit()
        self.password_lineedit.setReadOnly(True)

        # Кнопка копирования
        self.copy_button = QPushButton('Копировать в буфер обмена')
        self.copy_button.clicked.connect(self.copy_password)

        # Кнопка копирования
        self.strength_label = QLabel('Сложность пароля: Неизвестно')
        self.strength_label.setWordWrap(True)

        # Сложность пароля
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.password_lineedit)
        self.layout.addWidget(self.copy_button)
        self.layout.addWidget(self.strength_label)

        self.setLayout(self.layout)

    def setup_password_options(self):
        # Длина пароля
        self.length_label = QLabel('Длина пароля:')
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setMinimum(4)
        self.length_spinbox.setMaximum(128)
        self.length_spinbox.setValue(12)

        length_layout = QHBoxLayout()
        length_layout.addWidget(self.length_label)
        length_layout.addWidget(self.length_spinbox)

        # Опции для пароля
        self.uppercase_checkbox = QCheckBox('Прописные буквы')
        self.uppercase_checkbox.setChecked(True)
        self.lowercase_checkbox = QCheckBox('Строчные буквы')
        self.lowercase_checkbox.setChecked(True)
        self.digits_checkbox = QCheckBox('Цифры')
        self.digits_checkbox.setChecked(True)
        self.symbols_checkbox = QCheckBox('Символы')
        self.symbols_checkbox.setChecked(True)

        # Добавление элементов в слой опций
        self.layout.addLayout(length_layout)
        self.layout.addWidget(self.uppercase_checkbox)
        self.layout.addWidget(self.lowercase_checkbox)
        self.layout.addWidget(self.digits_checkbox)
        self.layout.addWidget(self.symbols_checkbox)

    def get_character_set(self):
        characters = []
        if self.uppercase_checkbox.isChecked():
            characters += string.ascii_uppercase
        if self.lowercase_checkbox.isChecked():
            characters += string.ascii_lowercase
        if self.digits_checkbox.isChecked():
            characters += string.digits
        if self.symbols_checkbox.isChecked():
            characters += string.punctuation
        return ''.join(characters)

    def generate_password(self):
        length = self.length_spinbox.value()
        characters = self.get_character_set()

        if not characters:
            self.password_lineedit.clear()
            self.password_lineedit.setPlaceholderText(
                "Выберите хотя бы один набор символов!")
            self.password_lineedit.setStyleSheet("color: red;")
        else:
            password = ''.join(
                random.choice(characters) for _ in range(length))
            self.password_lineedit.setText(password)
            self.password_lineedit.setStyleSheet("color: black;")
            self.evaluate_password_strength(password)

    def copy_password(self):
        password = self.password_lineedit.text()
        pyperclip.copy(password)

    def evaluate_password_strength(self, password):
        results = zxcvbn(password)
        score = results['score']
        strength_text = {
            0: 'Очень слабый',
            1: 'Слабый',
            2: 'Средний',
            3: 'Сильный',
            4: 'Очень сильный'
        }
        self.strength_label.setText(
            f'Сложность пароля: {strength_text[score]}')
