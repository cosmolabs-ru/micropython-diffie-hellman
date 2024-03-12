import dh

difhel = dh.DH()
bob_difhel = dh.DH()


def start_test():
    print('Started making keypairs')

    difhel.make_keypair()
    bob_difhel.make_keypair()  # we don't have a real Bob, so we make his public key here for test
    #  In real, Bob shares his public key with you

    print('my secret key: ', difhel.secret)
    print('my public key: ', difhel.public, '\r\n')

    print('Bob\'s public key: ', bob_difhel.public)

    print('Started making shared secret')
    shared_key = difhel.make_shared_secret(bob_difhel.public)
    print('Shared key: ', shared_key)

# Shared key is 4095 bits (512 bytes) long.
# Feed it into sha3 (or a KBKDF) and use the result as an AES encryption key.
# or split it into 16 portions by 32 bytes and get a 16-array of keys with enough entropy.
