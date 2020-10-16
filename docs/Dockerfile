from python:3.7 as builder

RUN mkdir /app
WORKDIR /app

ADD . /app/
RUN pip install -r docs/requirements.txt
RUN cd docs && make html

from nginx:1.17.9-alpine
COPY --from=builder /app/docs/_build/html /usr/share/nginx/html/sdk/v1
COPY --from=builder /app/docs/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# run sever when container starts
CMD ["nginx", "-g", "daemon off;"]
