FROM node:22.12.0-slim AS build-frontend

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

WORKDIR /app/frontend

COPY frontend/ ./

RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
RUN pnpm run build

FROM python:3.13.1-slim AS backend

WORKDIR /app

COPY backend/ ./

COPY --from=build-frontend /app/frontend/dist ./dist

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python","-m","fastapi","run","main.py"]