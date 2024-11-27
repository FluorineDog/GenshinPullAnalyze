def parse_file(file_path):
    """
    解析给定文件，返回格式化的数据列表。
    
    参数:
        file_path (str): 要解析的文件路径。
        
    返回:
        list: 包含序列及其计数的列表。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    parsed_data = []
    for line in lines:
        # 去除每行末尾的换行符，并按空格分割
        if line.startswith('#'):
            continue
        parts = line.strip().split(')')
        # 第一部分是序列，第二部分是计数
        sequence_str = parts[0]
        count = int(parts[1])
        
        # 处理序列字符串
        sequence_str = sequence_str.strip('(')

        sequence = [int(num) for num in sequence_str.split(',') if num != '']
        parsed_data.append((sequence, count))
    
    return parsed_data


if __name__ == '__main__':
    file_path = 'resources/log.txt'  # 替换为你的文件路径
    raw_data = parse_file(file_path)
    print(raw_data)