# 怀旧服惩戒骑士分析工具

这是一个专门为魔兽世界怀旧服惩戒骑士设计的本地化分析工具，帮助玩家分析和改进他们在团队副本中的表现。

## 功能特点

- **战斗总览**：显示DPS、总伤害、暴击率等关键指标
- **技能分析**：分析技能使用效率和伤害输出情况
- **施法时间分析**：分析施法时间和空闲时间，帮助优化技能循环
- **性能检查列表**：提供一系列检查项，帮助玩家评估自己的表现
- **多种数据来源**：支持本地日志文件和WarcraftLogs链接两种数据来源
- **国服支持**：支持国际服和国服的WarcraftLogs链接格式

## 安装和使用

### 安装依赖

本工具使用Python编写，需要安装Python 3.6或更高版本。

```bash
# 安装Python（如果尚未安装）
# 访问 https://www.python.org/downloads/ 下载并安装Python

# 安装tkinter（大多数Python安装已包含）
# 如果没有，可以使用以下命令安装
# Windows: 通常已包含在Python安装中
# Linux: sudo apt-get install python3-tk
# Mac: brew install python-tk

# 安装其他依赖
pip install re datetime
```

### 运行应用程序

```bash
# 直接运行Python脚本
python main.py
```

#### Windows PowerShell特别说明

如果您使用的是Windows PowerShell，请注意PowerShell不支持使用`&&`连接命令。请使用以下方式运行应用程序：

```powershell
# 先切换到应用程序目录
cd RetributionPaladinAnalyzer

# 然后运行Python脚本
python main.py
```

或者使用PowerShell的分号语法：

```powershell
cd RetributionPaladinAnalyzer; python main.py
```

## 使用方法

### 使用本地日志文件

1. 启动应用后，选择"本地文件"选项卡
2. 点击"浏览..."按钮选择战斗日志文件（.txt 或 .json 格式）
3. 点击"分析"按钮，系统会自动分析日志并生成报告
4. 查看各个分析页面，了解你的表现和改进建议

### 使用WarcraftLogs链接

1. 启动应用后，选择"WarcraftLogs"选项卡
2. 在输入框中粘贴WarcraftLogs报告链接
   - 国际服格式：`https://classic.warcraftlogs.com/reports/ABCDEFG`
   - 国服格式：`https://cn.classic.warcraftlogs.com/reports/ABCDEFG`
   - 完整链接示例：`https://cn.classic.warcraftlogs.com/reports/YGz7xwhaqRdpCcHB?fight=7&type=damage-done`
3. 点击"获取数据"按钮，系统会从WarcraftLogs获取战斗和玩家信息
4. 从下拉菜单中选择要分析的战斗和玩家
5. 点击"分析"按钮，系统会分析选定的战斗数据并生成报告

### 保存分析结果

无论使用哪种数据来源，您都可以点击"保存分析结果"按钮将分析结果保存为JSON文件，以便日后查看或分享。

## 技术说明

- 使用Python的tkinter库构建图形界面
- 简单易用，无需复杂的Web技术或数据库
- 轻量级应用，可在任何支持Python的平台上运行
- 支持从WarcraftLogs获取数据（当前版本使用模拟数据）

### 关于WarcraftLogs API

当前版本使用模拟数据演示WarcraftLogs功能。要使用真实API数据，需要：

1. 拥有并关联Battle.net账号（**必须条件**）：WarcraftLogs API要求用户必须拥有Battle.net账号并与WarcraftLogs账号关联
2. 在WarcraftLogs开发者门户注册应用：https://www.warcraftlogs.com/api/clients/
3. 获取API密钥和客户端ID
4. 实现OAuth2认证流程
5. 使用API密钥发送请求到WarcraftLogs API

> **重要提示**：根据WarcraftLogs官方要求，"You must have a linked Battle.net account to create a key for or use the API"（您必须拥有关联的Battle.net账号才能创建密钥或使用API）。如果您没有关联Battle.net账号，将无法获取API密钥。

## 数据来源

本工具基于 [WoWAnalyzer](https://github.com/WoWAnalyzer/WoWAnalyzer) 项目的分析逻辑，专门提取了怀旧服惩戒骑士的相关内容，并进行了本地化和UI优化。

## 日志格式说明

### 本地日志格式

本地日志文件应遵循以下格式：
```
[时间] 玩家名 使用了 技能名 对 目标名 造成了 伤害值 点伤害 (可选:暴击)
```

例如：
```
[12:30:18] 光明使者 使用了 审判 对 奥妮克希亚 造成了 1500 点伤害
[12:30:20] 光明使者 使用了 十字军打击 对 奥妮克希亚 造成了 2200 点伤害 (暴击)
```

### WarcraftLogs链接

WarcraftLogs链接应为标准的WarcraftLogs报告链接，支持以下格式：

- 国际服：`https://classic.warcraftlogs.com/reports/ABCDEFG`
- 国服：`https://cn.classic.warcraftlogs.com/reports/ABCDEFG`

链接中可能包含额外参数（如fight、type等），程序会自动提取报告ID。

## 常见问题

### 应用程序无法启动

1. 确保已安装Python 3.6或更高版本
2. 确保已安装tkinter库
3. 在命令行中运行`python main.py`，查看是否有错误信息

### 无法解析WarcraftLogs链接

1. 确保链接格式正确
2. 确保链接来自classic.warcraftlogs.com或cn.classic.warcraftlogs.com
3. 程序会自动提取报告ID，无需手动处理链接参数

## 贡献

欢迎提交 Issue 或 Pull Request 来帮助改进这个工具。 