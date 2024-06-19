#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()
    logger.info("Downloading artifact")
    local_path = run.use_artifact("sample.csv:latest").file()
    df = pd.read_csv(local_path)

    logger.info("Dropping outliers")
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()

    logger.info("Convert last_review to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info("Saving the output artifact")
    df.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description,
    )
    file_name = "clean_sample.csv"
    artifact.add_file(file_name)
    run.log_artifact(artifact)

    os.remove(file_name)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="name for input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="name for output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="type for output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="description of output",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="minimum price of ride",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="maximum price of ride",
        required=True
    )


    args = parser.parse_args()

    go(args)
