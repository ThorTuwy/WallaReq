(
    cd ./frontend
    pnpm install
    pnpm run build
)

rm -rf ./backend/dist

cp -r ./frontend/dist ./backend/dist

cd ./backend


python -m fastapi dev main.py