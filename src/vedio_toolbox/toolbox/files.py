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


def batch_rename_videos_in_directory(root_dir: str) -> None:
    """
    遍历指定目录及其所有子目录，根据特定规则重命名视频文件。

    原始格式: YYYY-mm-DD_HH-MM_HH-MM
    新格式: m_DD_HH_MM_HH_MM (例如: 2_15_10_30_11_00.mp4)

    Args:
        root_dir (str): 要处理的根目录的路径。
    """
    # 正则表达式用于匹配 "YYYY-mm-DD_HH-MM_HH-MM" 格式的文件名
    filename_pattern = re.compile(
        r"(\d{4})-(\d{2})-(\d{2})_(\d{2}-\d{2})_(\d{2}-\d{2})\..+"
    )

    print(f"正在扫描 '{root_dir}' 文件夹及其子文件夹...")

    files_renamed_count = 0
    files_scanned_count = 0

    # os.walk() 会遍历指定目录下的所有文件夹和文件
    for subdir, _, files in os.walk(root_dir):
        for filename in files:
            files_scanned_count += 1
            match = filename_pattern.match(filename)

            if match:
                # 提取文件名中的日期和时间部分
                year, month, day, time1, time2 = match.groups()

                # 获取文件的扩展名
                extension = os.path.splitext(filename)[1]

                # 根据规则处理月份：如果月份以 '0' 开头，则去掉 '0'
                new_month = month.lstrip("0")

                # *** 这是修改过的关键行 ***
                # 将时间部分 "HH-MM" 中的 '-' 替换为 '_'
                new_time_part = f"{time1.replace('-', '_')}_{time2.replace('-', '_')}"

                # 构建新的文件名
                new_filename = f"{new_month}_{day}_{new_time_part}{extension}"

                # 获取旧文件和新文件的完整路径
                old_filepath = os.path.join(subdir, filename)
                new_filepath = os.path.join(subdir, new_filename)

                try:
                    # 重命名文件
                    os.rename(old_filepath, new_filepath)
                    print(f"成功: '{old_filepath}'  ->  '{new_filepath}'")
                    files_renamed_count += 1
                except OSError as e:
                    print(f"错误: 重命名 '{old_filepath}' 时发生错误: {e}")

    print("\n--- 任务完成 ---")
    print(f"总共扫描文件: {files_scanned_count} 个")
    print(f"成功重命名文件: {files_renamed_count} 个")
