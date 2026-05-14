from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def transcript():
    url = request.args.get('url')
    lang = request.args.get('lang', 'uk,ru,en')
    if not url:
        return jsonify({"error": "Missing url"}), 400

    video_id = None
    if 'watch?v=' in url:
        video_id = url.split('watch?v=')[1]
        if '&' in video_id:
            video_id = video_id.split('&')[0]
    if not video_id:
        return jsonify({"error": "Invalid URL"}), 400

    languages = [l.strip() for l in lang.split(',')]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        full_text = ' '.join([item['text'] for item in transcript])
        return jsonify({
            "full_text": full_text,
            "segments": transcript,
            "language": languages[0]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
