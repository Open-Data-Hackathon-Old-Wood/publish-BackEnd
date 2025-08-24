# PostGIS (kartoza) on Docker — Setup Guide

Apple Silicon (M1/M2/M3) 対応の **kartoza/postgis:15-3.4** を使った開発用 PostGIS 環境です。  
`docker compose up -d` で初回起動～PostGIS有効化まで自動化されています。

## 0. 前提

- Mac に Docker Desktop が導入済み
- このフォルダ構成で運用します：

```
your-backend-repo/
└─ infra/
   └─ postgis/
      ├─ docker-compose.yml
      ├─ .env.example
      ├─ .env                 # ← 自分で作成（Git無視推奨）
      └─ initdb/
         └─ 01_enable_postgis.sql
```

## 1. 使い方（最短手順）

```bash
cd your-backend-repo/infra/postgis

# 1) .env を用意
cp .env.example .env
# 必要なら .env を編集（DB名/ユーザー/パスワード/ポートなど）

# 2) 初期化SQL（PostGIS拡張）を確認
#   initdb/01_enable_postgis.sql がこの内容になっていること：
#   CREATE EXTENSION IF NOT EXISTS postgis;
#   CREATE EXTENSION IF NOT EXISTS postgis_topology;

# 3) 起動（初回は自動でイメージpull）
docker compose up -d

# 4) ヘルスチェック（healthy になればOK）
docker compose ps
```

## 2. 接続テスト

### コンテナ外（Mac側）から
```bash
# .env の値に合わせて置き換え可
PGPASSWORD=gispass psql -h localhost -p 5432 -U gisuser -d gisdb -c "SELECT PostGIS_Version();"
```

### コンテナ内から
```bash
docker exec -it postgis psql -U gisuser -d gisdb -c "SELECT PostGIS_Version();"
```

成功例：
```
           postgis_version
---------------------------------------
 3.4 USE_GEOS=1 USE_PROJ=1 USE_STATS=1
(1 row)
```

## 3. 接続情報（アプリ / QGIS / pgAdmin）

- Host: `localhost`
- Port: `${PG_PORT}`（デフォルト: `5432`）
- Database: `${POSTGRES_DB}`（例: `gisdb`）
- User: `${POSTGRES_USER}`（例: `gisuser`）
- Password: `${POSTGRES_PASSWORD}`（例: `gispass`）

> pgAdmin を有効化している場合は `http://localhost:${PGADMIN_PORT}`（例: `5050`）  
> 接続先ホストは `postgis`、ポート `5432` を指定。

## 4. 環境変数（`.env`）

`.env.example` をコピーして `.env` を作成し、必要に応じて編集します。

```env
# == PostgreSQL / PostGIS ==
POSTGRES_DB=gisdb
POSTGRES_USER=gisuser
POSTGRES_PASSWORD=gispass
PG_PORT=5432

# == pgAdmin (任意) ==
PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=adminpass
PGADMIN_PORT=5050
```

> **セキュリティ**: `.env` は Git 追跡対象外にしてください（`.gitignore` 推奨）。

## 5. `docker-compose.yml`（参照）

この README と一緒に配置されている `docker-compose.yml` の主なポイント：

- イメージ：`kartoza/postgis:15-3.4`（ARM64対応）
- 永続化ボリューム：`pgdata`
- 初回起動スクリプト：`./initdb` を `docker-entrypoint-initdb.d` にマウント
- ヘルスチェック：`pg_isready`
- （任意）`dpage/pgadmin4` を同時起動可能

## 6. よく使うコマンド

```bash
# 起動 / 停止 / 再起動 / ログ
docker compose up -d
docker compose down
docker compose restart
docker compose logs -f postgis

# 状態確認
docker compose ps

# DBに入る
docker exec -it postgis psql -U gisuser -d gisdb
```

## 7. 初期化をやり直したい（DBを空から作り直す）

> 注意：**データは消えます**（ボリューム削除）。

```bash
docker compose down -v
docker compose up -d
```

`initdb/*.sql` は **最初の起動時のみ** 自動実行されます。  
再実行したい場合は上記の「ボリューム削除 → 再起動」を行ってください。

## 8. バックアップ & リストア

```bash
# Backup（ローカルに backup.sql を作成）
docker exec -t postgis   pg_dump -U "${POSTGRES_USER:-gisuser}" "${POSTGRES_DB:-gisdb}" > backup.sql

# Restore（backup.sql を流し込む）
cat backup.sql | docker exec -i postgis   psql -U "${POSTGRES_USER:-gisuser}" -d "${POSTGRES_DB:-gisdb}"
```

## 9. トラブルシュート

- `no matching manifest for linux/arm64/v8`  
  → 本構成は ARM64 対応の `kartoza/postgis:15-3.4` を使用しているため発生しません。タグを誤って変更していないか確認してください。
- `psql: FATAL: password authentication failed`  
  → `.env` の `POSTGRES_PASSWORD` と接続時のパスワードが一致しているか確認。
- `health: starting` のまま  
  → `docker compose logs -f postgis` で起動ログを確認。ポート競合や初期化SQLのエラーがないかチェック。

---

## 付録：アプリ（例：SQLAlchemy）からの接続文字列

```
postgresql+psycopg2://gisuser:gispass@localhost:5432/gisdb
```

`.env` を読み込むようにしておくと、環境ごとの差し替えが楽です。