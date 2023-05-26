# ocreval_tools

1. 建立Python运行环境
```
$ virtualenv -p python3 python3_env
$ source ./python3_env/bin/activate
$ pip install -r requirements.txt
```

2. 下载 tessdata
```
$ git clone git@github.com:tesseract-ocr/tessdata.git ./tessdata
```

3. 运行脚本，评测`tesseract`（--oem 0, 传统算法）的识别正确率
```
$ python tesseract_eval.py --dataset-name=bus.3A
```

4. 运行脚本，评测`PaddleOCR`的识别正确率
```
$ python paddleocr_eval.py --dataset-name=bus.3A
```

