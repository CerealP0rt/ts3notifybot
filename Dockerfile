FROM python:alpine

RUN apk add --update --no-cache --no-progress curl \
&& rm -rf /var/cache/apk/*

ENV DUMB_INIT=1.2.0

RUN curl -Lso /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v${DUMB_INIT}/dumb-init_${DUMB_INIT}_amd64 \
 && chmod +x /usr/local/bin/dumb-init

ENTRYPOINT ["dumb-init"]

COPY ./ /usr/src/
WORKDIR /usr/src/
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "run.py", "-h"]
