read -r ver < VERSION 
git tag v$ver && git push origin v$ver