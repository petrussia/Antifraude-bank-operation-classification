"""Скачать данные задачи «Страж» из Data Fusion Contest 2026."""

from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urljoin
from urllib.request import urlretrieve


# Размеры в байтах помогают отличить готовый файл от оборванной загрузки.
FILES = {
    "pretrain_part_1.parquet": 625238291,
    "pretrain_part_2.parquet": 622755429,
    "pretrain_part_3.parquet": 625160375,
    "train_part_1.parquet": 688088514,
    "train_part_2.parquet": 686544805,
    "train_part_3.parquet": 685373099,
    "train_labels.parquet": 1157397,
    "pretest.parquet": 338850719,
    "test.parquet": 17195864,
    "sample_submit.csv": 21904984,
}


def download(file_url, folder):
    folder.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=folder) as temp:
        for name, size in FILES.items():
            target = folder / name
            if target.is_file() and target.stat().st_size == size:
                print(f"Уже скачан: {name}")
                continue
            print(f"Скачиваю {name} ({size / 1_000_000:.1f} МБ)", flush=True)
            partial = Path(temp) / name
            urlretrieve(urljoin(file_url, name), partial)
            if partial.stat().st_size != size:
                raise ValueError(f"Размер {name} отличается от ожидаемого")
            partial.replace(target)


if __name__ == "__main__":
    link = input("Прямая ссылка на любой файл датасета из кабинета ODS: ").strip()
    download(link, Path(__file__).resolve().parent / "data")
