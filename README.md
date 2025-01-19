# my_bedding


Терминал stripe для webhooks (получения информации о платежах)
- скачай файл stripe.exe - https://github.com/stripe/stripe-cli/releases/tag/v1.23.3
- в терминале пройди в директорию payment и выполни команду
```shell
.\stripe login
```
- пройди на страницу stripe и введи код из почты
- выполни команду для подключения прослушивания платежей
```shell
.\stripe listen --forward-to localhost:8000/payment/webhook/
```
