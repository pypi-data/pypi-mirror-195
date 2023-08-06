title = """
    <tr>
        <td align="center" style="padding: 10px 0 30px 0">
            <h1 style="color: #37373C;font-family: 'Trebuchet', sans-serif;font-weight: bold;font-size: 24px;line-height: 140%; letter-spacing: 1.3px; margin-bottom: 0">
                {title}
            </h1>
        </td>
    </tr>
"""


team_cheers = """
    <tr>
        <td>
            Спасибо за чтение,
        </td>
    </tr>
    <tr>
        <td style="color: #3BD0BC;">
            Команда Zonesmart
        </td>
    </tr>
"""


password_reset = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                Похоже, вы хотите сбросить пароль для учетной записи <span style="color: #3BD0BC; font-weight: bold">Zonesmart</span>.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                Не волнуйтесь, вы можете создать новый, нажав кнопку ниже.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 30px">
                <a href="{reset_password_url}" class="button" style="color: #ffffff">
                    Сброс пароля
                </a>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px; letter-spacing: 0.5px; color: #736E6E; font-size: 12px">
                Если вы не просили нас сбросить пароль, то просто проигнорируйте
                это письмо. Ваша учетная запись в безопасности.
            </td>
        </tr>
        </tbody>
    </table>
"""


password_reset_footer = """
    Это письмо было отправленно, потому что вы попросили сбросить пароль на <a href="https://app.zonesmart.com" style="color: #3BD0BC; text-decoration: none">Zonesmart</a>
"""


password_reset_confirm = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 40px">
                Пароль для  вашей учетной записи <span style="color: #3BD0BC; font-weight: bold">Zonesmart</span> недавно был изменен. Теперь вы можете войти в систему, используя свой новый пароль.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{dashboard_url}" class="button" style="color: #ffffff">
                    Перейти в Zonesmart
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""

verification = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, добрый день.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                 Для подтверждения адреса электронной почты Вашего аккаунта <span style="color: #3BD0BC; font-weight: bold">ZoneSmart</span>, пожалуйста, нажмите на кнопку ниже.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0px 0 40px">
                <a href="{accept_email_url}" class="button" style="color: #ffffff">
                    Подтвердить email
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""

remind_verification = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, добрый день.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                Вы были зарегистрированы в системе <span style="color: #3BD0BC; font-weight: bold">Zonesmart OMS</span>. Пожалуйста, подтвердите ваш адрес электроной почты <a style="color: #3BD0BC; font-weight: bold">{email}</a>, чтобы продолжить пользоваться <span style="color: #3BD0BC; font-weight: bold">Zonesmart OMS</span>.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0px 0 40px">
                <a href="{accept_email_url}" class="button" style="color: #ffffff">
                    Подтвердить email
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""

successful_registration = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 520px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 15px">
                <span style="color: #3BD0BC; font-weight: bold">{user_first_name}</span>, приветствую Вас!
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 15px">
                Меня зовут <span style="color: #3BD0BC; font-weight: bold">{manager_first_name}</span>, и я менеджер пробного периода в компании <span style="color: #3BD0BC; font-weight: bold">ZoneSmart</span>, рад знакомству!
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 15px">
                Предполагаю, что регистрация в платформе для мульти-канальных продаж - уже не первое Ваше успешное решение за сегодняшний день.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 15px">
                Для того, чтобы в этом убедиться за время бесплатного пробного периода (который, кстати, длится целых 14 дней), я буду рад помогать Вам в процессе освоения нашего сервиса. Периодически я буду присылать рекомендации по работе на почту – они помогут сделать наше взаимодействие эффективнее.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                Перед тем, как Вы <a href="https://zonesmart.zendesk.com/hc/ru/categories/4407691046033" style="color: #3BD0BC; font-weight: bold">подключите первый аккаунт на маркетплейсе</a> к единому личному кабинету и начнете покорять новые каналы продаж, я бы посоветовал определить сценарий использования сервиса (их может быть <a href="https://zonesmart.zendesk.com/hc/ru/articles/4410033986577" style="color: #3BD0BC; font-weight: bold">несколько одновременно</a>):
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                1. <a href="https://zonesmart.zendesk.com/hc/ru/articles/4410033986577" style="color: #3BD0BC; font-weight: bold">Интеграция маркетплейса(-ов) с сайтом или системой товароучета.</a>
                <p style="margin: 0px">
                    Позволит массово адаптировать и разместить каталог товаров с сайта на одном или нескольких маркетплейсах. Товарные остатки синхронизируются автоматически, а заказы со всех каналов продаж – выгружаются в Вашу систему.
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                2. <a href="https://zonesmart.zendesk.com/hc/ru/articles/4410491540113" style="color: #3BD0BC; font-weight: bold">Интеграция аккаунтов на нескольких маркетплейсах между собой.</a>
                <p style="margin: 0px">
                    Подойдет для быстрой синхронизации каталога между маркетплейсами и автономного обновления информации об остатках.
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                3. <a href="https://zonesmart.zendesk.com/hc/ru/articles/4411155259537" style="color: #3BD0BC; font-weight: bold">Система управления заказами (OMS) для FBS / DBS / RFBS моделей.</a>
                <p style="margin: 0px">
                    Заказы со всех подключенных каналов продаж собираются в одном окне, а встроенные интеграции с популярными курьерскими службами не заставят тратить лишнее время на покупку почтового лейбла на стороннем ресурсе.
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                4. <a href="https://zonesmart.zendesk.com/hc/ru/articles/4411546464785" style="color: #3BD0BC; font-weight: bold">Система управления клиентской базой (CRM).</a>
                <p style="margin: 0px">
                    Платформа осуществляет сбор данных о покупателях со всех маркетплейсов в едином личном кабинете, упрощая анализ клиентской базы и статистики продаж.
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 15px">
                В процессе работы, пожалуйста, не забывайте обращаться к нам по любым возникающим вопросам, а также получать удовольствие.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 15px">
                Желаю успехов!
            </td>
        </tr>
        </tbody>
    </table>
"""

email_reset = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                Здравствуйте, <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>!
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                Для изменения адреса электронной почты вашего аккаунта <span style="color: #3BD0BC; font-weight: bold">Zonesmart</span>, пожалуйста, нажмите на кнопку ниже.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{reset_email_url}" class="button" style="color: #ffffff">
                    Изменить email
                </a>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                Мы желаем вам удачных продаж по всему миру.
            </td>
        </tr>
        </tbody>
    </table>
"""
