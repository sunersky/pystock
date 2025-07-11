"""
构建A股数据自动更新工具
"""
import os
import sys
import subprocess
import shutil

def main():
    print("=" * 60)
    print("构建A股数据自动更新工具")
    print("=" * 60)
    
    # 检查PyInstaller是否安装
    try:
        import PyInstaller
        print("PyInstaller已安装，版本:", PyInstaller.__version__)
    except ImportError:
        print("PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("PyInstaller安装完成")
    
    # 构建前清理
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            print(f"清理 {folder} 文件夹...")
            shutil.rmtree(folder)
    
    # 构建命令
    build_cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--icon=stock.ico" if os.path.exists("stock.ico") else "",
        "--name=A股数据自动更新工具",
        "auto_run.py"
    ]
    
    # 移除空选项
    build_cmd = [cmd for cmd in build_cmd if cmd]
    
    print("开始构建...")
    print("执行命令:", " ".join(build_cmd))
    subprocess.run(build_cmd, check=True)
    
    print("构建完成！")
    print("可执行文件位于:", os.path.join("dist", "A股数据自动更新工具.exe"))
    print("=" * 60)

if __name__ == "__main__":
    main() 