(
    cd ./frontend
    pnpm install
    pnpm run build --mode development
)

rm -rf ./backend/dist

cp -r ./frontend/dist ./backend/dist

cd ./backend


pip install -r requirements.txt
python -m fastapi dev main.py