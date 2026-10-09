# cybLaunch

> CLI для явного запуска проверок и статических приложений.

[![CI](https://github.com/c1cad4/cybLaunch/actions/workflows/ci.yml/badge.svg)](https://github.com/c1cad4/cybLaunch/actions/workflows/ci.yml)

[Карта экосистемы](https://github.com/c1cad4/cybOS) · [Архитектура](docs/ECOSYSTEM.md) · [Интеграция в cybOS](https://github.com/c1cad4/CybOS-demo)

## Назначение

CLI для явного запуска проверок и статических приложений. Этот репозиторий владеет своей областью; приложение и его UI остаются в `CybOS-demo`.

## Начать работу

Репозитории размещаются рядом в одной рабочей папке. Для полного окружения используйте `cybOS/tools/bootstrap.py` и `cybLaunch/launcher.py`; точные ревизии публикуются в lock-файлах интегратора.

```bash
cd cybLaunch
python3 -m unittest discover -s tests
python3 launcher.py list
python3 launcher.py test all
```

## Структура

- `launcher.py` — команды list/test/serve без shell-интерполяции.
- `tests/` — проверки реестра и аргументов.
- `docs/ECOSYSTEM.md` — границы компонента и связи.
