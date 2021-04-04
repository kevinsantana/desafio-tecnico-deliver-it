FROM centos/python-38-centos7

USER root

# DEPENDENCIES
RUN yum install -y \
        postgresql-devel-9.2.24 \
        poppler-utils-0.26.5 \
        zlib-devel-1.2.7

# INSTALL APPLICATION
COPY ./cadastro_contas /deploy/cadastro_contas
COPY ./docs /deploy/docs
COPY setup.py /deploy
COPY README.md /deploy
COPY /tests /deploy/tests

WORKDIR /deploy

RUN pip install -e . && \
    pip install pytest

EXPOSE 5000
CMD ["gunicorn", "--bind=0.0.0.0:5000", "--workers=3", "--worker-class=uvicorn.workers.UvicornWorker", "--timeout=174000", "cadastro_contas:app"]
