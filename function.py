import requests
import pandas as pd
from tqdm import tqdm
import os

MAX_BATCH_SIZE = 100
URL = "http://ZiptasticAPI.com/{}"  # API URL


def get_info(zip_codes: pd.Series, val_range: tuple):
    """
    Fetches locations of zip codes from the API.
    """

    metazip = []
    zip_codes = zip_codes.iloc[val_range[0] : val_range[1]]

    for zip_code in tqdm(zip_codes.zip_code):
        try:
            response = requests.get(URL.format(zip_code))
        except Exception as e:
            continue

        d = response.json()
        d.update({"zip_code": zip_code})
        metazip.append(d)

    return pd.DataFrame(metazip)


def lambda_handler(event=None, context=None):
    """
    Lambda Function's entrypoint.
    """

    low = event["low"]
    high = event["high"]

    SOURCE_S3_URL = os.getenv("SOURCE_S3_URL")
    DEST_S3_URL = os.getenv("DEST_S3_URL")

    # Checking if the range values doesn't exceed batch size
    assert (
        high - low <= MAX_BATCH_SIZE
    ), f"Difference between range values should not be more than {MAX_BATCH_SIZE}"

    zip_codes = pd.read_csv(SOURCE_S3_URL)
    df = get_info(zip_codes, (int(low), int(high)))

    df.to_parquet(
        DEST_S3_URL, partition_cols=["state"], compression="gzip", index=False
    )
