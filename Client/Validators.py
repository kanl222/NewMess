from string import ascii_letters, printable, digits
from re import match
invalid_combinations = [
    "qwe",
    "ert",
    "wer",
    "rty",
    "tyu",
    "yui",
    "uio",
    "iop",
    "asd",
    "sdf",
    "dfg",
    "fgh",
    "ghj",
    "hjk",
    "jkl",
    "zxc",
    "xcv",
    "cvb",
    "vbn",
    "bnm",
    "йцу",
    "цук",
    "уке",
    "кен",
    "енг",
    "нгш",
    "гшщ",
    "шщз",
    "щзх",
    "зхъ",
    "фыв",
    "ыва",
    "вап",
    "апр",
    "про",
    "рол",
    "олд",
    "лдж",
    "джэ",
    "ячс",
    "чсм",
    "сми",
    "мит",
    "ить",
    "тьб",
    "ьбю",
    "жэё",
]


class ValidationError(Exception):
    def __init__(self, message:str):
        super().__init__(message)

class NameValidator(object):
    def __init__(self, min_len=2, max_len=25):
        self.min_len = min_len
        self.max_len = max_len

    def __call__(self, Text: str):
        if self.min_len > len(Text) >= self.max_len:
            raise ValidationError(
                message=f"Имя должен иметь длинну от {self.min_len} до {self.max_len}")


class PasswordValidator(object):
    def __init__(self, min_len=8, max_len=25):
        self.min_len = min_len
        self.max_len = max_len
        self.valid_symb = printable

    def __call__(self, Text: str):
        if self.min_len > len(Text) >= self.max_len:
            raise ValidationError(
                message=f"Пароль должен иметь длинну от {self.min_len} до {self.max_len}"
            )
        if Text.lower() == Text or Text.upper() == Text:
            raise ValidationError(
                message="Пароль должен содержать строчные и заглавные буквы"
            )
        if not any([c in Text for c in list(digits)]):
            raise ValidationError(message="Пароль должен содержать цифры")
        if any([i in Text.lower() for i in invalid_combinations]):
            raise ValidationError(
                message="Пароль не долен содержать комбинации из подряд идущих символов"
            )
        for i in Text.strip():
            if i not in self.valid_symb:
                print(i)
                raise ValidationError(message="Пароль содержит недопустимые символы")


class EmailValidator(object):
    def __call__(self, Text: str):
        if not match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", Text):
            raise ValidationError(message="Некорректный адрес электронной почты: exemple@exemple.com")

