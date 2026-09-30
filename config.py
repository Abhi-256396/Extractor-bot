import os

# config.py - सुरक्षित कॉन्फ़िगरेशन फ़ाइल

# टोकन को सीधे कोड में लिखने के बजाय हम इसे सर्वर (Render) के Environment Variables से उठाएंगे
# जब हम Render पर होस्ट करेंगे, तब वहां सीक्रेट सेटिंग्स में यह टोकन डाल देंगे
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")

# अपनी एडमिन आईडी को भी आप सुरक्षित रूप से सर्वर सेटिंग्स से ले सकते हैं
ADMIN_ID = int(os.environ.get("ADMIN_ID", 123456789))
