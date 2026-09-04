curl -X POST https://api.fish.audio/v1/tts \
  -H "Authorization: Bearer $FISH_API_KEY" \
  -H "Content-Type: application/json" \
  -H "model: s2-pro" \
  -d '{
    "text":"Hello from Fish Audio!",
    "format":"mp3"
  }' \
  --output hello.mp3


curl --ssl-no-revoke \
  --fail-with-body \
  --request POST "https://api.fish.audio/v1/tts" \
  --header "Authorization: Bearer $FISH_API_KEY" \
  --header "Content-Type: application/json" \
  --header "model: s2-pro" \
  --data '{
    "text": "Hello from Fish Audio!",
    "format": "mp3"
  }' \
  --dump-header response-headers.txt \
  --output hello.mp3 \
  --write-out "\nHTTP status: %{http_code}\nContent type: %{content_type}\nDownloaded: %{size_download} bytes\n"

curl --ssl-no-revoke \
  -X POST "https://api.fish.audio/v1/tts" \
  -H "Authorization: Bearer $FISH_API_KEY" \
  -H "Content-Type: application/json" \
  -H "model: s2-pro" \
  -d '{
    "text":"Hello from Fish Audio!",
    "format":"mp3"
  }'




Hi ,
I’ve shared the Python tasks with you. Please go through the requirements carefully and try to work on them independently based on your current understanding.
I’m not expecting you to know everything mentioned in the tasks. The idea is for you to explore the requirements, attempt the implementation, and understand where you are comfortable and where you need guidance.
If you get stuck somewhere or are unsure about any concept or requirement, please feel free to reach out to me. Don’t stay blocked for too long.
We can connect around 6:00 PM today to discuss your progress, clarify any doubts, and go through anything you are finding difficult.
