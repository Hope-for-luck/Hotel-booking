from django.core.mail import send_mail


def send_activations_code(email, activation_code):
    message = f'Поздравляем с регистрацией на сайте. Ваш код для активации аккаунта: {activation_code}'
    send_mail(
         'Активация аккаунта',
         message,
         '123@gmail.com',
         [email]
    )
