import os
import json
import folder_paths

class ReversePromptNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        # 获取当前脚本所在目录
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        presets_dir = os.path.join(curr_dir, "presets")
        
        # 如果目录不存在，创建一个（防止报错）
        if not os.path.exists(presets_dir):
            os.makedirs(presets_dir)
            
        # 扫描 .json 文件
        files = [f for f in os.listdir(presets_dir) if f.endswith(".json")]
        
        # 如果没有文件，提供一个占位符
        if not files:
            files = ["put_json_in_presets_folder.json"]

        return {
            "required": {
                "preset_file": (sorted(files), ),
                "stringify_mode": (["Pretty (Indented)", "Minified (One Line)"], {"default": "Pretty (Indented)"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_string",)
    FUNCTION = "load_json_preset"
    CATEGORY = "ChiefAI/Utils"  # 你可以根据喜好修改类别

    def load_json_preset(self, preset_file, stringify_mode):
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(curr_dir, "presets", preset_file)
        
        json_content = ""
        
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                # 先解析一次以确保它是有效的JSON
                data = json.load(f)
                
            # 根据用户选择输出格式化后的文本
            if stringify_mode == "Minified (One Line)":
                # 压缩成一行，去除空格
                json_content = json.dumps(data, ensure_ascii=False)
            else:
                # 保持缩进的可读格式
                json_content = json.dumps(data, indent=4, ensure_ascii=False)
                
        except Exception as e:
            print(f"[ReversePromptNode] Error: {e}")
            json_content = json.dumps({"error": str(e)})

        return (json_content,)
