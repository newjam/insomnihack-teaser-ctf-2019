
We are given the following challenge text
```
Use this API to gift drink vouchers to yourself or your friends!

http://drinks.teaser.insomnihack.ch

http://146.148.126.185 <- 2nd instance if the first one is too slow

Vouchers are encrypted and you can only redeem them if you know the passphrase.

Because it is important to stay hydrated, here is the passphrase for water: WATER_2019.

Beers are for l33t h4x0rs only.
```

The source in [`drinks.py`](https://github.com/newjam/insomnihack-teaser-ctf-2019/blob/master/drinks/drinks.py) is a flask web service that allows two actions, `POST` to `/generateEncryptedVoucher` or `/redeemEncryptedVoucher`.

When supplied with a `recipientName` and a `drink`, `generateEncryptedVoucher` returns a PGP encrypted (and compressed) message.

```
-----BEGIN DRINK VOUCHER-----

jA0ECQMCZ874uMp5QGT/0l0Bl8uoi/5zbMUGgECbbk4WDtzQz7dIncIPHwExedXK
jEMMcey7mbvq5SWGAvhMz0Izf1e8+3kiiNpss22tIWoJTWPwX+tvX2C2j73Yn/Nt
lYGzx3QsBsHsN4mu1JU=
=iNtZ
-----END DRINK VOUCHER-----
```

By examining the code [`drinks.py`](https://github.com/newjam/insomnihack-teaser-ctf-2019/blob/master/drinks/drinks.py), we can see that each drink has a "coupon code" and the the drink voucher plaintext is the concatenation of the `recipientName` and the coupon code corresponding to the `drink`.
The symmetric passphrase used to encrypt the plaintext is also the coupon code for the drink.

`redeemEncryptedVoucher` takes the drink voucher, and the coupon code (aka passphrase) and checks that the supplied coupon code matches the coupon code in the plaintext of the drink voucher, and we see the flag is the the coupon code.

At first I spent a long time researching vulerabilities to gnupg symmetric key encryption and a lot of promising looking, but ultimately fruitless, leads came up.
Eventually, though, I read that pgp compresses the message before encrypting it.
This was the eureka moment, and I realized the if the `recipientName` we supply to `generateEncryptedVoucher` was similar to the coupon code for the `drink`, the length of the drink voucher would be less than if they were disimilar.
Thus we have an oracle which leaks information about the rest of the plaintext!

For example
```
len(generateEncryptedVoucher('', 'water')) == 179
```
and
```
len(generateEncryptedVoucher('WATER_2019', 'water')) == 179
```
Since our plaintext is `WATER_2019||WATER_2019`, the common strings are compressed.

However,
```
len(generateEncryptedVoucher('!@#$%^&*()', 'water')) == 191
```
because the plaintext is `!@#$%^&*()||WATER_2019`, and can not be compressed as much.

The [solution](https://github.com/newjam/insomnihack-teaser-ctf-2019/blob/master/drinks/client.py) is to start with an prefix and check the length of ciphertext of the prefix appended with each character in the alphabet.
If the length is less than the others, it is considered a candidate in the next round.
In practice, some manual intervention is required to eliminate unlikely prefixes, such as `G1MME________` in favor of more likely prefixes such as `G1MME_B33R_PL`. For example, I left the algorithm to run and this is what it decided the flag was: `G1MME_B33R_PLZ_1MME_B33RY_TH1RSTY`, even though the correct flag is `G1MME_B33R_PLZ_1M_S0_V3RY_TH1RSTY`

This is the same exploit as this ctf challenge, https://systemoverlord.com/2013/04/30/plaidctf-compression/,
as well as another recent ctf, which I forget.

This was a fun challenge, thanks to insomnihack!
