Deploy
========

1. Launch EC2 instance on AWS. Make sure to modify the default security to that
the server accepts inbound HTTP and HTTPS.
2. Create a secure sertificate in `/home/ubuntu/`
(https://www.digitalocean.com/community/articles/how-to-create-a-ssl-certificate-on-apache-on-arch-linux for directions)
3. Create the file `settings/my_production.py` and add the line
`from production import *`. Also override `ALLOWED_HOSTS`.
4. Run setup: `fab setup -i /path/to/file.pem -H aws.domain.name`
5. Do a `manage.py collectstatic`
