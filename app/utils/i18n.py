import os
import pathlib
from typing import Any, Union, cast

from fluent.runtime import FluentLocalization, FluentResourceLoader

from app.config import settings


class I18N:
    def __init__(self) -> None:
        self._loader = None
        self._l10n: dict[str, FluentLocalization] = {}
        self._current_locale = settings.app.default_locale

    def _get_loader(self) -> FluentResourceLoader:
        if self._loader is None:
            self._loader = FluentResourceLoader(
                os.path.join(
                    pathlib.Path(__file__).resolve().parent.parent.parent,
                    "locales",
                    "{locale}",
                ),
            )
        return self._loader

    def set_locale(self, locale: str) -> None:
        if locale not in settings.app.supported_locales:
            raise ValueError(f"Unsupported locale: {locale}")
        self._current_locale = locale

    def __call__(
        self,
        message_id: str,
        args: Union[dict[str, Any], None] = None,
        **kwargs: Any,
    ) -> str:
        if args is not None:
            kwargs.update(args)

        default_locale = settings.app.default_locale
        supported_locales = settings.app.supported_locales

        current_locale = self._current_locale
        if current_locale not in supported_locales:
            current_locale = default_locale

        for locale in {current_locale, default_locale}:
            if locale not in self._l10n:
                self._l10n[locale] = FluentLocalization(
                    [locale, default_locale],
                    ["main.ftl"],
                    self._get_loader(),
                )

        try:
            return cast(
                str,
                self._l10n[current_locale].format_value(message_id, kwargs),
            )
        except Exception:
            return cast(
                str,
                self._l10n[default_locale].format_value(message_id, kwargs),
            )


_ = I18N()
