from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.conf import settings
from core.models import AppLogs


app_log = Signal(providing_args=['code', 'severity', 'description', 'data'])


@receiver(user_logged_in)
def sig_user_logged_in(sender, user, request, **kwargs):
    ip = request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR', None))
    AppLogs.objects.create(severity=3, code='LOGIN', data={'user': user.id, 'ip': ip})


@receiver(user_logged_out)
def sig_user_logged_out(sender, user, request, **kwargs):
    ip = request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR', None))
    AppLogs.objects.create(severity=3, code='LOGOUT', data={'user': user.id, 'ip': ip})


@receiver(user_login_failed)
def sig_user_login_failed(sender, credentials, request, **kwargs):
    ip = request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR', None))
    data = {'credentials': credentials, 'ip': ip}
    AppLogs.objects.create(severity=3, code='LOGIN', data=data)


@receiver(app_log)
def sig_app_log(sender, code, severity=1, description=None, data=None, **kwargs):
    AppLogs.objects.create(severity=severity,
                           code=code,
                           description=description,
                           data=data)


@receiver(post_save, sender=User, dispatch_uid="assign_user_first_group")
def assign_user_first_group(sender, instance, created, **kwargs):
    # ISSUE usuario nuevo es por defecto ciudadano
    # https://github.com/cluster311/ggg/issues/180
    if created:
        group, created = Group.objects.get_or_create(name=settings.GRUPO_CIUDADANO)
        user = instance
        group.user_set.add(user)
