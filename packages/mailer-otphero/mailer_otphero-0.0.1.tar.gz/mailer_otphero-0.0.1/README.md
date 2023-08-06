# mailer 

Setup DNS and install:

```bash
pip install mailer-wildfluss
```

and then send email using SMTP which scores 10/10 at mail-tester.com like this

```python 
from mailer_otphero import Mailer

m = Mailer(host='smtp.google.com', port=465,
           user='your@email.com', password='secret')

m.send(subject='Ping?', from_='your@email.com',
       to='other@email.com', content='Hello, world')
```

## How to setup DNS 

Add these records to your DNS to make Spamassassin, Google and others happy:

`_dmarc.YOURDOMAIN` with value like `v=DMARC1; p=none` (or more strict - TODO: link ) 

`mail._domainkey.YOURDOMAIN` with your DKIM value 

`@` TXT record with your SPF value 

Obviously your domain must have `MX` records.

NB: `YOURDOMAIN` is one from which you're trying to send eg `email.com` in the example above.

## Release new version

```
python setup.py sdist && \
twine upload dist/*
```
