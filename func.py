from datetime import datetime
import json

def print_last_operations(operations):
    # Отфильтровать выполненные операции
    executed_operations = [op for op in operations if 'state' in op and op['state'] == 'EXECUTED']
    # Сортировать операции по дате в убывающем порядке
    sorted_operations = sorted(
        operations,
        key=lambda x: datetime.strptime(x.get('date', '1900-01-01T00:00:00.000'), '%Y-%m-%dT%H:%M:%S.%f'),
        reverse=True  # Для сортировки в убывающем порядке по дате
    )
    last_operations = sorted_operations[-6:]

    for operation in last_operations:
        # Перевод даты из строки в объект datetime
        date_obj = datetime.strptime(operation.get('date', '1900-01-01T00:00:00.000'), '%Y-%m-%dT%H:%M:%S.%f')
        # Преобразование объекта datetime обратно в строку, в нужном формате
        formatted_date = date_obj.strftime('%d.%m.%Y')
        # Вывести дату перевода и описание перевода в нужном формате
        print(f"{formatted_date} {operation.get('description')}")

        # Вывести номер карты в замаскированном формате
        card_number = operation.get('from')
        card_number_2 = operation.get('to')
        masked_card_number_2 = "**** **** **** {}".format(card_number_2[-4:])
        if card_number is None:
            print(f"{operation.get('to')}")
        else:
            masked_card_number = "{} **** **** {}".format(
                card_number[:6], card_number[-4:]
            )
            print(f"{masked_card_number} -> {masked_card_number_2}")
        # Вывести сумму перевода и валюту
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