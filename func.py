from datetime import datetime
import json


def mask_from_to_msg(msg) -> str:
    """
    Скрывает номер счета/карты для полей <откуда>, <куда>.
    :param msg: строка с типом перевода и номером счета/карты
    :return: строка со скрытым номером счета/карты
    """
    # если в json не было from или to ключа
    if msg is None:
        return ''

    # все слова через пробел, последним идет номер
    msg_split = msg.split(sep=' ')
    if msg_split[0] == 'Счет':
        number_hidden = mask_account_number(msg_split[-1])
    else:
        number_hidden = mask_card_number(msg_split[-1])
    return ' '.join(msg_split[:-1]) + ' ' + number_hidden


def mask_card_number(number: str) -> str:
    """
    Возвращает маску для номера карты.
    Правило: видны первые 6 цифр и последние 4, разбито по блокам по 4 цифры, разделенных пробелом.
    :param number: Строка с номером карты.
    :return: Строка с маской карты, в формате XXXX XX** **** XXXX
    """
    if number.isdigit() and len(number) == 16:
        return number[:4] + ' ' + number[4:6] + '** **** ' + number[-4:]
    else:
        return "Не корректный номер карты"


def mask_account_number(number: str) -> str:
    """
    Возвращает маску для номера счета.
    Правило: видны только последние 4 цифры номера счета.
    :param number: Строка с номером счета.
    :return: Строка с маской счета, в формате **XXXX
    """
    if number.isdigit() and len(number) >= 4:
        return '**' + number[-4:]
    else:
        return "Не корректный номер счета"


def print_last_operations(operations):
    # Отфильтровать выполненные операции
    executed_operations = [op for op in operations if 'state' in op and op['state'] == 'EXECUTED']
    # Сортировать операции по дате в убывающем порядке
    sorted_operations = sorted(
        executed_operations,
        key=lambda x: x['date'],
        reverse=True  # Для сортировки в убывающем порядке по дате
    )
    last_operations = sorted_operations[:5]

    for operation in last_operations:
        # Перевод даты из строки в объект datetime
        date_obj = datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f')
        formatted_date = date_obj.strftime('%d.%m.%Y')

        print(f"{formatted_date} {operation.get('description')}")
        message_from = mask_from_to_msg(operation.get('from'))
        message_to = mask_from_to_msg(operation.get('to'))
        print(f"{message_from} -> {message_to}")

        operation_amount_info = operation.get('operationAmount')
        amount = operation_amount_info.get('amount')
        currency = operation_amount_info.get('currency')
        name = currency.get('name')
        print(f"{amount} {name}")
        # Разделить операции пустой строкой
        print()


def main():
    # Получить список операций клиента
    with open('operations.json') as file:
        operations = json.load(file)
        # Вывести последние 5 операций
        print_last_operations(operations)


if __name__ == '__main__':
    main()