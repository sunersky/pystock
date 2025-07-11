"""
A股数据自动更新脚本
自动检测并使用最快的方式更新数据
"""
import os
import sys
import subprocess
import time

def main():
    print("=" * 60)
    print("A股数据自动更新工具")
    print("=" * 60)
    print("将自动使用最快的方式更新数据...")
    print()
    
    # 运行主程序的自动模式
    try:
        subprocess.run([sys.executable, "astock_main.py", "--auto"], check=True)
        print("自动更新完成！")
    except subprocess.CalledProcessError:
        print("自动更新过程中发生错误")
    except KeyboardInterrupt:
        print("用户中断了更新过程")
    
    print("=" * 60)
    input("按任意键退出...")

if __name__ == "__main__":
    main() 