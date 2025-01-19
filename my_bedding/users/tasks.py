# import logging
from celery import shared_task
from django.conf import settings
# from django.core.mail import send_mail
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

User = get_user_model()

logger = get_task_logger(__name__)


@shared_task
def user_registered(user_id, raw_password):
    """
    Уведомление об успешном создании пользователя.
    """
    user = User.objects.get(id=user_id)
    password = raw_password

    logger.info(f"Отправка эл.письма об успешной регистрации покупателя {user.first_name} ({user.email})")

    subject = f'Добро пожаловать, {user.first_name}!'
    text_content = f""""""
    html_content = f"""
        <html>
            <body>
                <h3>Здравствуйте {user.first_name}!</h3>
                <p>Добро пожаловать на сайт <strong>MyBedding</strong>.<br>
                Для входа в свою учетную запись на сайте нажмите на иконку: <img
                src="https://img.icons8.com/?size=100&id=fJ7hcfUGpKG7&format=png&color=000000" alt=""
                style="width:20px;height:20px;"></p>
                <p><strong>Данные для входа:</strong><br>
                Email: {user.email}<br>
                Пароль: {password}</p>
                <p>Когда вы войдете в свою учетную запись, вам будут доступны:
                    <ul>
                        <li><Быстрое оформление заказов</li>
                        <li>Проверка статуса заказов</li>
                        <li>Просмотр истории заказов</li>
                        <li>Изменение информации учетной записи</li>
                        <li>Сохранение дополнительных адресов</li>
                    </ul>
                </p>
                <p>Если у Вас возникли вопросы по поводу Вашей учетной<br>
                записи или любой другой вопрос, пожалуйста, свяжитесь<br>
                с нами по адресу info@mybedding.ru или по телефону<br>
                8(800)800-00-00</p>
                <p>Если Вы не хотите получать информацию<br>
                о новых скидках и акциях с сайта mybedding.ru<br>
                отпишитесь по ссылке.</p>
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
        recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()



