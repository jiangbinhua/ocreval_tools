prepare_env:
	source python3_env/bin/activate && pip install -r requirements.txt

tesseract_eval:
	python tesseract_eval.py --dataset-name=bus.3A

paddleocr_eval:
    python paddleocr_eval.py --dataset-name=bus.3A

