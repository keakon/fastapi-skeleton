FROM app

RUN apt-get update && apt-get install -y --no-install-recommends default-mysql-client
COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt

COPY test.sh .
COPY db db
COPY create_admin.py .
COPY tests tests

CMD ["bash", "-c", "/test.sh"]
