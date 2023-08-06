# archimedes-config

This library handles config files for services used by Optimeering AS.

The library is built around `ConfigManager` class. An instance of this class is meant to represent a single set of configuration for the execution environment. The library can also be used to encrypt and decrypt configurations selectively for security.

## Installation
The library is published on PyPi as "archimedes-config".

### Pip

```
# Base installation
pip install archimedes_config

# Installation with keyvault feature
pip install archimedes_config[azure_keyvault]
```

### Poetry

```
# Base Installation 
poetry add archimedes_config

# Installation with keyvault feature
poetry add archimedes_config[arcimedes_vault]
```

### Using azure key vault for secret key management

To authenticate to azure key vault service, `AZURE_TENANT_ID` , `AZURE_CLIENT_ID` and `AZURE_CLIENT_SECRET` should be set up as environment variable. If any one of these environment variables have not been set up, the authentication will instead be done though Azure CLI utility. Failing both the authentication process will raise an exception.

## Configuration Specification

1. The configuration should be in TOML standard.
2. There should be no root level configuration.
3. All the configurations are expected to be under one and only one level of group.
4. Each configuration must have `value` key where the value for the configuration must be store. All types supported by TOML are supported.
5. Additionally, each configuration can optionally have another key `encrypted`. The value for this must be boolean. This flag determines if the provided value is a secret; i.e. if the value must be encrypted or decrypted.
6. If `encrypted` is True, the `value` field must be a string.
7. If `encrypted` field is not available in the configuration, the `value` will be treated as an unprotected config and will be excluded from encryption and decryption.


    The library has adequate functionality to create a new configuration and add key values to existing ones. 
    While it is possible to manually create/ edit the cnfiguration, it is recomended to use the functionality provided to make changes to the configurations.

### Configuration keys

1. Key `_IS_CONFIG_ENCRYPTED` under  `CONFIGURATIONS` group : 
   - Used to determine encryption state of the configuration during load.
   - This is a required configuration.
2. Key `VAULT_NAME` under  `AZURE_KEYVAULT` group :
   - Name of vault to connect to.
   - Only required if Key Vault feature is used.
3. Key `VAULT_KEY` under  `AZURE_KEYVAULT` group :
   - Name of the key holding the encryption/decryption secret is store.
   - Only required if Key Vault feature is used. 


## Usage

### Import ConfigManager class

`from archimedes_config import ConfigManager`

ConfigManger is an in memory storage for all the configuration.

Features related to azure key vaults has been implemented in another Manager class.
To use keyvault features, use `KeyvaultConfigManager` instead.

`from archimedes_config import KeyvaultConfigManager`

All the interfaces for the two classes are same except the addition of `set_default_key_from_key_vault` method to set the secret key configured in azure vault as the default key for encryption and decryption of configurations.

### Create a new configuration set

```
config = ConfigManager()
config.create()
```

This instantiates a new config in memory.

### Load an existing configuration set

```
config = ConfigManager()
config.load(path = <PATH_TO_CONFIG> )
```

The `load` method optionally has the following parameters:
1. `default_key`
   - Assigns a default secret for encryption and decryption
2. `decrypt_on_load`
    - Decrypts the configurations on load

### Assign a default key

Fernet can be used to create a new key.
```
from cryptography.fernet import Fernet
secret = Fernet.Fernet.generate_key()
```

To add the key as a default key for the configuration instance.
```
config.set_default_key(key = secret)
```

To add secret from Azure key vault as encryption/ decryption key,
```
config = KeyvaultConfigManager()
config.set_default_key_from_key_vault()
```

### Add new configuration

To add a new configuration key value pair,
```
config.add_new_config(
        group_name = <NAME_OF_GROUP> ,
        key_name = <KEY_NAME>,
        unencrypted_values = <CONFIG_VALUE>,
        encrypted = <ENCRYPTION_FLAG>
    )
```
Additionally, the method optionally supports the following parameters:

1. `create_group_if_not_exist`
   - Boolean flag.
   - If True, creates new group if the group doesn't exist.
   - If False, raised an exception if the group doesn't exist.
   - 
2. `allow_updating`
   - Boolean flag.
   - If True, allows update of existing key value pair.
   - If False, raises an exception if key value pair already exists.

### Encrypt configurations
Encrypts all the configurations.
```
config.encrypt_configs()
```

### Decrypt configurations

Decrypts all the configuration.
```
config.decrypt_configs()
```

### List all groups in configurations

```
config.list_groups()
```

### List all keys under a group

```
config.list_keys(group = <NAME_OF_GROUP>)
```

### Get a single value for configuration

```
value = config.get(<NAME_OF_GROUP> , <NAME_OF_KEY>)
```
The `get` method optionally has `default_return` parameter. By default, if the group or the key is not found in the configuration set, a Key error is raised. If `default_return` is set, if the group or the key is not found, the value provided under `default_return` is returned instead.

### Saving a configuration set

```
config.save()
```

The `save` method optionally accepts the following parameters:
1. `path`
    - Path to save the configuration set.
     - If not set, will overwrite the configuration in the path used while calling the `load` method.
2. `allow_saving_decrypted`
    - Allows saving decrypted config.
     - By default, attempting to save a decrypted config results in an exception for security purposes. This flag allows saving protected secrets in plain text.


> All the operations performed on the configuration instance is performed on memory. 
`To persist the changes onto local disk, `save` method must be called.

### Generating a new key and encrypting configuration with the new key

```
config.create_new_key(<PATH_TO_SAVE_NEW_CONFIGURATION>, <PATH_TO_SAVE_NEW_KEY>)
```
The `create_new_key` method generates a new key and encrypts the loaded config with the new key. 
The new config and key is exported to provided paths respectively.
