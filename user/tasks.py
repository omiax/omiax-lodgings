from django.core import management


def flush_expired_tokens():
    management.call_command('flushexpiredtokens')
