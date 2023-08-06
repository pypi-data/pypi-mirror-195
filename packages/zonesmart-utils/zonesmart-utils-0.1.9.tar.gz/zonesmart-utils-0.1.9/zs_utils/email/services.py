import requests
import json

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext as _
from django.utils import timezone

from zs_utils.exceptions import CustomException
from zs_utils.api.services import ApiRequestLogService
from zs_utils.user.models import AbstractZonesmartUser
from zs_utils.user.utils import encode_uid, ignore_last_login_token_generator
from zs_utils.email import html_templates


class EmailServiceException(CustomException):
    pass


class EmailService:
    """
    Статика: https://cloud.digitalocean.com/spaces/zonesmart-production?i=e47403&path=zonesmart_production%2Femail_static%2F
    Сервис для работы с email-уведомлениями (EmailSubscription)
    """

    @staticmethod
    def format_date(date: timezone.datetime) -> str:
        """
        Конвертация timezone.datetime в строку формата: '%a, %d %b %Y %H:%M:%S 0000'
        """
        return date.strftime("%a, %d %b %Y %H:%M:%S 0000")

    @classmethod
    def send_email(
        cls,
        sender: str,
        receivers: list,
        subject: str,
        text: str = None,
        files: dict = None,
        html: str = None,
        template: str = None,
        template_params: dict = None,
        delivery_time: timezone.datetime = None,
        tags: list = None,
        cancel_if_not_production: bool = True,
        **kwargs,
    ) -> dict:
        """
        Отправка email-уведомления на пользовательские email адреса
        """
        if cancel_if_not_production and (not settings.IS_PRODUCTION):
            for email in receivers:
                if email not in settings.TEST_EMAILS:
                    return {"email_canceled": True}

        data = {
            "from": sender,
            "to": receivers,
            "subject": subject,
            "text": text,
            "html": html,
            "template": template,
            "o:tag": tags,
        }
        if delivery_time:
            data["o:deliverytime"] = cls.format_date(delivery_time)
        if template_params:
            data["h:X-Mailgun-Variables"] = json.dumps(template_params)
        data = {key: value for key, value in data.items() if value}

        response = requests.post(
            url=f"{settings.MAILGUN_API_URL}/messages",
            auth=("api", settings.MAILGUN_API_KEY),
            data=data,
            files=files,
        )
        ApiRequestLogService.save_api_request_log_by_response(
            response=response,
            save_if_is_success=False,
        )
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_social_media_icon_urls(cls) -> dict:
        """
        Получение данных об иконках соц. сетей для формирования шаблона email-уведомления
        """
        file_names = {
            "facebook_icon_url": "facebook-icon.png",
            "instagram_icon_url": "instagram-icon.png",
            "linkedin_icon_url": "linkedin-icon.png",
            "youtube_icon_url": "youtube-icon.png",
            "twitter_icon_url": "twitter-icon.png",
        }
        return {key: f"{settings.EMAIL_STATIC_FOLDER_URL}{value}" for key, value in file_names.items()}

    @classmethod
    def send_email_using_standard_template(
        cls,
        sender: str,
        receivers: list,
        subject: str,
        title: str,
        body_content: str,
        cheers_content: str,
        email_icon_path: str = None,
        email_icon_url: str = None,
        files: dict = None,
        footer_extra_content: str = None,
        extra_template_params: dict = None,
        **kwargs,
    ) -> dict:
        """
        Отправка email-уведомлений с использованием стандартного шаблона
        """
        if title:
            title_html = html_templates.title.format(title=title)
        else:
            title_html = ""

        if not email_icon_url:
            if email_icon_path:
                email_icon_url = f"{settings.EMAIL_STATIC_FOLDER_URL}{email_icon_path}"
            else:
                email_icon_url = f"{settings.EMAIL_STATIC_FOLDER_URL}icon_email.png"

        template_params = {
            "title": title_html,
            "body": body_content,
            "logo_url": f"{settings.EMAIL_STATIC_FOLDER_URL}logo-1.png",
            "email_icon_url": email_icon_url,
            "cheers_text": cheers_content,
        }

        if footer_extra_content:
            template_params["footer_text"] = footer_extra_content

        template_params.update(cls.get_social_media_icon_urls())

        if extra_template_params:
            template_params.update(extra_template_params)

        return cls.send_email(
            sender=sender,
            receivers=receivers,
            subject=subject,
            template="blank_template",
            template_params=template_params,
            files=files,
            **kwargs,
        )

    @classmethod
    def send_standard_team_email(
        cls,
        receivers: list,
        subject: str,
        title: str,
        body_content: str,
        email_icon_path: str = None,
        files: dict = None,
        footer_extra_content: str = None,
        extra_template_params: dict = None,
        **kwargs,
    ):
        """
        Отправка email-уведомлений с использованием командного шаблона (от лица команды Zonesmart)
        """
        return cls.send_email_using_standard_template(
            sender="Команда Zonesmart info@zonesmart.ru",
            receivers=receivers,
            subject=subject,
            title=title,
            body_content=body_content,
            email_icon_path=email_icon_path,
            cheers_content=html_templates.team_cheers,
            files=files,
            footer_extra_content=footer_extra_content,
            extra_template_params=extra_template_params,
            **kwargs,
        )

    @classmethod
    def send_password_reset_email(cls, user: AbstractZonesmartUser, **kwargs) -> dict:
        """
        Отправка email-уведомления о смене пароля
        """
        body_content = html_templates.password_reset.format(
            reset_password_url=settings.PASSWORD_RESET_CONFIRM_URL.format(
                uid=encode_uid(user.id),
                token=default_token_generator.make_token(user),
            )
        )

        return cls.send_standard_team_email(
            receivers=[user.email],
            subject="Сброс пароля",
            title="Забыли Ваш пароль?",
            body_content=body_content,
            email_icon_path="icon_password.png",
            footer_extra_content=html_templates.password_reset_footer,
            **kwargs,
        )

    @classmethod
    def send_successful_changed_password_email(cls, user: AbstractZonesmartUser, **kwargs):
        """
        Отправка email-уведомления об успешной смене пароля
        """
        body_content = html_templates.password_reset_confirm.format(
            dashboard_url=settings.ZONESMART_DOMAIN_WITH_PROTOCOL,
        )

        return cls.send_standard_team_email(
            receivers=[user.email],
            subject="Ваш пароль был изменен",
            title="Ваш пароль был изменен",
            body_content=body_content,
            email_icon_path="key-icon.png",
            **kwargs,
        )

    @classmethod
    def send_verification_email(cls, user: AbstractZonesmartUser, **kwargs) -> dict:
        """
        Отправка email-уведомления об подтверждении почты
        """
        body_content = html_templates.verification.format(
            first_name=user.first_name,
            accept_email_url=settings.VERIFY_EMAIL_URL.format(
                uid=encode_uid(user.id),
                token=ignore_last_login_token_generator.make_token(user),
            ),
        )

        return cls.send_standard_team_email(
            receivers=[user.email],
            subject="Подтверждение email",
            title="Подтверждение email",
            body_content=body_content,
            email_icon_path="icon_email.png",
            **kwargs,
        )

    @classmethod
    def send_remind_verification_email(
        cls, user: AbstractZonesmartUser, update_email_settings: bool = True, **kwargs
    ) -> dict:
        """
        Отправка email-напоминания о необходимости подтвердить почту
        """
        body_content = html_templates.remind_verification.format(
            first_name=user.first_name,
            email=user.email,
            accept_email_url=settings.VERIFY_EMAIL_URL.format(
                uid=encode_uid(user.id),
                token=ignore_last_login_token_generator.make_token(user),
            ),
        )

        if update_email_settings:
            user.email_settings.remind_verification_sent = True
            user.email_settings.save(update_fields=["remind_verification_sent"])

        return cls.send_standard_team_email(
            receivers=[user.email],
            subject="Напоминание о подтверждении email",
            title="Напоминание о подтверждении email",
            body_content=body_content,
            email_icon_path="icon_email.png",
            **kwargs,
        )

    @classmethod
    def send_successful_registration_email(cls, user: AbstractZonesmartUser, **kwargs) -> dict:
        """
        Отправка email-уведомления об успешной регистрации
        """
        manager = user.manager
        if not manager:
            raise EmailServiceException(_("У пользователя нет менеджера."))

        body_content = html_templates.successful_registration.format(
            user_first_name=user.first_name,
            manager_first_name=manager.first_name,
        )

        user.email_settings.welcome_email_sent = True
        user.email_settings.save(update_fields=["welcome_email_sent"])

        return cls.send_standard_manager_email(
            manager=manager,
            receivers=[user.email],
            subject="Спасибо за регистрацию в ZoneSmart",
            title="Спасибо за регистрацию в ZoneSmart",
            body_content=body_content,
            email_icon_path="icon_pricing.png",
            **kwargs,
        )

    @classmethod
    def send_email_reset_email(cls, user: AbstractZonesmartUser, **kwargs) -> dict:
        """
        Отправка email-уведомления об изменении почты
        """
        body_content = html_templates.email_reset.format(
            first_name=user.first_name,
            reset_email_url=settings.RESET_EMAIL_URL.format(
                uid=encode_uid(user.id),
                token=default_token_generator.make_token(user),
            ),
        )

        return cls.send_standard_team_email(
            receivers=[user.email],
            subject="Изменение email",
            title="Изменение email",
            body_content=body_content,
            email_icon_path="icon_email.png",
            **kwargs,
        )
