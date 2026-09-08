# 新手安装指南

安装完成后，Codex 可以在中文写作任务中读取这套去 AI 味规则。你需要能访问本机文件的 Codex；仅把 ZIP 发到普通聊天窗口，不等于已安装到本地技能目录。

## 方式一：让 Codex 安装

把以下文字发给 Codex：

```text
请使用 skill-installer，从 https://github.com/momowangOUO/natural-writing-zh
安装仓库根目录的 natural-writing-zh 技能。
先检查是否已安装；若已存在，核对版本与差异后更新，不要安装重复副本。
保留其他技能和已有配置。完成后读取 SKILL.md，告诉我安装位置及是否能调用。
```

安装器若不可用，可以采用下面的手动方式。两种方式任选一种。

## 方式二：下载并放入文件夹

### 1. 下载

打开 [最新发布页](https://github.com/momowangOUO/natural-writing-zh/releases/latest)，在 **Assets** 中下载名称为 `natural-writing-zh-v版本号.zip` 的安装包。当前技能版本为 1.0.0，对应 `natural-writing-zh-v1.0.0.zip`。

选择这个专用安装包即可，不需要下载下方的 `Source code`。写作本身不需要 Git、命令行或 Python。

### 2. 解压

Windows：右键 ZIP，选择“全部解压缩”。macOS：双击 ZIP。

找到解压后的 `natural-writing-zh` 文件夹，打开确认能直接看到 `SKILL.md`。接下来复制的是这个文件夹，不是 ZIP 文件。

### 3. 打开技能目录

本指南的手动安装采用官方列出的用户技能目录 `~/.agents/skills`。本项目也曾在 `.codex/skills` 中完成本机安装检查；如果安装器已安装且 Codex 能读取，就保留现有位置，不必迁移或重复安装。[目录依据：OpenAI 文档](https://learn.chatgpt.com/docs/build-skills)

**Windows**

1. 按 `Win + R`，输入 `%USERPROFILE%`，按回车，打开你的用户文件夹。
2. 找到 `.agents` 文件夹。没有就新建，名称是 `.agents`，包含开头的点。
3. 打开 `.agents`，找到或新建 `skills` 文件夹。
4. 把刚才的 `natural-writing-zh` 文件夹复制到 `skills` 里面。

之后可以用 `Win + R` 输入 `%USERPROFILE%\.agents\skills` 直接打开该位置。

**macOS**

1. 在访达按 `Shift + Command + G`，输入 `~`，前往个人文件夹。
2. 按 `Command + Shift + .` 显示隐藏文件，找到或新建 `.agents` 文件夹。
3. 在 `.agents` 内找到或新建 `skills`，把 `natural-writing-zh` 文件夹复制进去。

若目录已经存在，也可以直接用“前往文件夹”打开 `~/.agents/skills`。

### 4. 检查目录层级

安装结果应当是：

```text
.agents/
└── skills/
    └── natural-writing-zh/
        ├── SKILL.md
        ├── LICENSE
        ├── agents/
        ├── references/
        └── scripts/
```

不能多套一层 `natural-writing-zh/natural-writing-zh/`，也不能只复制 `SKILL.md` 而漏掉参考文件。不要把文件改名成 `SKILL.md.txt`。

### 5. 确认可以读取

回到 Codex，新建一个任务并发送：

```text
请查找并读取 natural-writing-zh 的 SKILL.md 和文章参考，
告诉我实际读取的位置。如果找不到，请明确说明，不要假定已经加载。
```

如果没有发现技能，重启 Codex 后再试。官方文档说明技能通常会自动发现，未显示时可重启。[发现与调用说明](https://learn.chatgpt.com/docs/build-skills)

## 第一次写作

```text
使用 natural-writing-zh，改写下面的活动通知，去除 AI 味。
读者是附近居民；保持正式、清楚，不要增加材料里没有的信息。

材料：每周三19:30—21:00在书店举办夜读，连续试办四周。
居民自带书籍，每场最多12人，免费参加，提前报名。
19:30—20:30各自阅读，20:30—21:00交流。
```

在支持 `$` 提及技能的界面，也可写 `$natural-writing-zh`。不同界面的选择方式可能不同，直接要求“读取并使用 natural-writing-zh”更容易核对是否找到文件。

## 希望写作任务都使用它

可以请 Codex 将下列规则合并进全局 `~/.codex/AGENTS.md`，保留原有内容。不要用这段文字覆盖整个文件。

```text
创作或改写中文文章、PPT 文案、策划案、小说、游戏台词和游戏内文案时，
先读取已安装的 natural-writing-zh，并只加载相关文体参考。
开发任务新增或改写玩家可见文字时，先独立保存纯文本、检查，
再按原文接入并读回核对。已有作品与项目设定、用户当前要求优先。
普通问答、过程汇报和不涉及玩家文字的代码工作不强制调用。
用户只要求文案时不修改项目；已经要求实现时检查后自动接入。
```

这是额外的调用指引，不保证每次输出的质量。全局文件机制见 [AGENTS.md 官方说明](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。

## 常见问题

| 情况 | 怎么处理 |
|---|---|
| Codex 说找不到技能 | 核对文件位置、目录层级和文件名，再重启；让它检查实际扫描的目录 |
| 发现了两份同名技能 | 保留一份有效安装，先核对位置再移除重复副本；不要删除其他技能 |
| 已安装，但文案仍生硬 | 明确要求读取技能，提供上下文并指出具体句段；安装成功不等于文风已满足要求 |
| 游戏台词直接写进了代码 | 要求按接入参考补齐独立文本稿、连贯检查和读回核对 |
| 不知道要不要装 Python | 只写文案不用装；开发者运行可选核对工具时才需要 Python 3 |
| 想在其他 AI 工具里用 | 先查该工具的技能格式与安装位置；本仓库尚未验证其他工具的兼容性 |

## 更新与卸载

更新前记录当前安装位置，并备份你自己修改过的内容。下载新版后替换同一位置的技能文件夹，再让 Codex 读取确认；不要把新版装到另一个目录与旧版并存。仓库首页更新不一定代表技能版本更新，下载版本以发布页为准。

卸载时移除已确认的 `natural-writing-zh` 文件夹；若曾添加全局调用规则，一并移除对应段落，保留其他规则与技能。

[返回首页](../README.md) · [查看修改前后](before-after.md)
