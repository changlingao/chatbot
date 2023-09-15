<h1 align="center">Technical Support Chatbot for Asiga</h1>

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

(optional: 5. Deactivate environment)
```
deactivate
```

6. run the chatbot under root directory
```
python3 frontend/routes.py
```

### Extras
If more packages, libraries, etc are required please update the requirements.txt file by running in the correct directory:
```
pip freeze > requirements.txt
```
