find .|grep ".ipynb_checkpoints|__pycache__"|xargs rm -rf
git pull
git add .
git commit -m 'update'
git push
