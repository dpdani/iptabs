# iptabs
A tool that lets you easly manage your iptables configurations by describing them in files which makes configuring easier to read and re-use.

## Installation
To install iptabs, clone this repo:
```
git clone https://github.com/dpdani/iptabs.git
cd iptabs
sudo pip3 install -r requirements.txt
```

## Basic Usage
Let's make a basic firewall set-up with iptabs:
```
~INPUT  # working on the input chain
  ACCEPT>
    dport: ssh
    sport: 10706 ?  # also log this
  DROP>
    proto: icmp
```
(this example is `examples/simple_input.ipbs`) <br>
To configure iptables from an iptabs file simply call:
```
python3 iptabs/main.py yourfile.ipbs
```
Internally, iptabs makes calls to iptables. To see what calls would be attempted without actually making them, you can use the `--debug` option. A sample output from `examples/simple_input.ipbs` would be:
```
$ python3 iptabs/main.py examples/simple_input.ipbs --debug
Parsed from file 'examples/simple_input.ipbs':
  On INPUT chain:
    sport: 10706 => LOG
    dport: ssh => ACCEPT
    proto: icmp => DROP
Are you sure you want to append these rules to iptables? [y/N] y
[DEBUG]  $ iptables -A INPUT --protocol tcp --sport 10706 -j LOG
[DEBUG]  $ iptables -A INPUT --protocol tcp --dport ssh -j ACCEPT
[DEBUG]  $ iptables -A INPUT --protocol tcp --proto icmp -j DROP
$ _
```
You can find more sample iptabs files in the `examples` folder.

### A short story
This project initially was a simple school homework, but it kind of evolved into a new language to describe iptables configurations.
Putting this here just in case somebody finds this kind of references in old commits.
