"""
修复工具 - 确保索引文件中的股票代码都是6位数格式
"""
import os
import pandas as pd

# 配置
ROOT_DIR = "D:/股票归档"
INDEX_FILE = os.path.join(ROOT_DIR, "stock_index.csv")
BACKUP_FILE = os.path.join(ROOT_DIR, "stock_index_backup.csv")

def print_header(message):
    """打印带格式的标题"""
    print("=" * 60)
    print(message)
    print("=" * 60)

def fix_stock_codes():
    """修复索引文件中的股票代码格式"""
    if not os.path.exists(INDEX_FILE):
        print(f"错误: 索引文件 {INDEX_FILE} 不存在")
        return False
    
    print(f"正在读取索引文件: {INDEX_FILE}")
    
    try:
        # 备份原始文件
        import shutil
        shutil.copy2(INDEX_FILE, BACKUP_FILE)
        print(f"已备份原始索引文件至: {BACKUP_FILE}")
        
        # 读取索引文件
        df = pd.read_csv(INDEX_FILE, encoding='utf-8')
        
        # 显示原始数据的前几行
        print("\n原始索引文件前5行:")
        print(df.head().to_string())
        
        # 统计需要修复的股票代码数量
        non_six_digit_codes = 0
        for _, row in df.iterrows():
            stock_code = str(row['股票代码'])
            if len(stock_code) != 6:
                non_six_digit_codes += 1
        
        print(f"\n检测到 {non_six_digit_codes} 个非6位数股票代码需要修复")
        
        if non_six_digit_codes == 0:
            print("所有股票代码已经是6位数格式，无需修复")
            return True
        
        # 修复股票代码格式
        fixed_codes = []
        for _, row in df.iterrows():
            stock_code = str(row['股票代码'])
            if len(stock_code) != 6:
                fixed_code = stock_code.zfill(6)
                fixed_codes.append((stock_code, fixed_code))
                row['股票代码'] = fixed_code
        
        # 显示部分修复结果
        print("\n部分修复示例:")
        for i, (old_code, new_code) in enumerate(fixed_codes[:10]):
            print(f"{i+1}. {old_code} -> {new_code}")
        
        if len(fixed_codes) > 10:
            print(f"... 以及其他 {len(fixed_codes) - 10} 个代码")
        
        # 保存修复后的索引文件
        df.to_csv(INDEX_FILE, index=False, encoding='utf-8')
        print(f"\n已保存修复后的索引文件: {INDEX_FILE}")
        
        # 显示修复后的数据
        print("\n修复后的索引文件前5行:")
        print(df.head().to_string())
        
        print(f"\n成功修复了 {len(fixed_codes)} 个股票代码")
        return True
        
    except Exception as e:
        print(f"修复过程中发生错误: {str(e)}")
        return False

def main():
    print_header("股票代码格式修复工具")
    
    if fix_stock_codes():
        print_header("修复成功")
    else:
        print_header("修复失败")

if __name__ == "__main__":
    main() 