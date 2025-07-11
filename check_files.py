"""
检查工具 - 验证日志中的下载记录与实际文件是否匹配
"""
import os
import re
import sys
import pandas as pd
from datetime import datetime

# 配置
ROOT_DIR = "D:/股票归档"
DATA_DIR = os.path.join(ROOT_DIR, "A_Stock_Data")
INDEX_FILE = os.path.join(ROOT_DIR, "stock_index.csv")

def print_header(message):
    """打印带格式的标题"""
    print("=" * 60)
    print(message)
    print("=" * 60)

def get_actual_files():
    """获取实际存在的文件列表"""
    files_dict = {}
    total_files = 0
    
    # 检查目录是否存在
    if not os.path.exists(DATA_DIR):
        print(f"错误: 目录 {DATA_DIR} 不存在")
        return files_dict, 0
    
    # 遍历所有年份目录
    for year_dir in os.listdir(DATA_DIR):
        year_path = os.path.join(DATA_DIR, year_dir)
        if not os.path.isdir(year_path):
            continue
            
        # 获取该年份目录下的所有文件
        files = [f for f in os.listdir(year_path) if f.endswith('.xlsx') and not f.startswith('~$')]
        
        # 解析文件名获取股票代码
        for file in files:
            match = re.match(r'(\d{6})_(.+)\.xlsx', file)
            if match:
                stock_code = match.group(1)
                stock_name = match.group(2)
                files_dict[stock_code] = {
                    '股票代码': stock_code,
                    '股票名称': stock_name,
                    '文件路径': os.path.join(year_path, file),
                    '年份目录': year_dir
                }
                total_files += 1
    
    return files_dict, total_files

def get_index_records():
    """获取索引文件中的记录"""
    if not os.path.exists(INDEX_FILE):
        print(f"错误: 索引文件 {INDEX_FILE} 不存在")
        return {}, 0
    
    try:
        df = pd.read_csv(INDEX_FILE, encoding='utf-8')
        
        # 打印索引文件的前几行，查看格式
        print("\n索引文件前5行:")
        print(df.head().to_string())
        print(f"索引文件列名: {list(df.columns)}")
        
        records = {}
        for _, row in df.iterrows():
            # 检查股票代码格式
            stock_code = str(row['股票代码'])
            
            # 如果股票代码不是6位数，尝试补齐
            if len(stock_code) < 6:
                stock_code = stock_code.zfill(6)
                print(f"警告: 股票代码 {row['股票代码']} 不是6位数，已补齐为 {stock_code}")
            
            records[stock_code] = {
                '股票代码': stock_code,
                '股票名称': row['股票名称'],
                '上市日期': row['上市日期'] if '上市日期' in df.columns else '',
                '上市年限': row['上市年限'] if '上市年限' in df.columns else 0,
                '文件路径': row['文件路径'] if '文件路径' in df.columns else ''
            }
        return records, len(records)
    except Exception as e:
        print(f"读取索引文件时出错: {str(e)}")
        return {}, 0

def main():
    print_header("文件系统与索引一致性检查工具")
    
    # 获取实际文件
    print("正在扫描文件系统...")
    actual_files, actual_count = get_actual_files()
    print(f"文件系统中找到 {actual_count} 个股票数据文件")
    
    # 显示部分实际文件信息
    print("\n文件系统中的部分文件:")
    for i, (code, info) in enumerate(list(actual_files.items())[:5]):
        print(f"{i+1}. 股票代码: {code}, 股票名称: {info['股票名称']}, 路径: {info['文件路径']}")
    
    # 获取索引记录
    print("\n正在读取索引文件...")
    index_records, index_count = get_index_records()
    print(f"索引文件中有 {index_count} 条记录")
    
    # 比较差异
    print("\n开始比较差异...")
    
    # 1. 在文件系统中存在但索引中不存在的文件
    missing_in_index = []
    for code in actual_files:
        if code not in index_records:
            # 检查是否因为前导零的问题
            no_leading_zeros = code.lstrip('0')
            if no_leading_zeros in index_records:
                print(f"发现代码格式不匹配: 文件系统中为 {code}，索引中为 {no_leading_zeros}")
                continue
                
            missing_in_index.append({
                '股票代码': code,
                '股票名称': actual_files[code]['股票名称'],
                '文件路径': actual_files[code]['文件路径'],
                '年份目录': actual_files[code]['年份目录']
            })
    
    # 2. 在索引中存在但文件系统中不存在的记录
    missing_in_fs = []
    for code in index_records:
        if code not in actual_files:
            # 检查是否因为前导零的问题
            code_with_zeros = code.zfill(6)
            if code_with_zeros in actual_files:
                print(f"发现代码格式不匹配: 索引中为 {code}，文件系统中为 {code_with_zeros}")
                continue
                
            missing_in_fs.append({
                '股票代码': code,
                '股票名称': index_records[code]['股票名称'],
                '文件路径': index_records[code]['文件路径'],
                '上市年限': index_records[code]['上市年限']
            })
    
    # 3. 路径不一致的记录
    path_mismatch = []
    for code in actual_files:
        if code in index_records:
            actual_path = actual_files[code]['文件路径']
            index_path = index_records[code]['文件路径']
            if actual_path != index_path:
                path_mismatch.append({
                    '股票代码': code,
                    '股票名称': actual_files[code]['股票名称'],
                    '实际路径': actual_path,
                    '索引路径': index_path
                })
    
    # 打印结果
    print_header("检查结果")
    
    print(f"文件系统中有 {actual_count} 个文件，索引中有 {index_count} 条记录")
    print(f"差异: {abs(actual_count - index_count)} 个")
    
    if missing_in_index:
        print(f"\n在文件系统中存在但索引中不存在的文件: {len(missing_in_index)} 个")
        for i, item in enumerate(missing_in_index[:10], 1):
            print(f"{i}. {item['股票代码']} - {item['股票名称']} ({item['年份目录']})")
        if len(missing_in_index) > 10:
            print(f"... 以及其他 {len(missing_in_index) - 10} 个文件")
    else:
        print("\n所有文件都已在索引中记录")
    
    if missing_in_fs:
        print(f"\n在索引中存在但文件系统中不存在的记录: {len(missing_in_fs)} 个")
        for i, item in enumerate(missing_in_fs[:10], 1):
            print(f"{i}. {item['股票代码']} - {item['股票名称']} (上市年限: {item['上市年限']})")
        if len(missing_in_fs) > 10:
            print(f"... 以及其他 {len(missing_in_fs) - 10} 个记录")
    else:
        print("\n索引中的所有记录都有对应的文件")
    
    if path_mismatch:
        print(f"\n路径不一致的记录: {len(path_mismatch)} 个")
        for i, item in enumerate(path_mismatch[:5], 1):
            print(f"{i}. {item['股票代码']} - {item['股票名称']}")
            print(f"   实际: {item['实际路径']}")
            print(f"   索引: {item['索引路径']}")
        if len(path_mismatch) > 5:
            print(f"... 以及其他 {len(path_mismatch) - 5} 个记录")
    
    # 提供修复建议
    print_header("修复建议")
    
    if missing_in_index:
        print("1. 更新索引文件，添加缺失的记录")
        print("   可以使用 astock_main.py 中的分类修复模式")
    
    if missing_in_fs or path_mismatch:
        print("2. 重新生成索引文件，确保与文件系统一致")
        print("   可以备份当前索引文件，然后运行初始化模式")
    
    print("\n检查完成！")

if __name__ == "__main__":
    main() 