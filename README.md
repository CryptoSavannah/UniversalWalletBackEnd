# Back End of the Binusu Loyalty Program.

## Setup steps

Clone the repository

```
git clone git@github.com:CryptoSavannah/UniversalWalletBackEnd.git
```

```
cd UniversalWalletBackEnd
```

Then install the application

```
pyenv shell 3.7.16
```

```
python3 -m venv env
```

```
source env/bin/activate
```

```
pip install -r requirements.txt
```

```
pip install django
```

```
brew update && brew install postgresql
```

```
psql -U postgres -h localhost
```

```
python3 manage.py migrate
```

```
python3 manage.py runserver
```

Run the application

```
python3 manage.py runserver
```