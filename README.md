# 智能文档生成工具

一个基于 CrewAI 的多智能体文档生成系统，能够自动分析 GitHub 项目并生成高质量的中文文档。

## 功能特性

### 🎯 双模式文档生成
- **项目介绍模式**: 从用户角度生成项目功能、价值和使用场景的介绍文档
- **技术文档模式**: 为开发者生成精简的技术架构、API 参考和实现文档

### 🤖 智能工作流
- 自动分析代码库结构和功能
- 智能规划文档结构
- 多智能体协作撰写和评审
- 自动生成流程图和架构图

### 📚 输出格式
- Markdown/MDX 格式文档
- Mermaid 流程图和架构图
- 用户友好的项目介绍
- 详细的技术参考文档

## 系统架构
```
📦 文档生成系统
├── 🔍 分析阶段
│ ├── 代码探索智能体
│ └── 文档规划智能体
├── ✍️ 撰写阶段
│ ├── 文档撰写智能体
│ └── 质量评审智能体
├── 📄 输出阶段
│ ├── 项目介绍文档
└ └── 技术参考文档
```

## 快速开始

### 环境要求

- Python 3.12+
- Ollama (运行 deepseek-r1 模型)
- Git

### 安装步骤

1.**安装依赖**
```
pip install -r requirements.txt
```

2. **启动 Ollama 服务**
```
# 安装并启动 Ollama
ollama serve

# 下载 deepseek-r1 模型
ollama pull deepseek-r1:7b
```

### 使用方法

#### 方式一: MCP 服务器模式

1. **启动服务器**
```
python server.py
```

2. **使用工具函数**
```
# 生成文档
write_documentation("https://github.com/username/repo")

# 查看文档列表
list_docs()

# 查看文档内容
view_content("docs/项目概述.mdx")

# 获取帮助
get_help()
```

#### 方式二: 直接运行模式

```
python main.py
# 输入 GitHub 仓库 URL
```

## 配置说明

### 智能体配置

系统包含多个专业智能体：

- **代码探索专家**: 分析代码库结构和架构
- **文档规划师**: 制定文档策略和计划  
- **文档撰写专员**: 编写高质量文档内容
- **质量评审专员**: 确保文档准确性和一致性

### 任务配置

支持两种任务模式：

1. **项目库文档模式** (`*_program_zh.yaml`)
   - 面向项目介绍和用户文档
   - 关注功能价值和用户体验
   - 业务逻辑和流程图

2. **代码库文档模式** (`*_code_zh.yaml`) 
   - 面向技术参考文档
   - 关注架构设计和 API 参考
   - 技术实现和代码示例

## 项目结构
```
doc-generator/
├── config/ # 配置文件
│ ├── planner_agents_program_zh.yaml # 规划智能体配置
│ ├── planner_tasks_program_zh.yaml # 规划任务配置
│ ├── documentation_agents_program_zh.yaml # 文档智能体配置
│ └── documentation_tasks_program_zh.yaml # 文档任务配置
├── docs/ # 生成的文档
├── workdir/ # 临时工作目录
├── crew.py # 智能体组初始化
├── documentation_flow.py # 文档生成流程
├── main.py # 主程序，负责协调
├── server.py # MCP 服务器
├── utils.py # 工具函数
└── models.py # 数据模型
```


## 工作流程

1. **仓库克隆**: 自动克隆目标 GitHub 仓库
2. **代码分析**: 分析项目结构、功能和架构
3. **文档规划**: 制定最适合的文档计划
4. **文档撰写**: 多智能体协作撰写文档
5. **质量评审**: 验证文档准确性和完整性
6. **输出保存**: 生成最终的 Markdown 文档

## 示例输出

### 项目介绍文档
- `项目概述.mdx` - 项目核心功能和价值
- `快速开始.mdx` - 安装和使用指南  
- `核心功能.mdx` - 主要特性详细介绍
- `架构设计.mdx` - 系统架构和实现逻辑

### 技术文档
- `API参考.mdx` - 接口文档和用法示例
- `开发指南.mdx` - 二次开发说明
- `部署指南.mdx` - 生产环境部署

## 故障排除

### 常见问题

1. **Ollama 连接失败**
   - 确保 Ollama 服务正在运行: `ollama serve`
   - 检查模型是否已下载: `ollama list`

2. **仓库克隆失败**
   - 验证 GitHub URL 格式
   - 检查网络连接和访问权限

3. **文档生成失败**
   - 检查目标仓库是否包含可分析代码
   - 验证依赖包版本兼容性

### 日志查看

系统会输出详细的过程日志，帮助诊断问题：

```
# 查看生成流程状态
python main.py
```

## 技术栈

- **CrewAI**: 多智能体框架
- **Ollama**: 本地 LLM 服务
- **MCP**: 模型上下文协议
- **Pydantic**: 数据验证
- **DeepSeek-R1**: 中文优化模型

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 许可证

MIT License

## 支持

如有问题，请提交 GitHub Issue 或联系开发团队。