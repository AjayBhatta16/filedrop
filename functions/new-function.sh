mkdir $1
cd $1
touch lambda_function.py
touch handler.py
touch requirements.txt
touch .gitignore
echo "**/shared_utils" > .gitignore
cp -r ../shared_utils ./shared_utils