import pytest
from function import mask_card_number, mask_account_number, print_last_operations

def test_mask_card_number_correct():
    card_number = '1234567812345678'
    masked = mask_card_number(card_number)
    assert masked == '1234 56** **** 5678', "Card number is not masked correctly."

def test_mask_card_number_incorrect_length():
    card_number = '12345678'
    masked = mask_card_number(card_number)
    assert masked == "Не корректный номер карты", "Should not mask an incorrectly length card number."

def test_mask_card_number_non_digit():
    card_number = '1234abcd1234efgh'
    masked = mask_card_number(card_number)
    assert masked == "Не корректный номер карты", "Should not mask a non-digit card number."

def test_mask_account_number_correct():
    account_number = '12345678'
    masked = mask_account_number(account_number)
    assert masked == '**5678', "Account number is not masked correctly."

def test_mask_account_number_too_short():
    account_number = '123'
    masked = mask_account_number(account_number)
    assert masked == "Не корректный номер счета", "Should not mask an incorrectly short account number."

def test_mask_account_number_non_digit():
    account_number = 'abcd5678'
    masked = mask_account_number(account_number)
    assert masked == "Не корректный номер счета", "Should not mask a non-digit account number."


def test_print_last_operations(capsys):
    # Создаем mock данных операций
    operations = [
        {
            "date": "2021-09-01T12:00:00.000",
            "description": "Тестовая операция",
            "from": "Счет 1234567890112233",
            "to": "Карта 1234567812345678",
            "operationAmount": {"amount": 1000, "currency": {"name": "RUB"}},
            "state": "EXECUTED"
        },
        # Добавьте столько операций, сколько требуется для тестирования
    ]

    # Предполагается, что `print_last_operations` является функцией, которую вы тестируете
    print_last_operations(operations)

    # Захватим вывод
    captured = capsys.readouterr()

    # Убедимся, что вывод соответствует ожидаемому
    assert "01.09.2021 Тестовая операция" in captured.out
    assert "Счет **2233 -> Карта 1234 56** **** 5678" in captured.out
    assert "1000 RUB" in captured.out