import requests
import tarfile
import os
import csv

def download_and_extract_to_csv(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        # Save tar.gz to temporary file
        with open('temp.tar.gz', 'wb') as f:
            f.write(response.content)

        # Open the tar.gz file
        with tarfile.open('temp.tar.gz', 'r:gz') as tar:
            # Extract the first file
            member = tar.getmembers()[0]
            f = tar.extractfile(member)

            # Read data from file
            data = f.read().decode()

            # Write data to csv
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in data.split('\n'):
                    writer.writerow(row.split())

        # Clean up the temporary file
        os.remove('temp.tar.gz')
    else:
        print(f"Failed to download data from {url}.")

download_and_extract_to_csv("https://www.ncei.noaa.gov/pub/data/ghcn/v4/ghcnm.tavg.latest.qfe.tar.gz", "data_qfe.csv")



