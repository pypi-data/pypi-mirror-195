# Fernet Encryption CLI tool

## Install
Use [pipx](https://pypa.github.io/pipx/) to install globally in an isolated python environment.
```bash
pipx install fernet-encrypt
```

## Usage
```
Commands:
  create-fernet-key
  encrypt-file
  decrypt-file
```

### create-fernet-key
Create a new fernet key to sign with. Keys will be stored in fernet-encrypt install location. When decrypting, all available keys will be tried until one succeeds or they are all exhasted.
```
Usage: fernet-encrypt create-fernet-key [OPTIONS]

Options:
  --help  Show this message and exit.
```

### encrypt-file
Encrypt provided `INPUT_FILE` with the newest fernet key (see `create-fernet-key`). The encrypted output will be directed to `OUTPUT_FILE` if provided. Otherwise output will be directed to stdout.
```
Usage: fernet-encrypt encrypt-file [OPTIONS] INPUT_FILE
                                   [OUTPUT_FILE]

Arguments:
  INPUT_FILE     [required]
  [OUTPUT_FILE]

Options:
  --help  Show this message and exit.
  ```

### decrypt-file
Decrypt provided `INPUT_FILE`. All existing fernet keys will be used for decryption until one succeeds or they are all exhasted. The decrypted output will be directed to `OUTPUT_FILE` if provided. Otherwise output will be directed to stdout.
```
fernet-encrypt decrypt-file [OPTIONS] INPUT_FILE
                            [OUTPUT_FILE]

Arguments:
  INPUT_FILE     [required]
  [OUTPUT_FILE]

Options:
  --help  Show this message and exit.
  ```
