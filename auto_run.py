"""
A股数据自动更新脚本
自动检测并使用最快的方式更新数据
"""
import os
import sys
import time

def main():
    print("=" * 60)
    print("A股数据自动更新工具")
    print("=" * 60)
    print("将自动使用最快的方式更新数据...")
    print()
    
    # 直接导入并调用主程序的自动模式
    try:
        # 导入主模块
        sys.argv = [sys.argv[0], "--auto"]  # 模拟命令行参数
        import astock_main
        
        # 直接调用自动模式函数
        astock_main.auto_mode()
        print("自动更新完成！")
    except KeyboardInterrupt:
        print("用户中断了更新过程")
    except Exception as e:
        print(f"自动更新过程中发生错误: {str(e)}")
    
    print("=" * 60)
    input("按任意键退出...")

if __name__ == "__main__":
    main() 