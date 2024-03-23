#!/bin/env bash

cd ~/.011/chroot/share/.011/011/cert || exit "can't \`cd' exiting..."


#Generate CCITSARCA.pem, CCITSARCA.key & CCITSARCA.crt:
openssl req -x509 -nodes -new -sha256 -days $((366 * 17)) -newkey rsa:2048 -keyout CCITSARCA.key -out CCITSARCA.pem -subj "/C=UG/L=Kampala/ST=Busia, monni/O=CCI Trust Services PLLC/OU=Restute/CN=CCITS Assured Root CA"

openssl x509 -outform pem -in CCITSARCA.pem -out CCITSARCA.crt


#Generate localhost.key, localhost.csr, and localhost.crt:
openssl req -new -nodes -newkey rsa:2048 -keyout localhost.key -out localhost.csr\
    -subj "/C=UG/L=Kampala/ST=Busia, monni/O=LocalHost/OU=Restute/CN=localhost"

openssl x509 -req -sha256 -days $((366*17)) -in localhost.csr -CA CCITSARCA.pem\
    -CAkey CCITSARCA.key -CAcreateserial -out localhost.crt -extfile /proc/self/fd/3 3<<EOF
    authorityKeyIdentifier=keyid,issuer
    basicConstraints=CA:FALSE
    keyUsage = digitalSignature,nonRepudiation,keyEncipherment,dataEncipherment
    subjectAltName = @alt_names
    [alt_names]
    DNS.1 = localhost
    DNS.2 = localhost:8443
EOF
