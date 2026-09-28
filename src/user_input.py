import sys

MODELS: tuple[str, ...] = ("base", "medium", "large-v3-turbo")
_DEFAULT_MODEL = "large-v3-turbo"
_CONFIRM_LETTERS = ('Y', 'y', 'Д', 'д', '')
_DENY_LETTERS = ('N', 'n', 'Н', 'н')


def _choice_parser(raw: str, options: tuple[str, ...]) -> str:
    """Checks if the user's input number is correct. Returns a model name or an error message. 
    
    1. raw: a user's input
    2. options: a tuple of models (is MODELS by default)
    """
    raw = raw.strip()  # cleaning string from garbage
    if not raw:
        raise ValueError("Ввод пустой")
    if not raw.isdigit():
        raise ValueError(f"{raw} - не является номером")
    index = int(raw) - 1
    if not 0 <= index <= len(options) - 1:
        raise ValueError(
            f"Номер должен быть в диапазоне от 0 до {len(options) - 1} вкл")

    return options[index]


def ask_model(options: tuple[str, ...] = MODELS) -> str:
    """Asks for user's model choice. Returns a chosen model name 

    1. options: a tuple of models (is MODELS by default)
    """
    print("Какую модель Вы хотите использовать?")
    for num, name in enumerate(options, start=1):
        mark = " (рекомендуется)" if name == _DEFAULT_MODEL else ""
        print(f"{num}. {name}{mark}")

    while True:
        try:
            choice = input("Введите номер модели: ")
            return _choice_parser(choice, options)
        except ValueError as err:
            print(f"{err}. Попробуйте ещё раз")
        except EOFError:
            print(f"\nstdin заблокирован, используем {_DEFAULT_MODEL}")
            return _DEFAULT_MODEL
        except KeyboardInterrupt:
            print("\nОстановка программы")
            sys.exit(130)


#TODO Добавить проверку на верное название, используя регулярки
def ask_file_name() -> str:
    """Asks for user's lecture's file name


    """
    print("Напишите название видео (расширение не писать): ")
    while True:
        _file_name = input()
        print(f"Название файла: {_file_name}")
        confirm = input("Вы уверены, что название верное? (это важно) (Y/n): ")
        confirm = confirm.strip()
        if (confirm in _CONFIRM_LETTERS):
            return _file_name
        elif (confirm in _DENY_LETTERS):
            print("Хорошо, повторите ввод...")
            continue
        else:
            print("Введите только y или n")
            #sys.exit(1)  #! Код ошибки другой!!!


if __name__ == "__main__":
    _model_name = ask_model()
    print("Model name: ", _model_name)
