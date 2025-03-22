(
    cd ./backend
    pip install -r requirements.txt
)

(
    cd ./auto-code-generator
    python3 dataVerifier.py
)

(
    cd ./frontend
    pnpm install
    pnpm run build
)

rm -rf ./backend/dist

cp -r ./frontend/dist ./backend/dist

cd ./backend

python3 -m fastapi main.py