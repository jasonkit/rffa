FROM python:3.8-buster

RUN \
    wget https://github.com/Yelp/dumb-init/releases/download/v1.2.1/dumb-init_1.2.1_amd64.deb && \
    dpkg -i dumb-init_*.deb && \
    rm dumb-init_*.deb

RUN pip install --upgrade pip && \
    pip install --upgrade setuptools

WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
ENV PYTHONUNBUFFERED 0
ENV OMP_THREAD_LIMIT 1
ENTRYPOINT ["dumb-init"]
CMD ["uvicorn", "--host", "0.0.0.0", "rffa:app"]

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY rffa /app/
