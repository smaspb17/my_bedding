from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404

from orders.models import Order

User = get_user_model()

logger = get_task_logger(__name__)


@shared_task
def payment_completed(order_id):
    """
    Уведомление об успешном создании пользователя.
    """
    logger.info(f'Отправка эл.письма об успешной оплате заказа № {order_id}')

    order = get_object_or_404(Order, id=order_id)
    user = order.user

    subject = f'Оплата заказа № {order_id}'
    text_content = f""""""
    html_content = f"""
        <html>
            <body>
                <h3>Здравствуйте, {user.first_name}!</h3>
                <p>Вы успешно оплатили заказ № {order_id} от {order.create_date.strftime('%d.%m.%Y')}.<br>
                Сумма оплаты: {order.total_cost_after_discount} руб.</p>
                Квитанция об оплате (чек): <ссылка></p>
                                
                <p>Чтобы пройти на страницу заказ нажмите на <ссылка></p>
                
                <p>Если у Вас возникли вопросы по поводу Вашего заказа<br>
                или любой другой вопрос, пожалуйста, свяжитесь<br>
                с нами по адресу info@mybedding.ru или по телефону<br>
                8(800)800-00-00</p>
                <p>Если Вы не хотите получать информацию<br>
                о новых скидках и акциях с сайта mybedding.ru<br>
                отпишитесь по <ссылка>.</p>
                <p>С уважением,<br>Магазин MyBedding.<br>
                Адрес сайта - https://mybedding.ru</p>
            </body>
        </html>
        """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    email = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        recipient_list
    )
    email.attach_alternative(html_content, "text/html")
    email.send()