import re

def sanitize_filename(filename):
    # 移除或替换 Windows 不允许的字符
    return re.sub(r'[<>:"/\\|?*]', "_", filename)
