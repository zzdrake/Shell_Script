#!/bin/bash

# 原文件夹路径
source_folder="/path/to/source_folder"
# 目标文件夹路径
destination_base_folder="/path/to/destination_base_folder"

# 确保目标文件夹存在
if [ ! -d "$destination_base_folder" ]; then
    mkdir -p "$destination_base_folder"
fi

# 遍历源文件夹中的所有文件
for json_filepath in "$source_folder"/*.json; do
    # 检查文件是否存在
    if [ ! -e "$json_filepath" ]; then
        continue
    fi
    
    filename=$(basename "$json_filepath")
    jpg_filename="${filename%.json}.jpg"
    jpg_filepath="$source_folder/$jpg_filename"

    # 读取json文件内容
    label=$(jq -r '.label' "$json_filepath")

    if [ "$label" != "null" ]; then
        # 创建目标文件夹
        destination_folder="$destination_base_folder/$label"
        if [ ! -d "$destination_folder" ]; then
            mkdir -p "$destination_folder"
        fi

        # 移动json文件
        mv "$json_filepath" "$destination_folder/$filename"

        # 移动同名jpg文件
        if [ -e "$jpg_filepath" ]; then
            mv "$jpg_filepath" "$destination_folder/$jpg_filename"
        fi
    fi
done

echo "文件整理完成。"
