curl -X POST https://api.fish.audio/v1/tts \
  -H "Authorization: Bearer $FISH_API_KEY" \
  -H "Content-Type: application/json" \
  -H "model: s2-pro" \
  -d '{
    "text":"Hello from Fish Audio!",
    "format":"mp3"
  }' \
  --output hello.mp3
