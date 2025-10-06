## You may need to generate virtaul alias and mailbox databases by running:

```sh
sudo postmap /etc/postfix/vmailbox
sudo postmap /etc/postfix/valiases
```

## Start both dovecot and postfix:

sudo systemctl start dovecot
sudo systemctl start postfix


## How to structure the virtaul directories ccan be found in [./vmail-directory-structure.txt](./vmail-directory-structure.txt)
