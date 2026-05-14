import subprocess
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
POT_PROVIDER_URL = "http://pot-provider.railway.internal:4416"

@app.route('/transcript', methods=['GET'])
def transcript():
    url = request.args.get('url')
    lang = request.args.get('lang', 'uk,ru,en')
    if not url:
        return jsonify({"error": "Missing url"}), 400
    cmd = [
        "yt-dlp",
        "--write-auto-sub",
        "--sub-lang", lang,
        "--skip-download",
        "--print", "%(subtitles)s",
        "--extractor-args",
        f"youtube:get_pot=True;pot_provider_base_url={POT_PROVIDER_URL}",
        url
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 500
        # Парсим вывод
        raw = result.stdout.strip()
        try:
            data = json.loads(raw)
            for lang_code in data:
                lines = [seg["text"] for seg in data[lang_code]]
                return jsonify({"language": lang_code, "full_text": " ".join(lines)})
        except Exception:
            return jsonify({"raw": raw})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
