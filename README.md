## License
This repository is published only for hackathon evaluation purposes.  
Currently, **All Rights Reserved** by the authors.

このリポジトリはハッカソン審査用に一時公開しています。  
**All Rights Reserved（再利用不可）**。審査終了後に非公開化またはアーカイブ化します。

## 0. 前提

- OS: macOS / Linux / Windows（WSLを推奨）
- 必須ツール:  
  - **Git**, **Docker**, **Docker Compose**（Docker Desktopに同梱）  
  - **Python 3.11+**（`pyenv` / `pyenv-win` 推奨）
  - **MinIO Client (mc)**

---

## 1. Python 環境

### 1-1. Python のインストール（推奨：pyenv）
- macOS / Linux
  ```bash
  # pyenv を導入している前提（未導入なら各公式手順でセットアップ）
  pyenv install 3.11.13
  pyenv local 3.11.13
  python -V
  ```
- Windows（PowerShell / cmd）
  - `pyenv-win` を導入後:
  ```powershell
  pyenv install 3.11.13
  pyenv local 3.11.13
  python --version
  ```

### 1-2. 仮想環境と依存関係
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
# .\\.venv\\Scripts\\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt
```

---

## 2. 環境変数（例）

ルートに `.env`（または `backend/.env` 等）を配置。以下は例です。(.envの設定はデフォルトでは読み込まれません。ポートなどの設定が不要であれば、.envは作成しないでください）

```dotenv
# --- Database (PostgreSQL + PostGIS)
DB_HOST=postgis
DB_PORT=5432
DB_NAME=app
DB_USER=app
DB_PASSWORD=app

# --- MinIO
MINIO_ENDPOINT=http://minio:9000
MINIO_PUBLIC_ENDPOINT=http://localhost:9000         # ブラウザから参照する公開URL
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_BUCKET=images                                  # 画像格納用バケット名

# --- App
APP_DEBUG=true
APP_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## 3. Docker で起動

### 3-1. 初回ビルド & 起動
```bash
docker compose up --build -d
```

### 3-2. 動作確認
```bash
docker compose ps
docker compose logs -f
```

- 代表的なサービス（例）
  - `postgis` … PostgreSQL + PostGIS (pgadmin4: http://localhost:8080)
  - `minio` … MinIO Server（Webコンソール: http://localhost:9001）
  - `backend` … FastAPI（例: http://localhost:8000）
  - `frontend` … React (例: http://localhost:3000)

---

## 4. MinIO 設定（匿名ユーザーにダウンロードのみ許可）

### 4-1. mc（MinIO Client）のインストール
- macOS（Homebrew）
  ```bash
  brew install minio/stable/mc
  ```
- Linux（バイナリ）
  ```bash
  curl -LO https://dl.min.io/client/mc/release/linux-amd64/mc
  chmod +x mc && sudo mv mc /usr/local/bin/
  ```
- Windows（Chocolatey）
  ```powershell
  choco install minio-client
  ```

### 4-2. MinIO への接続エイリアス登録
```bash
mc alias set localminio http://localhost:9000 minioadmin minioadmin
mc admin info localminio
```

### 4-3. 画像バケットの作成（未作成なら）
```bash
mc mb local/trees
```

### 4-4. 匿名ダウンロード権限を付与
```bash
mc anonymous set download local/trees --recursive
```

- 確認：
  ```bash
  mc anonymous get local/trees
  ```
  または、ブラウザで `http://localhost:9001/trees/<object_key>` にアクセスし、画像が表示されるか確認。

### 4-5. 既存オブジェクトの Content-Type を正す（任意）
```bash
mc cp --attr "Content-Type=image/jpeg" \
  localminio/images/path/to/whole.jpeg \
  localminio/images/path/to/whole.jpeg
```

### 4-6. （必要な場合のみ）CORS
```bash
mc admin config set localminio api cors_allow_origin="http://localhost:3000"
mc admin service restart local
```

---

## 5. データベース初期化（任意）

```bash
docker exec -i postgis psql -U app -d app < ./sql/001_init.sql
docker exec -i postgis psql -U app -d app < ./sql/001_testdata.sql
```

---

## 6. バックエンド/フロントエンドの起動（例）

- FastAPI:
  ```bash
  python main.py
  ```

- React:
  ```bash
  npm install
  npm start
  ```

---

## 7. トラブルシューティング

- **MinIO にアクセスできない**  
  - `docker compose ps` で `minio` が起動しているか確認  
- **匿名ダウンロードできない**  
  - `mc anonymous get local/trees` で有効か確認  
- **CORS エラー**  
  - 4-6 の CORS 設定を追加  
- **Content-Type が不正**  
  - 4-5 の手順で付け直し

---

## License

This repository is provided for hackathon evaluation purposes only.  
**All Rights Reserved** by the authors.
""" 
