FROM continuumio/miniconda3:23.5.2-0
RUN conda install --channel conda-forge gcg papilo scip soplex zimpl
#jsonschema
ADD . /work
WORKDIR /work
CMD ["python", "problem.py"]