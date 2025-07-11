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
    
    # 创建spec文件
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['auto_run.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pandas', 'openpyxl', 'akshare', 'numpy', 'requests', 'colorama'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='A股数据自动更新工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='stock.ico' if os.path.exists('stock.ico') else None,
)
"""
    
    # 写入spec文件
    with open("auto_run.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("已创建自定义spec文件")
    
    # 构建命令
    build_cmd = [
        "pyinstaller",
        "--noconfirm",
        "auto_run.spec"
    ]
    
    print("开始构建...")
    print("执行命令:", " ".join(build_cmd))
    subprocess.run(build_cmd, check=True)
    
    print("构建完成！")
    print("可执行文件位于:", os.path.join("dist", "A股数据自动更新工具.exe"))
    print("=" * 60)

if __name__ == "__main__":
    main() 