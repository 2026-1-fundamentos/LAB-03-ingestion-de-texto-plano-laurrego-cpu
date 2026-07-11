"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """
    import re

    import pandas as pd

    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as file:
        lines = [line.rstrip("\n") for line in file]

    sep_idx = next(
        i for i, line in enumerate(lines) if line.strip().startswith("---")
    )

    header_line1 = lines[0]
    col_cluster = header_line1.find("Cluster")
    col_cantidad = header_line1.find("Cantidad de")
    col_porcentaje = header_line1.find("Porcentaje de")
    col_palabras = header_line1.find("Principales palabras clave")

    columns = [
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave",
    ]

    def _collapse_spaces(text):
        return re.sub(r"\s+", " ", text).strip()

    records = []
    current = None

    for line in lines[sep_idx + 1 :]:
        if line.strip() == "":
            if current is not None:
                records.append(current)
                current = None
            continue

        cluster_chunk = line[col_cluster:col_cantidad].strip()
        cantidad_chunk = line[col_cantidad:col_porcentaje].strip()
        porcentaje_chunk = line[col_porcentaje:col_palabras].strip()
        palabras_chunk = _collapse_spaces(line[col_palabras:])

        if cluster_chunk:
            if current is not None:
                records.append(current)
            current = {
                "cluster": int(cluster_chunk),
                "cantidad_de_palabras_clave": int(cantidad_chunk),
                "porcentaje_de_palabras_clave": float(
                    porcentaje_chunk.replace("%", "").strip().replace(",", ".")
                ),
                "principales_palabras_clave": palabras_chunk,
            }
        else:
            if palabras_chunk:
                current["principales_palabras_clave"] = _collapse_spaces(
                    current["principales_palabras_clave"] + " " + palabras_chunk
                )

    if current is not None:
        records.append(current)

    df = pd.DataFrame(records, columns=columns)

    def _normalize_keywords(value):
        value = _collapse_spaces(value).rstrip(".").strip()
        words = [word.strip() for word in value.split(",")]
        words = [word for word in words if word]
        return ", ".join(words)

    df["principales_palabras_clave"] = df["principales_palabras_clave"].apply(
        _normalize_keywords
    )

    return df


if __name__ == "__main__":
    print(pregunta_01())
