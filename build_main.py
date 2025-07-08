"""
A股数据本地化归档工具 - 主程序打包脚本
符合需求文档V2.0
"""
import os
import sys
import shutil
from datetime import datetime
import subprocess

def log_message(message):
    """输出日志信息"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def create_build_spec():
    """创建PyInstaller规格文件"""
    log_message("创建PyInstaller规格文件...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

# 添加akshare数据文件
def get_akshare_data_files():
    """获取akshare数据文件路径"""
    try:
        import akshare
        akshare_path = os.path.dirname(akshare.__file__)
        data_files = []
        
        # 查找所有数据文件
        for root, dirs, files in os.walk(akshare_path):
            for file in files:
                if file.endswith(('.json', '.csv', '.xlsx', '.txt', '.dat')):
                    src_path = os.path.join(root, file)
                    rel_path = os.path.relpath(src_path, akshare_path)
                    dst_path = os.path.join('akshare', rel_path)
                    data_files.append((src_path, os.path.dirname(dst_path)))
        
        return data_files
    except:
        return []

# 获取akshare数据文件
akshare_data_files = get_akshare_data_files()

a = Analysis(
    ['astock_main.py'],
    pathex=[],
    binaries=[],
    datas=akshare_data_files + [
    ],
    hiddenimports=[
        'akshare',
        'akshare.stock',
        'akshare.stock.stock_zh_a_hist',
        'akshare.stock.stock_info_a_code_name',
        'akshare.futures',
        'akshare.futures.futures_basis',
        'akshare.futures.cons',
        'akshare.tool',
        'akshare.tool.data_download_tool',

        'pandas',
        'numpy',
        'openpyxl',
        'colorama',
        'urllib3',
        'requests',
        'bs4',
        'lxml',
        'json',
        'csv',
        'datetime',
        'time',
        'os',
        'sys',
        'warnings',
        'functools',
        'concurrent',
        'concurrent.futures',
        'threading',
        'multiprocessing'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'unittest',
        'test',
        'tests',
        'matplotlib',
        'PIL',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'scipy',
        'sklearn',
        'tensorflow',
        'torch'
    ],
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
    name='A股数据工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open('A股数据工具.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    log_message("规格文件创建成功: A股数据工具.spec")

def build_executable():
    """构建可执行文件"""
    log_message("开始构建可执行文件...")
    
    # 清理之前的构建
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # 使用spec文件构建
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        'A股数据工具.spec',
        '--clean',
        '--noconfirm'
    ]
    
    log_message(f"执行命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        
        if result.returncode == 0:
            log_message("构建成功!")
            return True
        else:
            log_message("构建失败!")
            log_message("错误输出:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        log_message("构建超时!")
        return False
    except Exception as e:
        log_message(f"构建过程中发生错误: {str(e)}")
        return False

def post_build_check():
    """构建后检查"""
    log_message("进行构建后检查...")
    
    exe_path = os.path.join('dist', 'A股数据工具.exe')
    
    if os.path.exists(exe_path):
        file_size = os.path.getsize(exe_path)
        file_size_mb = file_size / (1024 * 1024)
        log_message(f"可执行文件已生成: {exe_path}")
        log_message(f"文件大小: {file_size_mb:.1f} MB")
        
        # 移动到根目录
        root_exe_path = 'A股数据工具.exe'
        if os.path.exists(root_exe_path):
            os.remove(root_exe_path)
        
        shutil.copy2(exe_path, root_exe_path)
        log_message(f"文件已复制到根目录: {root_exe_path}")
        
        return True
    else:
        log_message("未找到可执行文件!")
        return False

def clean_build_files():
    """清理构建文件和脏数据"""
    log_message("清理构建文件和脏数据...")
    
    # 清理构建相关目录
    build_dirs = ['build', 'dist', '__pycache__']
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            log_message(f"删除目录: {dir_name}")
    
    # 清理spec文件（除了当前要使用的）
    spec_files = ['AStock_Real.spec', 'astock_main.spec']
    for spec_file in spec_files:
        if os.path.exists(spec_file):
            os.remove(spec_file)
            log_message(f"删除规格文件: {spec_file}")
    
    # 清理.pyc文件
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(('.pyc', '.pyo')):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                log_message(f"删除缓存文件: {file_path}")
    
    log_message("清理完成")

def main():
    """主函数"""
    print("=" * 60)
    print("A股数据工具 - 打包成exe")
    print("=" * 60)
    
    start_time = datetime.now()
    
    # 检查主程序文件是否存在
    if not os.path.exists('astock_main.py'):
        log_message("错误：未找到主程序文件 astock_main.py")
        return False
    
    # 清理构建文件和脏数据
    clean_build_files()
    
    # 创建规格文件
    create_build_spec()
    
    # 构建可执行文件
    if not build_executable():
        return False
    
    # 构建后检查
    if not post_build_check():
        return False
    
    # 清理构建过程中的临时文件
    log_message("清理构建临时文件...")
    if os.path.exists('build'):
        shutil.rmtree('build')
        log_message("删除build目录")
    
    # 完成统计
    end_time = datetime.now()
    duration = end_time - start_time
    
    log_message("=" * 60)
    log_message("打包完成!")
    log_message(f"耗时: {duration}")
    log_message("可执行文件: A股数据工具.exe")
    log_message("已内置反制机制和增强版算法，直接运行即可")
    log_message("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 打包成功!")
            print("可以运行 A股数据工具.exe 开始使用")
        else:
            print("\n❌ 打包失败!")
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"\n打包过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
    
    input("\n按任意键退出...") 