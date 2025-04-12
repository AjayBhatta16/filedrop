# setup new folder
mkdir $1
cd $1

# create files
touch lambda_function.py
touch handler.py
touch requirements.txt
touch .gitignore

# install shared utils
echo "**/shared_utils" > .gitignore
cp -r ../shared_utils ./shared_utils
cat ./shared_utils/requirements.txt >> ./requirements.txt