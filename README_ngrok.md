# Public Access Setup for Twilio

Your local server needs to be accessible from the public internet for Twilio to reach it. Here are the setup instructions:

## Using ngrok

### Install ngrok

**Windows:**
```bash
# Download from: https://ngrok.com/download
# Extract ngrok.exe
# Add to your PATH or place in project folder
```

**Other platforms:**
```bash
# macOS with Homebrew:
brew install ngrok

# Linux:
# Download from https://ngrok.com/download
```

### Start the server with public access

```bash
python start_server.py
```

This will:
1. Start your Flask server
2. Create a public ngrok tunnel
3. Update all URLs to use the public address
4. Display the public URLs for Twilio


## Usage

1. **Start the server:**
   ```bash
   python start_server.py
   ```

2. **Copy the public URLs** displayed in the console

3. **Update your test.py** to use the public URL:
    ```python
    call = client.calls.create(
        url = 'https://your-ngrok-url.ngrok.io/script1',  # Use the public URL
        to="",
        from_="",
    )
    ```

4. **Test dynamic updates:**
   ```bash
   # Update script content while call is active
   python update_script.py script1 '<?xml version="1.0" encoding="UTF-8"?><Response><Say voice="woman">Dynamic update!</Say><Redirect method="POST">https://judgementally-unlettered-carrie.ngrok-free.dev/script2</Redirect></Response>'
   ```

## Important Notes

- **ngrok URLs change** each time you restart (unless you have a paid account)
- **Free ngrok** has session limits and bandwidth restrictions
- **HTTPS is preferred** for production use
- **Keep the server running** while testing with Twilio

## Troubleshooting

- **"ngrok not found"**: Make sure ngrok is installed and in your PATH
- **"Connection refused"**: Ensure your Flask server is running on port 5000
- **"Tunnel failed"**: Check your internet connection and try again
- **Twilio can't reach URL**: Verify the public URL is accessible from your browser

## Security Note

⚠️ **Warning**: Exposing your local server to the internet makes it publicly accessible. Only use this for development and testing. For production, use proper hosting services.
