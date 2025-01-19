
# статусы заказа
ORDER_STATUS = [
    ('Created', 'Оформлен'),
    ('In progress', 'Выполняется'),
    ('In transit', 'Передан в доставку'),
    ('Completed', 'Завершен'),
]
# статус оплаты
PAYMENT_STATUS = [
    ('Not paid', 'Не оплачен'),
    # ('Partially paid', 'Оплачен частично'),
    ('Paid', 'Оплачен'),
]
TRANSPORT_COMPANY = [
    ('Russian post', 'Почта России'),
    ('CDEK', 'СДЭК'),
    ('Boxberry', 'Boxberry'),
    ('5post', '5post'),
]