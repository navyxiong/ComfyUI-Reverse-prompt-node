import os
import json
import hashlib

class ReversePromptNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        # 获取当前脚本所在目录
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        presets_dir = os.path.join(curr_dir, "presets")
        
        # 自动创建目录
        if not os.path.exists(presets_dir):
            try:
                os.makedirs(presets_dir)
            except:
                pass
            
        # 扫描 .json 文件
        files = []
        if os.path.exists(presets_dir):
            files = [f for f in os.listdir(presets_dir) if f.endswith(".json")]
        
        # 防止列表为空导致的前端错误
        if not files:
            files = ["No_json_files_found"]

        return {
            "required": {
                "preset_file": (sorted(files), ),
                "stringify_mode": (["Pretty (Indented)", "Minified (One Line)"], {"default": "Pretty (Indented)"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_string",)
    FUNCTION = "load_json_preset"
    CATEGORY = "ChiefAI/Utils"

    # 核心修复：添加 IS_CHANGED 逻辑
    # 这告诉 ComfyUI：如果不返回 NaN，则每次运行都检查文件内容是否有变化
    # 这里我们返回文件的修改时间或哈希，确保修改 json 内容后能生效
    @classmethod
    def IS_CHANGED(s, preset_file, stringify_mode):
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(curr_dir, "presets", preset_file)
        if os.path.exists(file_path):
            mtime = os.path.getmtime(file_path)
            return f"{preset_file}_{mtime}_{stringify_mode}"
        return float("NaN")

    def load_json_preset(self, preset_file, stringify_mode):
        if preset_file == "No_json_files_found":
            return (json.dumps({"error": "No JSON files found in presets folder"}),)

        curr_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(curr_dir, "presets", preset_file)
        
        json_content = ""
        
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if stringify_mode == "Minified (One Line)":
                json_content = json.dumps(data, ensure_ascii=False)
            else:
                json_content = json.dumps(data, indent=4, ensure_ascii=False)
                
        except Exception as e:
            print(f"[ReversePromptNode] Error loading {preset_file}: {e}")
            # 返回错误信息但保持 JSON 格式，防止工作流崩溃
            json_content = json.dumps({"error_loading_file": str(e)})

        return (json_content,)
