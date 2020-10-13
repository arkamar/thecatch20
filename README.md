# The Catch 2020

https://www.thecatch.cz/

- [`FLAG{a5AG-IVeK-jYvv-Brvq}` Intro](#intro)
- [`FLAG{Tyqz-EgrI-8G7E-6PKB}` Malicious e-mails](#malicious-e-mails)

## Intro

> Hi, junior investigator!
>
> Recently, severe danger for whole humanity has emerged again in form of aggressive virus malware, which decimates the Internet population. Many computers were infected a nearly all of them were encrypted by ransomware called `RANSOMVID-20`. Some governments have already announced digital quarantine for most affected companies and its employees are not allowed to use computers, smartphones, etc.
>
> We need your help to solve this issue, otherwise we will have to return to the steam age technologies. Enter the code `FLAG{a5AG-IVeK-jYvv-Brvq}` to get the access to the Training Ground.
>
> Good luck!

## Malicious e-mails

> Hi, junior investigator!
>
> We have extracted a bunch of suspicious e-mails. We believe that you can analyze them and find their secret.
>
> Use password `MaIlZZzz-20` to [download the evidence](malicious_emails/malicious_emails.zip)
>
> Good Luck!

There is bunch of emails in the archive. I extracted them with `ripmime`

```sh
ls *.eml | xargs -n1 ripmime -i
```

every email contains http address and one of them contains the final flag.

```sh
cat textfile* | grep -o 'http://[^ ]*' | xargs curl 2>/dev/null
```
