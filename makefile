.PHONY: install all test clean

install:
	python3 -m pip install -r requirements.txt

test:
	python3 -m pytest\
                  --cov-config=.coveragerc\
                  --cov-report xml:coverage.xml\
                  --cov=./ test/

clean:
    rm coverage.xml

run:
	python3 ptt_crawler/main.py --board=aaa --index=123 --out=bbb
	
