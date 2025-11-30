from pathlib import Path
import sqlite3

DB_FILE = Path("/data/demo.db")


def preparar_pasta() -> None:
    """Garante que a pasta do volume exista antes de salvar o banco."""
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)


def montar_banco() -> int:
    """Cria a tabela de clientes e insere os registros base."""
    registros = [
        (1, "Alice", "alice@example.com"),
        (2, "Bruno", "bruno@example.com"),
        (3, "Carla", "carla@example.com"),
    ]

    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
            """
        )
        cursor.executemany(
            "INSERT OR IGNORE INTO customers (id, name, email) VALUES (?, ?, ?)",
            registros,
        )
        connection.commit()

    return len(registros)


def main() -> None:
    """Fluxo principal: prepara volume e registra clientes exemplo."""
    preparar_pasta()
    total_planejado = montar_banco()
    print("Arquivo do banco:", DB_FILE)
    print("Total de cadastros planejados:", total_planejado)
    print("Rodar de novo nao duplica, entao ta ok para demonstrar volume.")


if __name__ == "__main__":
    main()
