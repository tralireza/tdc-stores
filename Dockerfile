FROM python:3-alpine

RUN apk add --no-cache bash curl zip
RUN pip install --no-cache-dir Flask pytest

EXPOSE 5000
HEALTHCHECK --interval=1m --timeout=3s --retries=1 \
    CMD curl -f http://127.0.0.5000/status || exit 1

WORKDIR /opt/tdc

RUN mkdir -p /opt/tdc/api
RUN mkdir /opt/tdc/lib
RUN mkdir /opt/tdc/cli
RUN mkdir /opt/tdc/tests
RUN mkdir /opt/tdc/output

ENTRYPOINT ["docker-entrypoint.sh"]
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod 755 /usr/local/bin/docker-entrypoint.sh

COPY lib/*.py /opt/tdc/lib/
COPY api/*.py /opt/tdc/api/
COPY cli/*.py /opt/tdc/cli/
COPY tests /opt/tdc/tests

COPY pytest.ini .
COPY stores.json .
COPY stores-subset.json .
