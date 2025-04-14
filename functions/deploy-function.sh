# example usage: ./deploy-function.sh function-directory lambda-name

# run update script
./update-function.sh $1

# checkout function code
cd $1

# install dependencies in function directory
pip install -r requirements.txt -t .

# zip function code + dependencies
zip -r lambda.zip .

# deploy to the specified aws resource
aws lambda update-function-code \
    --function-name $2 \
    --zip-file fileb://$(pwd)/lambda.zip \
    --region us-east-2