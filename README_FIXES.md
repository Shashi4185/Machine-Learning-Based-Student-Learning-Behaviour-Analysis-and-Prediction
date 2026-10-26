# Project setup and fixes

## Run the application

This project contains a model serialized with scikit-learn 1.0.2. Use **Python 3.10** in a virtual environment so that the model and scikit-learn versions are compatible.

### Windows

1. Install Python 3.10.
2. Open Command Prompt in this project folder.
3. Create and activate an environment:

   ```bat
   py -3.10 -m venv .venv
   .venv\\Scripts\\activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   python app.py
   ```

4. Open http://127.0.0.1:5000 in your browser.

## Signup email configuration

Signup sends an OTP by email. Configure SMTP credentials in the terminal before starting the app. For Gmail, use an app password rather than your normal account password:

```bat
set SMTP_USER=your-email@gmail.com
set SMTP_PASSWORD=your-gmail-app-password
set SMTP_HOST=smtp.gmail.com
set SMTP_PORT=587
python app.py
```

Do not commit SMTP credentials to source control.

## Changes made

- Fixed the prediction route to load the model file that actually exists (`model_wapper.sav`).
- Added numeric input validation, model feature-count validation, and clearer error responses.
- Changed prediction output to a scalar for reliable template comparisons.
- Removed the hard-coded email account/password from the application and made SMTP configuration environment-based.
- Added dependency and setup instructions.

## Compatibility note

The bundled model was saved using scikit-learn 1.0.2. Loading it with newer scikit-learn versions can fail because the internal decision-tree data format changed. If model loading still fails, ensure that the app is running in Python 3.10 with the exact pinned scikit-learn version above.
