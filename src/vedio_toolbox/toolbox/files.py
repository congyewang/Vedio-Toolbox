import os
import re


def batch_rename(
    root_dir: str,
    pattern_str: str = r"^(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})_(\d{2})-(\d{2})(?:\..*)?$",
) -> None:
    """
    批量重命名指定目录下的子文件夹和文件。

    将 "YYYY-mm-DD_HH-MM_HH-MM" 格式重命名为 "m_DD_HH_MM_HH_MM"。
    如果月份小于10，则月份前的0会被移除。

    参数:
        root_dir (str): 要处理的根目录路径。
    """
    # 正则表达式匹配 YYYY-mm-DD_HH-MM_HH-MM 格式，不包括扩展名
    pattern = re.compile(pattern_str)

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # 重命名文件
        for filename in filenames:
            match = pattern.match(filename)
            if match:
                # 分离文件名和扩展名
                name, ext = os.path.splitext(filename)

                # 获取匹配的组
                year, month, day, hour1, min1, hour2, min2 = match.groups()[:7]

                # 如果月份小于10，移除前导零
                new_month = str(int(month))

                # 创建新的文件名（保留原来的扩展名）
                new_name = f"{new_month}_{day}_{hour1}_{min1}_{hour2}_{min2}{ext}"

                # 检查新的文件名是否已经存在
                new_filepath = os.path.join(dirpath, new_name)
                if os.path.exists(new_filepath):
                    print(
                        f"警告：文件 '{new_filepath}' 已存在，跳过重命名 '{filename}'"
                    )
                    continue

                try:
                    os.rename(os.path.join(dirpath, filename), new_filepath)
                    print(f'文件已重命名: "{filename}" -> "{new_name}"')
                except OSError as e:
                    print(f"错误：重命名文件 '{filename}' 失败: {e}")

        # 重命名子文件夹
        for dirname in dirnames:
            match = pattern.match(dirname)
            if match:
                year, month, day, hour1, min1, hour2, min2 = match.groups()[:7]

                # 如果月份小于10，移除前导零
                new_month = str(int(month))

                new_name = f"{new_month}_{day}_{hour1}_{min1}_{hour2}_{min2}"

                # 检查新的文件夹名是否已经存在
                new_dirpath = os.path.join(dirpath, new_name)
                if os.path.exists(new_dirpath):
                    print(
                        f"警告：文件夹 '{new_dirpath}' 已存在，跳过重命名 '{dirname}'"
                    )
                    continue

                try:
                    os.rename(os.path.join(dirpath, dirname), new_dirpath)
                    print(f'文件夹已重命名: "{dirname}" -> "{new_name}"')
                except OSError as e:
                    print(f"错误：重命名文件夹 '{dirname}' 失败: {e}")


if __name__ == "__main__":
    data_directory = "Italy"

    if os.path.isdir(data_directory):
        batch_rename(data_directory)
        print("\n批量重命名完成！")
    else:
        print(f"错误：目录 '{data_directory}' 不存在。请检查路径是否正确。")
