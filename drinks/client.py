from requests import get, post


#URL = 'http://drinks.teaser.insomnihack.ch'
#URL = 'http://146.148.126.185'
URL = 'http://localhost:5000'

def generateEncryptedVoucher(recipientName, drink, base_url = URL):
  return post(base_url + '/generateEncryptedVoucher', json = {
    'recipientName': recipientName,
    'drink': drink
  }).text

def redeemEncryptedVoucher(encryptedVoucher, passphrase, base_url = URL):
  return post(base_url + '/redeemEncryptedVoucher', json = {
    'encryptedVoucher': encryptedVoucher,
    'passphrase': passphrase
  }).text

from string import ascii_uppercase, digits

alphabet = ascii_uppercase + '_' + digits

def logged_oracle(sample):
  print('trying: %s' % sample)
  l = oracle(sample)
  print('%s has length %i' % (sample, l))
  return l

def oracle(sample):
  return len(generateEncryptedVoucher(sample, 'beer'))

# it's unlike the flag will have three repeated characters
# but repeated characters in the plaintext dont effect the length of the ciphertext
# so they should be dropped early to prevent exponential growth of our search space.
def conspicuous(sample):
  return len(sample) >= 3 and len(set(sample[-3:])) == 1

def filterProbable(samples):
  smallest = min([l for _, l in samples])
  return [p for p, l in samples if l == smallest]

# gnupg compresses the plaintext before encrypting.
# Since the flag is in the plaintext, the length of the ciphertext will be shorter if we have correctly guessed a portion of the plaintext

# nextPrefixes : [string] -> [string]
def nextPrefixes(prefixes):
#  print('trying: %s' % str(prefixes))
  samples = [(prefix + a, oracle('||' + prefix + a * 5)) for a in alphabet for prefix in prefixes if not conspicuous(prefix + a)]
  return filterProbable(samples)

def find():
  prefixes = ['G']
  for _ in range(33):
    prefixes = nextPrefixes(prefixes)
    print(prefixes)


