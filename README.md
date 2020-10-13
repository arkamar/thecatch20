# The Catch 2020

https://www.thecatch.cz/

- [`FLAG{a5AG-IVeK-jYvv-Brvq}` Intro](#intro)
	- [`FLAG{Tyqz-EgrI-8G7E-6PKB}` Malicious e-mails](#malicious-e-mails)
	- [`FLAG{SaXY-u8fc-p1Kv-oXoT}` Spam everywhere](#spam-everywhere)
	- [`FLAG{MXcz-PrQK-FJbJ-jWVA}` Easy Bee](#easy-bee)
	- [`FLAG{YHsB-hr0J-W2ol-fV17}` Wiretaped Message`](#wiretaped-message)
- [`FLAG{Jb91-XGSI-05xR-kqgQ}` Promotion](#promotion)
	- [`FLAG{rUn5-GwMR-IlY6-orZd}` Malware spreading](#malware-spreading)
	- [Attachment analysis](#attachment-analysis)
	- [Downloaded File](#downloaded-file)
	- [The Connection](#the-connection)
	- [Botnet master](#botnet-master)
	- [Ransomware](#ransomware)
- [`FLAG{aKAL-qQhH-MsAz-miUG}` Epilogue](#epilogue)

## Intro

> Hi, junior investigator!
>
> Recently, severe danger for whole humanity has emerged again in form of aggressive virus malware, which decimates the Internet population. Many computers were infected a nearly all of them were encrypted by ransomware called `RANSOMVID-20`. Some governments have already announced digital quarantine for most affected companies and its employees are not allowed to use computers, smartphones, etc.
>
> We need your help to solve this issue, otherwise we will have to return to the steam age technologies. Enter the code `FLAG{a5AG-IVeK-jYvv-Brvq}` to get the access to the Training Ground.
>
> Good luck!

### Malicious e-mails

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

### Spam everywhere

> Hi, junior investigator!
>
> We get some recorded traffic, we believe you can analyze it and found whether it contains something malicious.
>
> Use password `sPaMMerS-wOrKS` to [download the evidence](spam_everywhere/spam_everywhere.zip)
>
> Good Luck!

The pcap in the archive contains 35 SMTP connections where everyone is used to send exactly one email. Most of them are spam advertising **The Cure from RANSOMVID-20**. The flag is in the image.

![](spam_everywhere/rv20protector.png)

### Easy Bee

> Hi, junior investigator!
>
> We have for you something malicious called "Easy Bee". We believe that you can analyze it and found what is its purpose.
>
> Use password `eAsY-beE-mAlWr-20` to [download the evidence](easy_bee/easy_bee.zip)
>
> Good Luck!

The archive contains binary `easy_botnet_client.exe`. The simplest solution is to dump the network communication and inspect transfered data. The client connects to `78.128.216.92:20200` and sends the message `Easy-Bee-358n9pqh ready for work`. The server replies `Hello, your order is to keep in secret this flag: FLAG{MXcz-PrQK-FJbJ-jWVA}`.

### Wiretaped message

> Hi, junior investigator!
>
> We have wiretaped strange communication - probably a message. Try to decode it.
>
> Use password `wiREtaPeD-msG` to [download the evidence](wiretaped_message/wiretaped_message.zip)
>
> Good Luck!

Every message is encoded with 2 bytes for length of the message in big endian followed by data. Data are base64 encoded. I used following script to decode all data.

```python
import base64
import sys

f = open(sys.argv[1], 'rb')

for i in range(31):
	l = int.from_bytes(f.read(2), byteorder='big')
	b64 = base64.b64decode(f.read(l)).decode()
	print(l, b64)

f.close()
```

## Promotion

> Hi, junior investigator!
>
> You have successfully completed the training and earned the promotion to the **Executive Senior Investigator**. You are ready to get access to the malware research facility - just enter the code `FLAG{Jb91-XGSI-05xR-kqgQ}` and save the world from the RANSOMVID-20 imminent threat. Remember - many of our experienced investigators have been already digitally quarantined, so be careful!
>
> Good luck!

### Malware spreading

> Hi, executive senior investigator!
>
> We suspect that the malware is primarily spreaded somehow by e-mail. We have partial traffic dump from one small company, that was attacked. Try to check this hypothesis.
>
> Use password `ThE-MaLWr-MaIlZZz-20` to [download the evidence](malware_spreading/malware_spreading.zip)
>
> Good Luck!

The pcap from given archive contains 4 tcp connections to imap server. There is an email with `<winning_numbers.zip>` attachment in **Alice** mail box.

```
Return-Path: <lorem@genuine-national-lottery.cz>
X-Original-To: alice@cypherfix.cz
Delivered-To: alice@cypherfix.cz
Received: from mx.genuine-national-lottery.cz (mx.genuine-national-lottery.cz [203.0.113.150])
	by mail.cypherfix.cz (Postfix) with ESMTP id 013DD60535
	for <alice@cypherfix.cz>; Mon,  5 Oct 2020 22:01:09 +0200 (CEST)
Received: from [203.0.113.92] (mail-sor-f41.google.com [mail-sor-f41.google.com]) 
	by mx.genuine-national-lottery.cz (Postfix) with ESMTP id E4444821AA
	for <alice@cypherfix.cz>; Mon,  5 Oct 2020 20:01:08 +0000 (UTC)
Content-Type: multipart/mixed; boundary="===============2043998906902155698=="
MIME-Version: 1.0
User-Agent: Mutt/1.10.1 (2018-07-13)
Message-Id: <160192806888.20243.12819215096109337023@27f13e44ef5b>
From: Lorem Ipsum <lorem@genuine-national-lottery.cz>
To: Alice Nelson <alice@cypherfix.cz>
Subject: The prediction
Date: Mon,  5 Oct 2020 20:01:08 +0000 (UTC)

--===============2043998906902155698==
Content-Type: text/plain; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit

Dear Alice,
I know it - you are the right person to cooperate. The numbers you are looking for, are in attachment. The password was send on your cell. Enjoy your (our) prize!

Lorem
--===============2043998906902155698==
Content-Type: application/octet-stream
MIME-Version: 1.0
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename=<winning_numbers.zip>

UEsDBBQACQAIAIJYQVEJNsOIqEMAAPhTAAAaABwAbmF0aW9uX2xvdHRlcnlfbnVtYmVycy5vZHNV
VAkAA4SbdV+Em3VfdXgLAAEEAAAAAATnAwAAyGLAGz7fLqYUdXMocddTUam0LApC2qdKxDQauLyH
BICNYjxwXaRpajF37BmyLqE4m1vvi8ZfQJdFrX5IFDk/yoGhjOwmrTxVzf7K2F9pWZuDCRMw2b/W
...
AAD4UwAAGgAYAAAAAAAAAAAA+IEAAAAAbmF0aW9uX2xvdHRlcnlfbnVtYmVycy5vZHNVVAUAA4Sb
dV91eAsAAQQAAAAABOcDAABQSwUGAAAAAAEAAQBgAAAADEQAAAAA

--===============2043998906902155698==--
```

**Alice** than e-mailed to **John** about her struggle with the attachment, followed by secret password (`HappyWinner-paSSw00rd42`) necessary to open the attachment.

```
From: Alice Nelson <alice@cypherfix.cz>
To: John Johnson <john@cypherfix.cz>
Subject: Rich rich rich!

Johnny, I need your help!
I got the winning lottery numbers and we can be really rich :) But my computer is too slow or entro-something is wrong inside and it can't show me the numbers :(. I left a flash drive on your desk, run the only file that's there and gimme the results.
Thanks and see ya!
A.
```

```
From: Alice Nelson <alice@cypherfix.cz>
To: John Johnson <john@cypherfix.cz>
Subject: Rich and stupid :)

Oh my, you will need the secret 'HappyWinner-paSSw00rd42'. See ya! A.
```

We found `nation_lottery_numbers.ods` file in `<winning_numbers>.zip`. I run following commands to find the flag

```sh
7z x nation_lottery_numbers.ods
find -type f | xargs grep -F 'FLAG{'
```

### Attachment analysis

> Hi, executive senior investigator!
>
> Well done, we have acquired the malicious mail attachment. Now, you should take a closer look on it and find out, how it works.
>
> Use password `ThE-aTTacHmEnt-20` to download the evidence
>
> Good Luck!

### Downloaded file

> Hi, executive senior investigator!
>
> The file, you have acquired in previous investigation is not the malware, we were looking for. The attacker probably replaced it to fool us. Fortunatelly, we have a traffic dump, where you can probably find the original file. Try to find it and do not forget to be sure it is the correct file.
>
> Use password `ThE-doWNloAdeD-fIlE-20` to download the evidence
>
> Good luck!

### The Connection

> Hi executive senior investigator!
>
> Cool, you have found the malware dropped on target computer. According to your defined procedure and your previously detected IoC (indicators of compromise), we were able to find other versions of malware in traffic dumps - we assume it is some kind of botnet client. Unfortunatelly, it looks like the C2 server has been meanwhile upgraded and although the server reacts to client's messages, the client can't decode the orders. You should investigate the communication.
>
> Use password `ThE-CaNDc-cONNecTiOn-20` to download the evidence
>
> Good luck!

### Botnet master

> Hi, executive senior investigator!
>
> We have managed to get a rare catch - a traffic dump of issuing commands for the C2 server by its master! Glory to the network specialists of unnamed company. Try to find out how this communication works.
>
> Use password `maSTeR-aND-coMMAndEr` to download the evidence
>
> Our network analytics report that one of currently online C2 servers can be found on IP `78.128.216.92` on `TCP/20220`.
>
> Good luck!

### Ransomware

> Hi, executive senior investigator!
>
> Finally, we have acquired the `RANSOMVID-20` encryption module. According to the information from our partners, it encrypts files on any drives, it can found. We have also one image of relatively small drive, which was affected by `RANSOMVID-20` only (no user or system action were undertaken). Try to find out how to decrypt the files without paying any single TCC.
>
> Use password `rAnSOmVID-20` to download the evidence
>
> Good luck!
>
> **WARNING: The ransomware executable is dangerous - virtual machine is strongly recommended for the analysis.**

## Epilogue

> Hi, savior of the world!
>
> You have succesfully analyzed all aspects of the dreadful malware, which has threatened the Internet population. The digital quarantine can be now lifted and the happy users can return to their ordinary activities - especially to searching pictures and videos of fluffy cute kittens...
>
> We would like to ask you to fill short questionnaire - we need some information for eventual prize delivery.
>
> You can also enter the flag `FLAG{aKAL-qQhH-MsAz-miUG}` to set this challenge green :-)
>
> See you!
