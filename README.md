# The Catch 2020

https://www.thecatch.cz/

- [`FLAG{a5AG-IVeK-jYvv-Brvq}` Intro](#intro)
	- [`FLAG{Tyqz-EgrI-8G7E-6PKB}` Malicious e-mails](#malicious-e-mails)
	- [`FLAG{SaXY-u8fc-p1Kv-oXoT}` Spam everywhere](#spam-everywhere)
	- [`FLAG{MXcz-PrQK-FJbJ-jWVA}` Easy Bee](#easy-bee)

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

## Spam everywhere

> Hi, junior investigator!
>
> We get some recorded traffic, we believe you can analyze it and found whether it contains something malicious.
>
> Use password `sPaMMerS-wOrKS` to [download the evidence](spam_everywhere/spam_everywhere.zip)
>
> Good Luck!

The pcap in the archive contains 35 SMTP connections where everyone is used to send exactly one email. Most of them are spam advertising **The Cure from RANSOMVID-20**. The flag is in the image.

![](spam_everywhere/rv20protector.png)

## Easy Bee

> Hi, junior investigator!
>
> We have for you something malicious called "Easy Bee". We believe that you can analyze it and found what is its purpose.
>
> Use password `eAsY-beE-mAlWr-20` to [download the evidence](easy_bee/easy_bee.zip)
>
> Good Luck!

The archive contains binary `easy_botnet_client.exe`. The simplest solution is to dump the network communication and inspect transfered data. The client connects to `78.128.216.92:20200` and sends the message `Easy-Bee-358n9pqh ready for work`. The server replies `Hello, your order is to keep in secret this flag: FLAG{MXcz-PrQK-FJbJ-jWVA}`.
