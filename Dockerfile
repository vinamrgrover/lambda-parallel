FROM public.ecr.aws/lambda/python:3.12-arm64

ENV SOURCE_S3_URL s3://batch-bucket-zcodes/raw/zip_codes_list.csv
ENV DEST_S3_URL s3://batch-bucket-zcodes/curated/

COPY requirements.txt ${LAMBDA_TASK_ROOT}
COPY function.py ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

CMD [ "function.lambda_handler" ]
