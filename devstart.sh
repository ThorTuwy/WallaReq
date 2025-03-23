(
    cd ./backend
    pip install -r requirements.txt
)

(
    cd ./frontend
    pnpm install
)

(
    cd ./auto-code-generator
    python3 main.py
)

(
    cd ./frontend
    pnpm run build --mode development
)

rm -rf ./backend/dist

cp -r ./frontend/dist ./backend/dist

cd ./backend

python3 -m fastapi dev main.py