!#/bin/bash

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/gitbutt
ssh -T git@github.com

git remote -v




