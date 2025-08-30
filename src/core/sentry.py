import sentry_sdk

from core.settings import get_settings


def init_sentry() -> None:
    settings = get_settings()

    if not settings.sentry_dsn:
        return

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.env,
        traces_sample_rate=0.1,
        send_default_pii=True,
        debug=settings.debug,
    )
