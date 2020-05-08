.PHONY: install all test clean

install:
	python3 -m pip install -r requirements.txt

test:
	python3 -m pytest\
                  --cov-config=.coveragerc\
                  --cov-report xml:coverage.xml\
                  --cov=./ test/

clean:
	rm coverage.xml *.out

run:
	python3 ptt_crawler/main.py  --out=article.out --log_conf=conf_log.ini --conf=conf_product.ini
	
