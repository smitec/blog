---
layout: post
title:  "Connecting a NTC C.H.I.P to eduroam"
date:   2016-02-18 11:03:16 +1000
tags: meta ntc next thing co chip uq
---

So I got a [C.H.I.P][cp] today. I happened to be at the University of Queensland today and wanted to 
play around with it. As the university runs eduroam I guessed it might be a little
bit of a challenge. After several attempts I managed to get it connected. Here is
what I did to get it on the network.

I am assuming your CHIP came straight out of the box and was plugged into your
machine. I was talking to it via [minicom][mc] on my mac. It is possible that
other configurations will work but this is what worked for me in the end.

## Step 1 - interfaces

First step open up `/etc/network/interfaces` in `vi` and add the following lines
to the bottom of the file. After the `source-directory ...` line.

{% highlight bash %}
auto wlan0
iface wlan0 inet manual
wireless-power off
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp
{% endhighlight %}

## Step 2 - wpa_supplicant.conf

Now we are going to create the `wpa_supplicant.conf` file we referenced above.
At this point it wont exist so create the file `/etc/wpa_supplicant/wpa_supplicant.conf`
and add the following. Change `<password>` to your password and `<identity>` to your
identity.

{% highlight bash %}
network={
  ssid="eduroam"
  scan_ssid=1
  key_mgmt=WPA-EAP
  eap=TTLS
  identity="<identity>"
  phase2="auth=PAP"
  password="<password>"
}
{% endhighlight %}

## Step 3 - reboot
Now I found some things that said running `/etc/init.d/networking restart` would
make things work but I had no success with that. I ran a quick `reboot` and after
a minuet or so I had an IP address and could ping google.

Hooray! Hopefully someone finds this helpful. Let me know on twitter at [@smitec][tw]
if you do.

[tw]: https://twitter.com/smitec
[mc]: https://en.wikipedia.org/wiki/Minicom
[cp]: http://getchip.com/
