find .|grep ".ipynb_checkpoints"|xargs rm -rf
git pull
git add .
git commit -m 'update'
git push
