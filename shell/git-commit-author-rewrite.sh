#!/bin/env sh
echo "$0: Please review this files contents before executing!"
exit 1

git filter-branch --env-filter '
OLD_EMAIL="oldemail@example.com"
CORRECT_NAME="Your Correct Name"
CORRECT_EMAIL="newemail@example.com"

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags

git push --force --tags origin 'refs/heads/*'
