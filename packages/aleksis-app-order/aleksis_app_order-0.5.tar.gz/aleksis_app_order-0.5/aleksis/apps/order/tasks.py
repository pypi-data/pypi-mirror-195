from datetime import timedelta

from django.utils import timezone

from aleksis.core.celery import app

from .models import DigitalProductShare


@app.task(run_every=timedelta(days=1))
def cleanup_expired_shares():
    """Delete expired digital product shares."""
    expired_shares = DigitalProductShare.objects.filter(share_expiration__lt=timezone.now().date())
    expired_shares.delete()
