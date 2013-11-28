django-tesseract2
=================

OCR rest service using tesseract.

## Requirements:

* Django
* Pillow 
* PyPDF2
* Wand
* Tesserwrap
* Django Rest Framework

## Usage

Clone the repo:

    $ git clone git@github.com:setaris/django-tesseract2.git

Get into the newly cloned repo directory and run:

    $ python manage.py syncdb
    $ python manage.py runserver

If you have created a superuser account on syncdb. You can start using the service.

To try it out. Run this on your terminal:

    $ curl -X POST -H "Content-Type:multipart/form-data;" -u username:password -F "file=@<<filename>>" http://localhost:8000/document/

The server will give out a JSON response in the following format:
    
    { 'fileid': 'b048ef9d-55ea-4163-a236-420e47dd24d9' }

You can start getting the pages by executing:

    $ curl -X GET -u username:password http://localhost:8000/pages/?fileid=b048ef9d-55ea-4163-a236-420e47dd24d9 



## Other authentication mechanism

Django-tesseract2 also support Token based authentication. 
To use this feature. You will need to access the admin page and create token.
Once you have done that. You can do all the above by embedding the token in the HTTP header.

    $ curl -X POST -H "Content-Type:multipart/form-data; Authorization: Token <<randomtoken>>" -F "file=@<<filename>>" http://localhost:8000/document/
    $ curl -X GET -H "Authorization: Token <<randomtoken>>" http://localhost:8000/pages/?fileid=b048ef9d-55ea-4163-a236-420e47dd24d9 
