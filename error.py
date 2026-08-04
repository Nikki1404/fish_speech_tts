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

cmd.exe /c start "" "$(cygpath -w "$PWD/hello.mp3")"
