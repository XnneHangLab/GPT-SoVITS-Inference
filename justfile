server:
    uv run uvicorn src.gsv.server:app --reload --host localhost --port 12393
test:
	curl -X POST "http://127.0.0.1:12393/tts/gptsovits" \
	-H "Content-Type: application/json" \
	-d '{ \
		"text": "筆者はすでにエッセイの序論、本文、結論を紹介する記事を書いたが、この記事では英文エッセイの書き方の全体的な考え方をおさらいする。", \
		"character": "elaina", \
		"text_language": "ja", \
		"ref_audio_path": "/home/xnne/code/Chatter/GPT-SoVITS-Inference/models/gptsovits/elaina/elaina.wav" \
	}' --output output.wav