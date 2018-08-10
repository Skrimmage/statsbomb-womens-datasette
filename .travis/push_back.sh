#!/bin/sh

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
}

commit_database() {
  git checkout master
  git add . *.db
  git commit --message "Automated Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git remote add back_home https://${GH_TOKEN}@github.com/skrimmage/statsbomb-womens-datasette.git > /dev/null 2>&1
  git push --quiet --set-upstream back_home master
}

setup_git
commit_database
upload_files
