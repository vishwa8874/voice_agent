# Deepgram + Twilio Voice Agent Setup Guide

## Prerequisites

- Deepgram Account
- Twilio Account
- ngrok Installed
- Python + UV Installed
- VS Code

---

# Step 1: Create a Deepgram Account

1. Create a free Deepgram account.
2. Log in to the dashboard.
3. Generate a new API key.
4. Save the API key securely.

---

# Step 2: Verify Your Mobile Number in Twilio

Navigate to:

```text
Phone Numbers → Manage → Verified Caller IDs
```

Verify your personal mobile number.

![Verified Caller IDs](Screenshot%202026-06-12%20152638(2).png)

---

# Step 3: Create a TwiML Bin

In the Twilio dashboard search bar, search for:

```text
TwiML Bin
```

Then click **Create TwiML Bin**.

![Search TwiML Bin](Screenshot%202026-06-12%20152735.png)

---

# Step 4: Configure the TwiML Bin

Paste the following XML into the TwiML Bin.

Replace the ngrok URL with your own URL.

```xml
<Response>
    <Say language="en">This call may be monitored or recorded.</Say>
    <Connect>
        <Stream url="wss://your-ngrok-url.ngrok-free.dev/twilio" />
    </Connect>
</Response>
```

Example configuration:

![TwiML Bin Configuration](Screenshot%202026-06-12%20152811.png)

After entering the XML, click **Create**.

---

# Step 5: Start ngrok

Open a terminal in VS Code and run:

```bash
ngrok http 5000
```

You will receive a forwarding URL similar to:

```text
https://natural-monstrous-monotone.ngrok-free.dev
```

Convert it to:

```text
wss://natural-monstrous-monotone.ngrok-free.dev/twilio
```

Rules:

- Replace `https://` with `wss://`
- Add `/twilio` at the end
- Keep ngrok running

---

# Step 6: Run the Application

Open a new terminal and run:

```bash
uv run .\main.py
```

Make sure:

- ngrok is running in the first terminal
- main.py is running in the second terminal

---

# Step 7: Verified Caller ID Example

Your verified mobile number should appear under:

```text
Phone Numbers → Manage → Verified Caller IDs
```

Example:

![Verified Number Example](Screenshot%202026-06-12%20153219.png)

---

# Testing

1. Start ngrok.
2. Start the Python application.
3. Call your Twilio phone number.
4. Twilio connects to the WebSocket endpoint.
5. Audio is streamed to your Deepgram voice agent.

---

# Important Notes

- ngrok must remain running.
- If ngrok restarts, update the Stream URL in the TwiML Bin.
- Always use:

```text
wss://<your-ngrok-url>/twilio
```

- Never use `http://` or `https://` in the Stream URL.
- Ensure your Deepgram API key is configured correctly.
