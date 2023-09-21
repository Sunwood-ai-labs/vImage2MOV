git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch 'image/Echoes-of-Creation/00029-1365031934.png'" --force HEAD
git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch 'image/Echoes-of-Creation/00030-2356801959.png'" --force HEAD
git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch 'image/Echoes-of-Creation_Blurred/00028-1365031933.png'" --force HEAD
git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch 'image/Echoes-of-Creation_Blurred/00029-1365031934.png'" --force HEAD
git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch 'image/Echoes-of-Creation_Blurred/00030-2356801959.png'" --force HEAD
git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch 'image/Echoes-of-Creation/00028-1365031933.png'" --force HEAD

git merge origin/main --allow-unrelated-histories

git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch 'image/Echoes-of-Creation_Blurred/00028-1365031933.png' 'image/Echoes-of-Creation_Blurred/00029-1365031934.png' 'image/Echoes-of-Creation_Blurred/00030-2356801959.png' 'image/Echoes-of-Creation/00028-1365031933.png'" --force HEAD