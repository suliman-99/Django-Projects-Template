
## Getting Started

Make sure you have installed all of the following prerequisites on your development machine:

* Git. OSX and Linux machines typically have this already installed.

* Python.

* Pipenv module:

    after you install python you will have pip installed on your machin automatically
    you can check it by
    ```
    pip --version
    ```
    then to install pipenv module by pip just write this command on your cmd
    ```
    pip install pipenv
    ```

* Python Packages:
     then to install all needed packages by pipenv
    ```
    pipenv install
    ```

Environment variables:

* make `.env` file by copying the `.env.example` and renaming it to `.env`
* fill these fields:
    * SECRET_KEY
    * DATABASE_USER
    * DATABASE_PASSWORD
    * DATABASE_NAME

Be aware of these things:

* change field name of a field that has translation values will let these values don't belong to him and will not be returned in the response of this field and you can solve this issue by change the field_name of the needed data in the translation table

