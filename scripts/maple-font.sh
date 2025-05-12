#!/bin/bash

# 作者 LIPiston
# 作用 下载最新版本的 MapleMono 字体

# Define variables
FONT_URL="https://github.com/subframe7536/maple-font/releases/latest/download/MapleMono-NF-CN-unhinted.zip"
DEST_DIR="./maple"
ZIP_FILE="MapleMono-NF-CN-unhinted.zip"

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Download the font zip file
echo "Downloading font from $FONT_URL..."
curl -L -o "$ZIP_FILE" "$FONT_URL"

# Check if the download was successful
if [ $? -ne 0 ]; then
    echo "Failed to download the font. Exiting."
    exit 1
fi

# Unzip the font into the destination directory
echo "Extracting font to $DEST_DIR..."
unzip -o "$ZIP_FILE" -d "$DEST_DIR"

# Check if the extraction was successful
if [ $? -ne 0 ]; then
    echo "Failed to extract the font. Exiting."
    exit 1
fi

# Clean up the zip file
echo "Cleaning up..."
rm -f "$ZIP_FILE"

echo "Font downloaded and extracted successfully to $DEST_DIR."