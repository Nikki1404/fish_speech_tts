

curl -X POST https://api.fish.audio/v1/tts \
  -H "Authorization: Bearer $sk-fish-fLbtXLiw_myl9J9KzkifUmaU0n870CFJkCoQjAQyRic" \
  -H "Content-Type: application/json" \
  -H "model: s2-pro" \
  -d '{
    "text":"Hello from Fish Audio!",
    "format":"mp3"
  }' \
  --output hello.mp3
