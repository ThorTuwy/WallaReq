FROM python:3.13.1-slim AS prebuild

WORKDIR /app

COPY ./frontend ./frontend
COPY ./backend ./backend
COPY ./auto-code-generator ./auto-code-generator

WORKDIR /app/auto-code-generator

RUN pip install --no-cache-dir -r requirements.txt
RUN python main.py

FROM node:slim AS build-frontend

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

WORKDIR /app/frontend

COPY --from=prebuild app/frontend/ ./ 

RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
RUN pnpm run build

FROM python:3.13.1-slim AS backend

WORKDIR /app

COPY --from=prebuild app/backend/ ./

RUN pip install --no-cache-dir -r requirements.txt

COPY --from=build-frontend /app/frontend/dist ./dist

EXPOSE 8000

CMD ["python","-m","fastapi","run","main.py"]