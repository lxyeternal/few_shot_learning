# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# @File     : test.py
# @Project  : SCC_Intelligence
# Time      : 22/4/24 1:41 pm
# Author    : honywen
# version   : python 3.8
# Description：
"""

import os
import gzip
import shutil


def decompress_gz_files(directory):
    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.gz'):
            gz_path = os.path.join(directory, filename)
            # 解压文件路径，去掉.gz后缀
            output_path = os.path.join(directory, filename[:-3])

            # 打开.gz文件，并解压到目标文件
            with gzip.open(gz_path, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            print(f'File {filename} decompressed to {output_path}')


# # 使用函数，传入你的目录路径
# decompress_gz_files('/Users/blue/Downloads/RawData')


import os
import json


def process_json_files(input_directory, output_directory):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(input_directory, filename)
            output_file_base = os.path.splitext(filename)[0]

            # Initialize counters and output file index
            count_1 = count_minus1 = 0
            output_index = 1

            # Open input file
            with open(file_path, 'r') as f:
                # Initialize output file
                output_file_path = os.path.join(output_directory, f"{output_file_base}.{output_index}t")
                output_file = open(output_file_path, 'w')

                for line in f:
                    try:
                        data = json.loads(line)
                        overall = data['overall']

                        # Check if 'reviewText' exists in the data
                        if 'reviewText' in data:
                            review_text = data['reviewText'].replace('\n', ' ').replace('\t', ' ').replace('\r',
                                                                                                           ' ').strip()
                        else:
                            continue  # Skip this entry if 'reviewText' is missing

                        # Determine the label based on 'overall' score
                        if overall == 5.0 or overall == 4.0:
                            label = 1
                            count_1 += 1
                        elif overall == 1.0 or overall == 2.0:
                            label = -1
                            count_minus1 += 1
                        else:
                            continue  # Skip if the score is not targeted

                        # Write data to file
                        if (count_1 <= 500 and label == 1) or (count_minus1 <= 500 and label == -1):
                            output_file.write(f"{review_text}\t{label}\n")

                        # Check if new file is needed and limit to 10 files
                        if count_1 > 500 and count_minus1 > 500:
                            if output_index >= 10:
                                break  # Stop if 10 files have been created
                            output_file.close()
                            count_1 = count_minus1 = 0
                            output_index += 1
                            output_file_path = os.path.join(output_directory, f"{output_file_base}.{output_index}t")
                            output_file = open(output_file_path, 'w')

                    except json.JSONDecodeError:
                        print(f"Error decoding JSON from file {filename}, line: {line}")

                # Close the last opened output file
                output_file.close()


# Call the function to process specified directories
process_json_files('/Users/blue/Downloads/RawData', '/Users/blue/Downloads/data')