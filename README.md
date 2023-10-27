<h1 align="center">Technical Support Chatbot for Asiga</h1>

## Setting up Environment Variables
> ⚠️ **The API key must  be set in order for the code to run**

Source: https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety


## Virtual Environments

1. Install virtualenv
 ```
 pip install virtualenv
 ```

2. Change directory then create virtual environment
```
cd <location>
python<version> -m venv <virtual-environment-name>

# for example: python3 -m venv venv

# python<version> -m venv <virtual-environment-name>: This creates a folder called <virtual-environment-name>(venv for my case) in the directory you're in
```

3. Activate environment
```
source <virtual-environment-name>/bin/activate

# for example: source venv/bin/activate
```

4. Install packages
```
python -m pip install -r requirements.txt
```

5. Deactivate environment (optional)
```
deactivate
```

6. run the chatbot under root directory
```
python3 frontend/routes.py
```

6. run the dashboard under root directory
```
python3 dashboard-frontend/routes.py
```

### Extras
If more packages, libraries, etc are required please update the requirements.txt file by running in the correct directory:
```
pip freeze > requirements.txt
```
