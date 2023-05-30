#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

if __name__ == "__main__":
    for page in ['bus.2B', 'bus.3A', 'bus.3B', 'bus.4B', 'legal.2B', 'legal.3A', 'legal.3B', 'legal.4B']:
        pages = os.path.join('/Users/binhua_jiang/mywork/ocreval', page, 'pages')
        print(pages)
        f = open(pages,'r')
        pages_content = f.readlines()
        f.close()
        for line in pages_content:
            line_split = line.split(' ')
            #print(line_split)
            img_src = os.path.join('/Users/binhua_jiang/mywork/ocreval', page, line_split[1].replace('\n', ''), line_split[0] + '.tif')
            img_dst = os.path.join(os.getcwd(), 'imgs.all', line_split[0] + '.tif')
            correct_src = os.path.join('/Users/binhua_jiang/mywork/ocreval', page, line_split[1].replace('\n', ''), line_split[0] + '.txt')
            correct_dst = os.path.join(os.getcwd(), 'correct.all', line_split[0] + '.txt')
            print(img_src)
            print(correct_src)
            if os.path.exists(img_src) and os.path.exists(correct_src):
                shutil.copyfile(img_src, img_dst)
                shutil.copyfile(correct_src, correct_dst)

    print('done')