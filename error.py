curl -X POST https://api.fish.audio/v1/tts \
  -H "Authorization: Bearer $FISH_API_KEY" \
  -H "Content-Type: application/json" \
  -H "model: s2-pro" \
  -d '{
    "text":"Hello from Fish Audio!",
    "format":"mp3"
  }' \
  --output hello.mp3


re_nikitav@C18L10-DP3144 MINGW64 ~/Desktop
$ curl -X POST https://api.fish.audio/v1/tts \
  -H "Authorization: Bearer $FISH_API_KEY" \
  -H "Content-Type: application/json" \
  -H "model: s2-pro" \
  -d '{
    "text":"Hello from Fish Audio!",
    "format":"mp3"
  }' \
  --output hello.mp3
curl: (35) schannel: next InitializeSecurityContext failed: CRYPT_E_NO_REVOCATION_CHECK (0x80092012) - The revocation function was unable to check revocation for the certificate.
