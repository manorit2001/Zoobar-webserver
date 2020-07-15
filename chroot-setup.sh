#!/bin/sh -x
if id | grep -qv uid=0; then
    echo "Must run setup as root"
    exit 1
fi

create_socket_dir() {
    local dirname="$1"
    local ownergroup="$2"
    local perms="$3"

    mkdir -p $dirname
    chown $ownergroup $dirname
    chmod $perms $dirname
}

set_perms() {
    local ownergroup="$1"
    local perms="$2"
    local pn="$3"

    chown $ownergroup $pn
    chmod $perms $pn
}

rm -rf /jail
mkdir -p /jail
cp -p index.html /jail

./chroot-copy.sh zookd /jail
./chroot-copy.sh zookfs /jail

#./chroot-copy.sh /bin/bash /jail

./chroot-copy.sh /usr/bin/env /jail
./chroot-copy.sh /usr/bin/python /jail

# to bring in the crypto libraries
./chroot-copy.sh /usr/bin/openssl /jail

mkdir -p /jail/usr/lib /jail/usr/lib/i386-linux-gnu /jail/lib /jail/lib/i386-linux-gnu
cp -r /usr/lib/python2.7 /jail/usr/lib
cp /usr/lib/i386-linux-gnu/libsqlite3.so.0 /jail/usr/lib/i386-linux-gnu
cp /lib/i386-linux-gnu/libnss_dns.so.2 /jail/lib/i386-linux-gnu
cp /lib/i386-linux-gnu/libresolv.so.2 /jail/lib/i386-linux-gnu
cp -r /lib/resolvconf /jail/lib

mkdir -p /jail/usr/local/lib
cp -r /usr/local/lib/python2.7 /jail/usr/local/lib

mkdir -p /jail/etc
cp /etc/localtime /jail/etc/
cp /etc/timezone /jail/etc/
cp /etc/resolv.conf /jail/etc/

mkdir -p /jail/usr/share/zoneinfo
cp -r /usr/share/zoneinfo/America /jail/usr/share/zoneinfo/

create_socket_dir /jail/echosvc 61010:61010 755
create_socket_dir /jail/authsvc 61016:61016 755
create_socket_dir /jail/banksvc 61017:61017 755

mkdir -p /jail/tmp
chmod a+rwxt /jail/tmp

mkdir -p /jail/dev
mknod /jail/dev/urandom c 1 9

cp -r zoobar /jail/
rm -rf /jail/zoobar/db

python /jail/zoobar/zoodb.py init-person
python /jail/zoobar/zoodb.py init-transfer
python /jail/zoobar/zoodb.py init-cred
python /jail/zoobar/zoodb.py init-bank
chown -R 61015:61015 /jail/zoobar/db/person
chown -R 61015:61015 /jail/zoobar/db/transfer
# chown -R 61016:61016 /jail/zoobar/db/cred
# chown -R 61012:61012 /jail/zoobar/media
# chown 0:0 /jail/zoobar/media
set_perms 61013:61013 755 /jail/zoobar/index.cgi
set_perms 61015:61015 770 /jail/zoobar/db/person/person.db
set_perms 61017:61017 700 /jail/zoobar/db/transfer/transfer.db
set_perms 61017:61017 700 /jail/zoobar/db/bank/bank.db
set_perms 61016:61016 700 /jail/zoobar/db/cred/cred.db
set_perms 61016:61016 700 /jail/zoobar/db/cred
set_perms 61017:61017 700 /jail/zoobar/db/bank
set_perms 61017:61017 700 /jail/zoobar/db/transfer
# set_perms 61016:61016 770 /jail/zoobar/db/transfer/transfer.db
# set_perms 123:456 777 /jail/zoobar/db/person/person.db
# set_perms 123:456 777 /jail/zoobar/db/transfer/transfer.db
