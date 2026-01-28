## fastpix-python test project (copy/paste playground)

This folder is a tiny runnable project that installs the SDK from the parent folder (`../`) so you can copy examples and see real output.

### 1) Create a virtualenv + install the SDK

From `fastpix-python/test-project`:

```bash
cd "/Users/sravanimaramreddy/Desktop/Dec-speakeasy/new sdk/fastpix-python/test-project"
chmod +x run.sh
```

### 2) Configure credentials

This SDK uses **Basic Auth** and reads credentials from environment variables:

- `FASTPIX_USERNAME`
- `FASTPIX_PASSWORD`

Create a local `.env` file (not committed):

```bash
cp env.example .env
```

Then edit `.env` and set your values.

Optional:
- `FASTPIX_SERVER_URL` (defaults to `https://api.fastpix.io/v1/`)

### 3) Run examples

List playlists:

```bash
./run.sh get_playlists
```

List signing keys:

```bash
./run.sh get_signing_keys
```

Delete a media by ID (DANGER: irreversible):

```bash
./run.sh delete_mediaId "<media_id>"
```
