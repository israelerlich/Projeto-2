"""App Flask simples usando Postgres e Redis via Docker Compose."""

# Nota: pyright reclama localmente porque essas libs só vivem no container
# pyright: reportMissingImports=false

import importlib
import os
from contextlib import contextmanager
from typing import Any, Generator, Optional

try:
    psycopg2 = importlib.import_module("psycopg2")
    _extras = importlib.import_module("psycopg2.extras")
    RealDictCursor = getattr(_extras, "RealDictCursor")
except ImportError as exc:  # pragma: no cover - somente apita fora do container
    raise RuntimeError(
        "psycopg2 precisa estar instalado (o container cuida disso, relaxa)"
    ) from exc

from flask import Flask, jsonify

try:
    import redis
except ImportError as exc:  # pragma: no cover - somente apita fora do container
    raise RuntimeError(
        "redis (cliente Python) precisa estar instalado dentro do container"
    ) from exc


def create_app() -> Flask:
    """Factory básica do Flask para manter a config centralizada."""
    app = Flask(__name__)

    app.config.update(
        APP_NAME=os.getenv("APP_NAME", "Student Service Hub"),
        POSTGRES_HOST=os.getenv("POSTGRES_HOST", "db"),
        POSTGRES_DB=os.getenv("POSTGRES_DB", "student_notes"),
        POSTGRES_USER=os.getenv("POSTGRES_USER", "student"),
        POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD", "studentpass"),
        REDIS_HOST=os.getenv("REDIS_HOST", "cache"),
        REDIS_PORT=int(os.getenv("REDIS_PORT", "6379")),
        CACHE_TTL=int(os.getenv("CACHE_TTL", "30")),
    )

    # Redis vira nosso cache rápido; decode_responses facilita para trabalhar com strings.
    cache_client = redis.Redis(
        host=app.config["REDIS_HOST"],
        port=app.config["REDIS_PORT"],
        decode_responses=True,
    )

    @contextmanager
    def db_cursor() -> Generator[Any, None, None]:
        """Abre conexão curta com Postgres para evitar conexões penduradas."""
        connection = psycopg2.connect(
            host=app.config["POSTGRES_HOST"],
            dbname=app.config["POSTGRES_DB"],
            user=app.config["POSTGRES_USER"],
            password=app.config["POSTGRES_PASSWORD"],
        )
        try:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                yield cursor
                connection.commit()
        finally:
            connection.close()

    def fetch_counter_from_db(label: str) -> Optional[int]:
        """Busca o contador direto no banco quando o cache não souber responder."""
        with db_cursor() as cursor:
            cursor.execute(
                "SELECT total FROM visit_counter WHERE label = %s", (label,)
            )
            row = cursor.fetchone()
        return row["total"] if row else None

    def persist_counter(label: str, total: int) -> None:
        """Garante que o contador fica salvo, atualizando o mesmo registro."""
        with db_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO visit_counter(label, total)
                VALUES (%s, %s)
                ON CONFLICT (label)
                DO UPDATE SET total = EXCLUDED.total
                """,
                (label, total),
            )

    @app.get("/health")
    def healthcheck():
        """Endpoint rápido para testar se banco e cache estão respondendo."""
        try:
            db_ok = fetch_counter_from_db("homepage") is not None
        except psycopg2.Error:
            db_ok = False

        try:
            cache_ok = cache_client.ping()
        except redis.exceptions.RedisError:
            cache_ok = False

        status = db_ok and cache_ok
        http_code = 200 if status else 503
        return jsonify(
            service=app.config["APP_NAME"],
            database=db_ok,
            cache=cache_ok,
        ), http_code

    @app.get("/")
    def homepage():
        """Mostra mensagem de boas-vindas e incremento do contador de visitas."""
        cache_key = "visit_counter:homepage"
        cached_total = cache_client.get(cache_key)

        if cached_total is None:
            total = fetch_counter_from_db("homepage") or 0
        else:
            total = int(cached_total)

        updated_total = total + 1
        persist_counter("homepage", updated_total)
        cache_client.setex(cache_key, app.config["CACHE_TTL"], updated_total)

        return jsonify(
            message="Bem-vindo ao hub de serviços da faculdade!",
            visits=updated_total,
            cached=cached_total is not None,
        )

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=8000, debug=True)
