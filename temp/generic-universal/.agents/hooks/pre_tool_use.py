# pre_tool_use

> **作用**: 工具调用前时执行
> **工具**: 通用
> **类型**: 确定性执行（非建议性）

## 影响范围

- **触发时机**: 工具调用前
- **执行方式**: Python 脚本，100% 执行（不像指令文件是建议性的）
- **用途**: 自动化、安全检查、格式化、日志记录

## 格式说明

Python 脚本，接收事件参数：

```python
# pre_tool_use
# 触发: 工具调用前

import json
import sys

def main():
    # 读取事件数据
    event = json.load(sys.stdin)
    
    # 你的逻辑
    print(f"Hook triggered: {event}")
    
    # 返回结果
    result = {
        "status": "ok",
        "message": "处理完成"
    }
    print(json.dumps(result))

if __name__ == "__main__":
    main()
```

## 注意事项

- Hooks 是**确定性**的（一定执行），而指令文件是**建议性**的
- 如果 Hook 返回错误，可能会阻断后续操作
- 适合放 linter、formatter、安全检查等自动化逻辑
