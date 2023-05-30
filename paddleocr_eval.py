#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import time

import shell_execute
from paddleocr import PaddleOCR

if __name__ == "__main__":
    args_parser = argparse.ArgumentParser(description='ocreval tools')
    args_parser.add_argument(
        '--dataset-name',  action='store', dest='dataset_name', default='')
    args_parser.add_argument(
        '--lang',  action='store', dest='lang', default='en')
    args = args_parser.parse_args()
    print(args)

    ocr_engine = 'paddleocr'

    imgs_dir = os.path.join(os.getcwd(), 'imgs.' + args.dataset_name)
    correct_dir = os.path.join(os.getcwd(), 'correct.' + args.dataset_name)
    output_dir = os.path.join(os.getcwd(), ocr_engine + '.output.' + args.dataset_name)
    report_dir = os.path.join(os.getcwd(), ocr_engine + '.report.' + args.dataset_name)

    if os.path.exists(output_dir):
        cmd = 'rm -rf %s/*' % output_dir
        shell_execute.run(cmd, print_to_console=True)
    else:
        os.makedirs(output_dir)
    
    if os.path.exists(report_dir):
        cmd = 'rm -rf %s/*' % report_dir
        shell_execute.run(cmd, print_to_console=True)
    else:
        os.makedirs(report_dir)

    start_time = time.time()

    # lang = 'en'
    # lang = 'ch'
    lang = args.lang

    # need to run only once to download and load model into memory
    ocr = PaddleOCR(use_angle_cls=True, lang=lang)
    # 列出 imgs_dir 目录下扩展名为 .jpg 或 .png 或 .tif 的文件
    imgs = [os.path.join(imgs_dir, f) for f in os.listdir(imgs_dir) if f.endswith(
        '.jpg') or f.endswith('.png') or f.endswith('.tif') or f.endswith('.tiff')]
    # 对每个图片文件进行 OCR 识别，和正确答案比较，生成准确率报告
    accuracy_report_files = []
    wordacc_report_files = []
    for img in imgs:
        # print(img)
        result = ocr.ocr(img, cls=True)
        # print(type(result), len(result))
        # print(json.dumps(result, ensure_ascii=False, indent=4))
        ocr_result = []
        for line in result[0]:
            # print(type(line))
            # print(json.dumps(line, ensure_ascii=False, indent=4))
            line_text = line[1][0]
            if lang == 'ch': 
                #删除字符串 line_text 中的空格字符
                line_text = line_text.replace(' ', '')
            ocr_result.append(line_text + '\n')

        output_file = os.path.join(os.getcwd(), output_dir, os.path.splitext(
            os.path.basename(img))[0] + '.txt')
        # print(output_file)
        if os.path.exists(output_file):
            os.unlink(output_file)
        f = open(output_file, 'w')
        f.writelines(ocr_result)
        f.close()

        correct_file = os.path.join(os.getcwd(), correct_dir, os.path.splitext(
            os.path.basename(img))[0] + '.txt')
        accuracy_report_file = os.path.join(os.getcwd(), report_dir, os.path.splitext(
            os.path.basename(img))[0] + '.accuracy.txt')
        cmd = 'accuracy "%s" "%s" "%s"' % (
            correct_file, output_file, accuracy_report_file)
        if os.path.exists(accuracy_report_file):
            os.unlink(accuracy_report_file)
        shell_execute.run(cmd, print_to_console=True)
        accuracy_report_files.append(accuracy_report_file)

        wordacc_report_file = os.path.join(os.getcwd(), report_dir, os.path.splitext(
            os.path.basename(img))[0] + '.wordacc.txt')
        cmd = 'wordacc "%s" "%s" "%s"' % (
            correct_file, output_file, wordacc_report_file)
        if os.path.exists(wordacc_report_file):
            os.unlink(wordacc_report_file)
        shell_execute.run(cmd, print_to_console=True)
        wordacc_report_files.append(wordacc_report_file)

    end_time = time.time()
    # 合并所有准确率报告
    cmd = 'accsum'
    for report_file in accuracy_report_files:
        cmd += ' "%s"' % report_file
    cmd += ' >' + os.path.join(os.getcwd(), ocr_engine + '.accsum.%s' %
                            args.dataset_name + '.report.txt')
    shell_execute.run(cmd, print_to_console=True)

    
    cmd = 'accci'
    for report_file in accuracy_report_files:
        cmd += ' "%s"' % report_file
    cmd += ' >' + os.path.join(os.getcwd(), ocr_engine + '.accci.%s' %
                            args.dataset_name + '.report.txt')
    shell_execute.run(cmd, print_to_console=True)


    cmd = 'wordaccsum'
    for report_file in wordacc_report_files:
        cmd += ' "%s"' % report_file
    cmd += ' >' + os.path.join(os.getcwd(), ocr_engine + '.wordaccsum.%s' %
                            args.dataset_name + '.report.txt')
    shell_execute.run(cmd, print_to_console=True)

    # 显示报告的前 20 行
    cmd = 'head -n 20 ' + os.path.join(os.getcwd(), ocr_engine + '.accsum.%s' %
                            args.dataset_name + '.report.txt')
    shell_execute.run(cmd, print_to_console=True)
    cmd = 'head -n 20 ' + os.path.join(os.getcwd(), ocr_engine + '.accci.%s' %
                            args.dataset_name + '.report.txt')
    shell_execute.run(cmd, print_to_console=True)
    cmd = 'head -n 20 ' + os.path.join(os.getcwd(), ocr_engine + '.wordaccsum.%s' %
                            args.dataset_name + '.report.txt')
    shell_execute.run(cmd, print_to_console=True)

    # 显示耗时, 单位为毫秒
    print('耗时: %d 毫秒' % ((end_time - start_time) * 1000))
    print('执行成功')
