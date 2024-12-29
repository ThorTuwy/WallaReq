(
    cd ./frontend
    pnpm install
    pnpm run build
)

rm -rf ./backend/dist

cp -r ./frontend/dist ./backend/dist

cd ./backend


pip install -r requirements.txt
python -m fastapi run main.py