A Bash script, transfer, which serves as a convenience for using the rsync 
command to copy files between two directories, one of which may reside on 
another host. The executing format of transfer is:
```shell
$ transfer transfer-options config-file.xml
```

The XML configuration file plus transfer-options provide the specifications for
how to run the rsync command. The XML file provides two directories, SRC and DST
so that the outcome is either:

rsync rsync-options SRC/ DST/   or   rsync rsync-options DST/ SRC/

The transfer script should be written to work in the most general way possible:

1. It is to be deployed in the /usr/local/bin directory and usable by all users
on the system.
2. It can be invoked anywhere in the system so as long as the paths to the config file
and affected directories are correct relative to the shell's working directory.
3. The directory containing the XML configuration file, the SRC and DST directories 
need not bear any relation to each other.
4. It relies on one python support script to validate and parse the XML file. 
Otherwise, it should use only bash scripting and build-in system operations.
5. It is complete as is and does not source any other files.
    
## Getting started ##

The python support script requires a package which must be installed:
```shell
$ sudo apt-get install python-lxml
```

If you want the rsync man page as a pdf document:
```shell
$ man -Tps rsync | ps2pdf - rsync.pdf
```

## XML configuration file ##

The XML configuration files used by transfer have this format:
```shell
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE sync SYSTEM "/usr/local/share/xml/declaration/transfer.dtd">
<sync src="SRC" dst="DST">
  <rules>
   + pattern
   - pattern
   ...
  </rules>
</sync>
```

The DTD file spells out the most basic requirements:
**----------------------------------------/usr/local/share/xml/declaration/transfer.dtd**
```shell
<!ELEMENT sync (rules?)>
<!ELEMENT rules (#PCDATA)>
<!ATTLIST sync src CDATA #REQUIRED>
<!ATTLIST sync dst CDATA #REQUIRED>
```

In particular:
1. The top level sync element may have a single rules sub-element, i.e., rules is optional.
2. The src and dst are required attributes of the top level sync element.

The rules element, if it exists, should contain inclusion(+)/exclusion(-) patterns , one
per line. Legitimate lines, when trimmed, have these possibilities:
1. They are empty
2. They start with a "+"
3. They start with a "-"

The value of "SRC" or "DST" can be a regular directory or a remote directory specification, e.g.,
`dst="USER_NAME@EXAMPLE.COM:someDirectory"`

## Operational Semantics

Execution with no parameters should give the following synopsis of the command usage:
```shell
  usage: transfer [options] config-file.xml
  options:
  -d or -u: download or upload, resp. one and only one must be present
  -f:       force transfer regardless of later timestamp on target file
  -x:       delete items in target not present in source
  -t:       (testing) show the contents of the exclusion rules file,
            the full rsync command and terminate without doing anything
```

The options can be used separately, e.g., -u -f -x or compressed, i.e., -ufx.

The intention is to use the XML configuration file and the **transfer-options** to create
and run an rsync command:

rsync **rsync-options** SRC/ DST/
or
rsync **rsync-options** DST/ SRC/

Here are the points about the creation of the rsync command used:
1. The -a rsync option is always present. We'll assume you are transferring from one UNIX
like system to another in which the file permissions are equivalent. When transferring from
a Windows system (e.g. in Cygwin shell) you want to use "rsync -rt" to avoid invalid permissions
being set.
2. One **and only one** of the transfer-options -u and -d must be present.
if -u(upload) is present, the dst value is the target:
rsync -a **other-rsync-options** SRC/ DST/
if -d(download) is present, the src value is the target:
rsync -a **other-rsync-options** DST/ SRC/
3. The directories used by the rsync command **must** be terminated with "/".
4. If the -f(force) option is **not** present, it means that -u **is** one of the
**other-rsync-options**. Conversely, if the -f transfer-options **is** present it means that
-u option is **not** one of the **other-rsync-options**. The implication is that target files
with later timestamps are not overwritten unless -f is present.
5. If the -x transfer-option is present, then --delete is one of the **other-rsync-options**.
6. If there is a rules element, then **other-rsync-options** contains this:
`--exclude-from="$rules_file"`
where *$rules_file* is a temporary file holding the edited content of the rules element.


# Testing the transfer script during development:

Use this as the basis:
```shell
$ ./setup2
```
and test run:
```shell
$ ./transfer -u sample.xml 
$ ./transfer -uf sample.xml
$ ./transfer -ux sample.xml
$ ./transfer -ufx sample.xml
$ ./transfer -d sample.xml
$ ./transfer -dx sample.xml
```

# Final step

The final step to get the target executable:
```shell
$ cd ~/program1
$ sudo cp transfer /usr/local/bin/
```
which should be usable as "transfer" anywhere on your system.

## Vagrant Box ##

Using a Vagrant Box, start the ubuntu virtual machine:
```shell
$ vagrant up
```
Log into the machine:
```shell
$ vagrant ssh
```
Change into the /vagrant directory:
```shell
$ cd /vagrant
```
To exit the machine:
```shell
$ exit
```
To stop the machine:
```shell
$ vagrant halt
```
