from .reverse_prompt_node import ReversePromptNode

# 节点类映射 (必须与 class 名一致)
NODE_CLASS_MAPPINGS = {
    "Reverse_prompt_node": ReversePromptNode
}

# 节点显示名称映射 (菜单里显示的名字)
NODE_DISPLAY_NAME_MAPPINGS = {
    "Reverse_prompt_node": "Reverse Prompt Loader (JSON)"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
