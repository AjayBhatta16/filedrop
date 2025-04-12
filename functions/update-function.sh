# checkout function folder
cd $1

# clear old package files
rm -rf ./shared-utils
rm -rf ./shared_utils

# rebuild gitignore
rm -f .gitignore
echo "**/shared_utils" > .gitignore

# reinstall shared package
cp -r ../shared_utils ./shared_utils
cat ./shared_utils/requirements.txt >> ./requirements.txt