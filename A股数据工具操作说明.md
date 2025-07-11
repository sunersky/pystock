# A股数据工具操作说明

## 📋 目录
1. [程序简介](#程序简介)
2. [系统要求](#系统要求)
3. [安装方法](#安装方法)
4. [运行方法](#运行方法)
5. [功能详解](#功能详解)
6. [参数选择指南](#参数选择指南)
7. [故障排除](#故障排除)
8. [注意事项](#注意事项)

---

## 🎯 程序简介

**A股数据工具**是一个专业的股票历史数据下载和归档工具，支持下载所有A股上市公司的完整历史交易数据。

### 核心功能
- ✅ **全量数据下载**：5,419只A股股票完整历史数据
- ✅ **智能分类存储**：按上市年限自动分类到对应文件夹
- ✅ **Excel格式输出**：包含12个关键交易指标
- ✅ **多线程下载**：3线程并行，大幅提升效率
- ✅ **断点续传**：支持中断重启，不重复下载
- ✅ **智能监控**：实时进度报告和自动优化

### 数据字段
每只股票包含以下12个字段：
1. 日期
2. 开盘价
3. 收盘价
4. 最高价
5. 最低价
6. 成交量
7. 成交金额
8. 振幅
9. 涨跌幅
10. 涨跌额
11. 换手率
12. 成交次数（智能算法估算）

---

## 💻 系统要求

### 硬件要求
- **操作系统**：Windows 7/8/10/11
- **内存**：4GB以上（推荐8GB）
- **硬盘空间**：10GB以上可用空间
- **网络**：稳定的互联网连接

### 软件依赖
- **Python 3.7+**（如使用源码版本）
- **Excel 2010+**（用于查看数据文件）

---

## 🔧 安装方法

### 方法一：使用可执行文件（推荐）
1. 下载 `A股数据工具.exe`
2. 双击运行即可，无需安装Python

### 方法二：使用Python源码
1. 确保已安装Python 3.7+
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行主程序：
   ```bash
   python astock_main.py
   ```

### 方法三：重新打包
如需自定义打包：
```bash
python build_main.py
```

---

## 🚀 运行方法

### 步骤1：启动程序
**可执行文件方式**：
- 双击 `A股数据工具.exe`

**源码方式**：
```bash
python astock_main.py
```

### 步骤2：选择速度模式
程序启动后会显示两个速度选项：

```
请选择速度模式:
1. 保守模式 - 稳定但较慢（预计15-22小时）
2. 优化模式 - 较快但风险稍高（预计8-12小时）
```

**推荐选择**：2 (优化模式)

### 步骤3：选择线程模式
```
请选择线程模式:
1. 单线程模式 - 稳定可靠
2. 3线程模式 - 速度提升40-50%
```

**推荐选择**：2 (3线程模式)

### 步骤4：选择功能模式
```
请选择运行模式:
1. 初始化模式 - 首次运行，下载所有可用历史数据
2. 更新模式 - 日常使用，仅追加最新数据
```

**首次使用选择**：1 (初始化模式)
**日常更新选择**：2 (更新模式)

---

## 📊 功能详解

### 初始化模式
- **功能**：下载全部5,419只A股股票的完整历史数据
- **适用**：首次使用或重建数据库
- **耗时**：
  - 单线程保守：15-22小时
  - 单线程优化：8-12小时
  - 3线程模式：3.5-7小时

### 更新模式
- **功能**：只下载最新的交易数据
- **适用**：日常数据更新
- **耗时**：5-30分钟

### 数据存储结构
```
股票历史数据/
├── 0年/          # 上市不足1年的股票
├── 1年/          # 上市1-2年的股票
├── 2年/          # 上市2-3年的股票
...
├── 35年/         # 上市35年以上的股票
└── 股票列表索引.xlsx  # 完整索引文件
```

### 文件命名规则
- **格式**：`股票代码_股票名称.xlsx`
- **示例**：`000001_平安银行.xlsx`

---

## 🎯 参数选择指南

### 速度模式选择
| 模式 | 特点 | 适用场景 | 预计时间 |
|------|------|----------|----------|
| 保守模式 | 最稳定，几乎不会失败 | 网络不稳定、首次使用 | 15-22小时 |
| 优化模式 | 速度快，风险可控 | 网络稳定、追求效率 | 8-12小时 |

### 线程模式选择
| 模式 | 特点 | 适用场景 | 速度提升 |
|------|------|----------|----------|
| 单线程 | 最稳定，兼容性好 | 网络环境较差 | 基准速度 |
| 3线程 | 速度快，已修复阻塞问题 | 网络稳定，追求效率 | 提升40-50% |

### 推荐配置组合
| 场景 | 速度模式 | 线程模式 | 预计时间 | 成功率 |
|------|----------|----------|----------|--------|
| 🥇 **最佳平衡** | 优化模式 | 3线程模式 | 3.5-7小时 | 85-90% |
| 🥈 **稳定优先** | 优化模式 | 单线程 | 8-12小时 | 95-98% |
| 🥉 **最稳定** | 保守模式 | 单线程 | 15-22小时 | 99% |

---

## 🔍 运行监控

### 进度显示
程序运行时会显示：
```
[INFO] 2025-01-08 21:36:52 - 进度: 100/5419 (1.8%), 成功率: 95.0%, 失败: 5
[INFO] 2025-01-08 21:37:15 - 进度: 150/5419 (2.8%), 成功率: 96.7%, 失败: 5
```

### 关键指标说明
- **进度**：已处理/总数量 (百分比)
- **成功率**：成功下载的比例
- **失败数**：下载失败的股票数量
- **ETA**：预计剩余时间

### 自动优化机制
- 成功率 > 85%：继续当前模式
- 成功率 70-85%：发出警告但继续
- 成功率 < 70%：自动建议降级到单线程

---

## ⚠️ 故障排除

### 常见问题及解决方案

#### 1. 程序无法启动
**现象**：双击exe无反应或报错
**解决方案**：
- 检查是否有杀毒软件拦截
- 尝试以管理员身份运行
- 检查系统是否缺少运行库

#### 2. 网络连接失败
**现象**：大量"网络请求失败"错误
**解决方案**：
- 检查网络连接
- 尝试切换到保守模式
- 避开网络高峰期（9:30-15:00）

#### 3. 下载速度过慢
**现象**：每只股票处理时间超过30秒
**解决方案**：
- 切换到优化模式
- 尝试3线程模式
- 选择网络较好的时段运行

#### 4. 程序假死或卡住
**现象**：长时间无进度更新
**解决方案**：
- 按Ctrl+C中断程序
- 重新启动，程序会自动续传
- 改用单线程模式

#### 5. Excel文件无法打开
**现象**：生成的Excel文件损坏
**解决方案**：
- 删除损坏的文件
- 重新运行程序下载该股票
- 检查磁盘空间是否充足

### 错误代码对照表
| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| 网络请求超时 | 网络不稳定 | 稍后重试或切换保守模式 |
| 股票代码无效 | 数据源问题 | 程序会自动跳过 |
| 文件写入失败 | 磁盘空间不足 | 清理磁盘空间 |
| 内存不足 | 系统资源不够 | 关闭其他程序或重启 |

---

## 📝 注意事项

### 使用建议
1. **运行时间**：建议在夜间运行，避开交易时间
2. **网络环境**：确保网络连接稳定
3. **磁盘空间**：预留至少10GB可用空间
4. **系统资源**：运行期间避免同时进行大量其他任务

### 重要提醒
1. **断点续传**：程序支持中断重启，不用担心重复下载
2. **数据更新**：建议每周运行一次更新模式
3. **备份建议**：定期备份生成的数据文件
4. **法律合规**：仅用于个人研究和学习，遵守相关法律法规

### 性能优化建议
1. **关闭杀毒软件实时监控**：提升文件写入速度
2. **使用SSD硬盘**：加快文件读写
3. **充足内存**：8GB以上内存有助于提升性能
4. **稳定网络**：有线网络比WiFi更稳定

---

## 📞 技术支持

### 文件说明
- `astock_main.py`：主程序源码
- `build_main.py`：打包脚本
- `requirements.txt`：Python依赖清单
- `A股数据工具.exe`：可执行程序
- `使用指南.md`：简要说明文档

### 日志文件
程序运行时会在控制台显示详细日志，包含：
- 运行状态信息
- 错误和警告信息
- 进度和统计信息

### 版本信息
- **当前版本**：3线程修复版
- **更新内容**：修复多线程阻塞问题，增加智能监控
- **兼容性**：支持Windows 7/8/10/11

---

## 🎉 结语

A股数据工具为您提供便捷、高效的股票数据获取方案。通过合理的参数配置和稳定的网络环境，您可以在几小时内获得完整的A股历史数据，为后续的数据分析和研究提供坚实基础。

如有问题，请参考本文档的故障排除章节，或检查程序运行日志中的详细错误信息。

**祝您使用愉快！** 📈 