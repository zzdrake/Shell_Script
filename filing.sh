#!/bin/bash

# 源目录和目标目录
source_dir="source_directory"
target_dir="target_directory"

# 创建目标目录（如果不存在）
mkdir -p "$target_dir"

# 使用 find 命令递归查找所有的 JSON 文件
find "$source_dir" -type f -name "*.json" | while read -r json_file; do
    # 获取文件名（不包括扩展名）
    filename=$(basename "$json_file" .json)
    
    # 获取 JSON 文件所在的目录
    file_dir=$(dirname "$json_file")
    
    # 对应的 JPG 文件
    jpg_file="$file_dir/$filename.jpg"
    
    # 检查 JPG 文件是否存在
    if [[ -f "$jpg_file" ]]; then
        # 复制 JSON 文件和 JPG 文件到目标目录
        cp "$json_file" "$target_dir"
        cp "$jpg_file" "$target_dir"
        echo "Copied $json_file and $jpg_file to $target_dir"
    else
        echo "JPG file $jpg_file not found for $json_file"
    fi
done

echo "Script execution completed."
