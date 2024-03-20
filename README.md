
To be able to use this project localy you have to:

* make .env file by copying the .env.example and renaming it
* fill these fields:
    * SECRET_KEY
    * DATABASE_USER
    * DATABASE_PASSWORD
    * DATABASE_NAME

Be aware of these things:

* change field name of a field that has translation values will let these values don't belong to him and will not be returned in the response of this field and you can solve this issue by change the field_name of the needed data in the translation table

