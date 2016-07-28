# Meaningless

When dealing with a group of things, using string as a unique identifier for each one of them is not a good idea because people change their minds. A good unique identifier should not change over time, so it is desirable to remove any meaning from the identifier. An unsigned 64-bit integer is generally good.

The trouble is, unlike UUIDs, integers draw an illusion of nonexistent meaning: "The object with ID 1 should somehow important" or "the object 10 and 11 should be somehow related." Therefore, even when these identifiers are _stored_ as integers, we want to _display_ them as a series of completely meaningless characters with no regularity, just like how UUIDs look.

Meaningless is a simple codec function intended to serve such purpose: excise the meaning from integers. It is a bijective function for unsigned 64-bit integers with fast encoding and decoding.

## Usage

```python
# You need to fix the 64-bit prime below to get consistent results.
# If you have OpenSSL installed, you may get one with:
# openssl prime -generate -bits 64 -hex
>>> m = Meaningless(0xeb57c60ca37bf6d2)
>>> m.encode(27)
15150640503858120147
>>> m.decode(15150640503858120147)
27
>>> m.encode_hex(264)
'b2843c60a49dc7c8'
>>> m.decode_hex('b2843c60a49dc7c8')
264
```

## Warning

Meaningless only removes the meaning from the displayed digits, not securely protect them. Hostile adversaries can still easily figure out the algorithm beneath the seemingly random hexadecimal characters. If it is important to, for example, prevent the guesswork of the previous or the next sequential identifier, don't use this function. Choose a real symmetric encryption algorithm like AES or ChaCha20, and properly protect the secret key.
