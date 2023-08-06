# mb-cruise-migration

Migration scripts for migrating multibeam metadata from MB schema to CRUISE schema. 

## Migration Instructions


## Development

### Setup virtual environment

1. setup virtualenv
2. specify python installation for virtualenv to use
3. activate the virtual environment
4. verify python version and virtualenv
5. install required modules
6. verify they were installed with pip list
7. deactivate the virtual environment

```bash
virtualenv migenv

virtualenv --python=</path/to/python> </path/to/new/virtualenv/>

source ./migenv/bin/activate

python which
python -V

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

pip list

deactivate
```


### run tests 

from project root:
```bash
python -m unittest discover tests
```


