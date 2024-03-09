# AWS Lambda - Parallel Processing

This repo demonstrates how to achieve parallel processing with AWS Lambda, that can eventually save costs.

> Note : We'll be using Ziptastic API to get the metadata for the specific zip codes. 
Repo URL : https://github.com/joshstrange/Ziptastic

> This API is open source, but still, not meant to be used in production environments.

# Architecture Diagram

![ezgif-3-757602d927](https://github.com/vinamrgrover/lambda-parallel/assets/100070155/10457e4a-b171-4508-bbc1-18d014c048a3)


### About the dataset

This dataset ([zip_codes_sample.csv](https://github.com/vinamrgrover/lambda-parallel/blob/master/data/zip_codes_sample.csv)) contains 140 records, i.e., 140 zip codes; 10 for each state.


### Getting Started

### 1. Create an S3 Bucket

I'll be using AWS CLI to create an S3 Bucket named `batch-bucket-zcodes`

```
aws s3 mb <your_bucket_name>
```

### 2. Copy the csv file to S3 Bucket

I'm using a csv file that contains US zip codes, based on what we'll fetch the location's info from the API. You can find the dataset under the `data` directory.

```
aws s3 cp zip_codes_sample.csv s3://<your_bucket_name>/raw/zip_codes_sample.csv
```

This command copies `zip_codes_sample.csv` to our S3 Bucket under `raw` directory



### 3. Creating a Lambda Function

I'll be using a Docker Image to create our Lambda Function. 
This function will be used to get the location info of the corresponding zip code from API.

Our Lambda Function's code is saved as `function.py`

Inside `Dockerfile` you'll need to make two changes:

 - ```ENV SOURCE_S3_URL s3://batch-bucket-zcodes/raw/zip_codes_list.csv```
- ```ENV DEST_S3_URL s3://batch-bucket-zcodes/curated/```

Replace `batch-bucket-zcodes` with your S3 Bucket name

#### 3.1 Building Docker Image

```docker build -t lambda_batch:latest .```

This command will locally build our Lambda Function's Docker Image.

#### 3.2 Creating an ECR Repository

Use the AWS Console to create an ECR Repository.

#### 3.3 Push the Docker Image to ECR Repository

Use the push commands specified in the AWS Console to push your local image to ECR Repository.
#### 3.4 Create a Lambda Function with Image

Use the AWS Console to create the Lambda Function with the recently-pushed image in your ECR Repository.

> Make sure to attach an IAM Execution Role that allows to access the S3 Bucket created in step 1.

> Also, increase the timeout and memory-capacity for your Lambda Function

### 4. Trigger the Lambda Function (in-parallel)

Use the shell script `parallel-lambda-invoke.sh` to trigger multiple instances of our Lambda Function in parallel. Make sure to replace `batch-func` with your Lambda Function's name.

```
./parallel-lambda-invoke.sh
```

This shell script triggers 10 parallel instances of our Lambda Function

After the execution completes, Parquet Files, partitioned by state column, will be created under `curated` directory in your S3 Bucket.

<img width="800" alt="Screenshot 2024-03-09 at 7 59 23 PM" src="https://github.com/vinamrgrover/lambda-parallel/assets/100070155/491a6e65-f7b5-4f33-8df4-d90c4a201480">

