from celery import shared_task
from django.core.mail import send_mail
from celery.utils.log import get_task_logger

from .models import Order, OrderItem

logger = get_task_logger(__name__)


@shared_task
def order_created(order_id):
    """
    Задание по отправке уведомления по электронной почте
    при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    logger.info(f'Отправка уведомления об оформлении заказа № {order.id}')

    # Формирование списка товаров
    items_list = "\n".join(
        f"- {item.article.product.title} (арт.№ {item.article.article}), размер - {item.article.size}, "
        f"количество - {item.quantity} шт." for item in order_items
    )

    # Используем get_FOO_display() для вывода статуса на русском
    payment_status = 'Оплачен' if order.payment else 'Не оплачен'
    transport_company = order.get_transport_company_display()

    subject = f'Заказ № {order.id} оформлен'
    message = f"""\
Уважаемый(-ая) {order.first_name}!

Вы успешно оформили заказ в интернет-магазине товаров для дома MyBedding
Номер заказа: {order.id} от {order.create_date.strftime('%d.%m.%Y')}

Товары в заказе:
{items_list}

Стоимость товаров: {order.total_cost} руб.
Скидка ({order.discount_percentage} %): {order.discount} руб.
Доставка: {order.delivery_cost} руб.
--------------------------
Итоговая стоимость: {order.total_cost_after_discount} руб.

Статус оплаты - {payment_status}.

Заказ будет передан в {transport_company}, пункт выдачи заказов - 
{order.pickup_point_address}. Просим Вас отслеживать доставку на сайте 
или приложении транспортной компании.

С уважением,
Магазин MyBedding,
адрес сайта - http://127.0.0.1:9000

Если Вы не оформляли заказ, просто проигнорируйте данное сообщение.
"""
    mail_sent = send_mail(
        subject,
        message,
        'smaspb17@yandex.ru',
        [order.email]
    )
    return mail_sent
