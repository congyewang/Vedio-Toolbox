import random
import re
from pathlib import Path

from vedio_toolbox.toolbox.files import batch_rename


def generate_mock_data(num: int) -> list[str]:
    res = []

    for i in range(num):
        month = random.randint(4, 5)

        if month == 4:
            day = random.randint(1, 30)
        else:
            day = random.randint(1, 31)

        if day < 10:
            day = f"0{day}"
        else:
            day = str(day)

        hour = random.randint(1, 23)
        if hour < 10:
            hour0 = f"0{hour - 1}"
            hour1 = f"0{hour}"
        else:
            hour0 = str(hour - 1)
            hour1 = str(hour)

        minute1 = random.randint(0, 59)
        if minute1 < 10:
            minute1 = f"0{minute1}"
        else:
            minute1 = str(minute1)

        minute2 = random.randint(0, 59)
        if minute2 < 10:
            minute = f"0{minute2}"
        else:
            minute = str(minute2)

        s = f"2025-0{month}-{day}_{hour0}-{minute}_{hour1}-{minute}"
        res.append(s)
    return res


def create_folders(folder_names: list[str]) -> None:
    for folder_name in folder_names:
        path = Path(folder_name)
        try:
            path.mkdir(parents=True, exist_ok=True)
            print(f"文件夹 '{folder_name}' 创建成功。")
        except OSError as e:
            print(f"创建文件夹 '{folder_name}' 时发生错误: {e}")


def test_batch_rename(tmp_path) -> None:
    # 生成模拟数据
    create_folders([tmp_path])
    folder_name_list = generate_mock_data(10)
    create_folders([f"{tmp_path}/" + name for name in folder_name_list])

    batch_rename(tmp_path)

    # 验证重命名结果
    for folder_name in folder_name_list:
        old_name = Path(folder_name)
        new_name = old_name.with_name(
            re.sub(
                r"^(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})_(\d{2})-(\d{2})",
                r"\1_\3_\4_\5_\6_\7",
                old_name.name,
            )
        )
        assert not old_name.exists()
        assert new_name.exists()
