from .reverse_prompt_node import ReversePromptNode

# 节点类映射
NODE_CLASS_MAPPINGS = {
    "ReversePromptNode": ReversePromptNode
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "ReversePromptNode": "Reverse Prompt Loader (JSON)"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
