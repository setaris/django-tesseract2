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

Where \<\<filename\>\> is the name of the file you would like to upload.

The server will give out a JSON response in the following format:
    
    { 'fileid': 'b048ef9d-55ea-4163-a236-420e47dd24d9' }

You can start getting the pages by executing:

    $ curl -X GET -u username:password http://localhost:8000/pages/?fileid=b048ef9d-55ea-4163-a236-420e47dd24d9 
    
It will return:

    {
      "count": 50, 
      "next": "?page=2", 
      "previous": null, 
      "results": [
        {
          "text": "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", 
          "page": 1
        }, 
        {
          "text": "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", 
          "page": 2
        }, 
        ...
      ], 
      "author": null, 
      "subject": null, 
      "title": null
    }


Since Django-tesseract2 uses Django-Rest-framework. You can also utilize the built-in API explorer by visiting your browser.


## Other authentication mechanism

Django-tesseract2 also support token based authentication. 
To use this feature. You will need to access the admin page and create a token.

Once you have done that. You can do all the above by embedding the token in the HTTP header.

    $ curl -X POST -H "Content-Type:multipart/form-data; Authorization: Token <<randomtoken>>" -F "file=@<<filename>>" http://localhost:8000/document/
    $ curl -X GET -H "Authorization: Token <<randomtoken>>" http://localhost:8000/pages/?fileid=b048ef9d-55ea-4163-a236-420e47dd24d9 

Of course it is best to use this approach via a HTTPS instead of HTTP.
