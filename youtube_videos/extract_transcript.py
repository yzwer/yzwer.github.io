#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys

def extract_transcript():
    json_path = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\DqDUrNyLxZM.json'
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 提取所有segments中的text字段
        segments = data.get('segments', [])
        if not segments:
            print('未找到segments字段')
            sys.exit(1)
        
        # 拼接完整转录文本
        full_text = ' '.join([seg.get('text', '') for seg in segments])
        
        print(f'共提取 {len(segments)} 个segments')
        print(f'转录文本长度: {len(full_text)} 字符')
        print('='*50)
        print(full_text)
        print('='*50)
        
        # 保存到文件
        output_path = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\DqDUrNyLxZM_transcript.txt'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        print(f'\n转录文本已保存到: {output_path}')
        
        return full_text
        
    except Exception as e:
        print(f'错误: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    extract_transcript()
