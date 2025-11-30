from pathlib import Path
import sqlite3
from typing import List, Tuple

DB_FILE = Path("/data/demo.db")


def carregar_registros() -> List[Tuple[int, str, str]]:
    """Busca todos os clientes cadastrados no banco compartilhado."""
    if not DB_FILE.exists():
        raise FileNotFoundError(
            f"Banco {DB_FILE} nao encontrado. Rode o container writer primeiro."
        )

    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, email FROM customers ORDER BY id")
        registros = cursor.fetchall()

    return [(int(row[0]), str(row[1]), str(row[2])) for row in registros]


def main() -> None:
    """Mostra o conteudo do banco para provar a persistencia."""
    registros = carregar_registros()
    print("Clientes cadastrados:")
    if not registros:
        print("Nenhum registro por aqui. Confere se o writer rodou direitinho.")
        return

    for identificador, nome, email in registros:
        print(f"{identificador} - {nome} ({email})")

    print("Se voce derrubou o container e ainda viu esses dados, parabens: volume funcionando!")


if __name__ == "__main__":
    main()
