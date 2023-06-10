#!/bin/bash


# Activate the virtual environment
source venv/bin/activate

# Navigate to the historicTemperaturesLambda folder
cd historicTemperaturesLambda

# (Optional) Install any required packages inside the virtual environment using pip
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate

# Navigate to the parent folder
cd ../

# Remove unnecessary files (__pycache__, *.pyc) to reduce package size
find historicTemperaturesLambda -type d -name "__pycache__" -exec rm -rf {} +
find historicTemperaturesLambda -type f -name "*.pyc" -delete

# Navigate to the site-packages directory
cd venv/lib/python3.9/site-packages

# Create the historicTemperaturesLambda_dep_pack.zip file containing the packages in the lambdas directory
zip -r9 ../../../../historicTemperaturesLambda_dep_pack.zip .

# Move back to the lambdas folder
cd ../../../../

cd historicTemperaturesLambda

# Add the Lambda function file and additional files to the deployment_package.zip
zip -g ../historicTemperaturesLambda_dep_pack.zip lambda_function.py logger_config.py db_conn.py helpers.py OpenAI.py


# # Move the deployment package to the parent folder
# mv historicTemperaturesLambda_dep_pack.zip ../

echo "Deployment package created successfully."

# To execute the file: ./create_deployment_package.sh
