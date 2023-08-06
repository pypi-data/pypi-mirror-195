import typing, os, solcx, logging, web3
from web3 import Web3
from .exception import *
from .utils import *

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s')

if int(web3.__version__.partition('.')[0]) < 6:
    build_transaction = 'buildTransaction'
else:
    build_transaction = 'build_transaction'

class ETHClient:

    def __init__(
        self,
        node_host: str = 'localhost',
        node_port: typing.Union[str, int] = 8545,
        node_connection_type: str = 'http',
        node_consensus: str = 'PoA'
    ):

        self.w3 = None

        if node_host and node_port and node_connection_type and node_consensus:
            self.connect(
                node_host,
                node_port,
                node_connection_type,
                node_consensus
            )

    @property
    def isConnected(
        self
    ) -> bool:

        if isinstance(self.w3, Web3):
            return self.w3.isConnected()
        return False

    @staticmethod
    def parse_json(
        data
    ) -> typing.Any:

        if isinstance(data, (list, set, tuple)):
            return [ETHClient.parse_json(i) for i in data]
        elif isinstance(data, (dict, AttributeDict)):
            return {k: ETHClient.parse_json(v) for k,v in data.items()}
        elif isinstance(data, HexBytes):
            return data.hex()
        elif isinstance(data, bytes):
            return '0x'+data.hex()
        elif not isinstance(data, (str, int, float)):
            return str(data)
        else:
            return data
    
    @staticmethod
    def parse_param(param: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:

        if 'tuple' == param['type']:
            return [ETHClient.parse_param(i) for i in param['components']]
        elif 'tuple[' in param['type']:
            return [[ETHClient.parse_param(i) for i in param['components']]]
        
        return param['name'] + ':' + param['type']
        
    @classmethod
    def parse_abi(cls, contract_abi: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[typing.Dict[str, typing.Any]]:

        return [{
            'name': i['name'],
            'type': 'call' if i.get('stateMutability', 'view') in ['pure', 'view'] else i.get('stateMutability', None),
            'inputs': [cls.parse_param(j) for j in i.get('inputs', [])],
            'outputs': [cls.parse_param(j) for j in i.get('outputs', [])]
        } for i in contract_abi if i['type'] == 'function']
    
    def parse_args(
        self,
        args: typing.Iterable = [],
        kwargs: typing.Dict[str, typing.Any] = {}
    ) -> typing.Tuple[typing.Tuple[typing.Any], typing.Dict[str, typing.Any]]:

        def parse_data(self, data: typing.Union[str, int]) -> typing.Any:
            
            if isinstance(data, str):
                if 'b:' == data[:2]:
                    if '0x' == data[2:4]:
                        return bytes.fromhex(data[4:].lower())
                    return bytes.fromhex(data[2:].lower())
                if '0x' == data[:2] and len(data) == 42 and not self.w3.isChecksumAddress(data):
                    return self.w3.toChecksumAddress(data.lower())
            return data

        return (parse_data(self, i) for i in args), {k:parse_data(self,v) for k,v in kwargs.items()}

    def parse_address(self, address: typing.Optional[str]) -> typing.Optional[str]:

        if isinstance(address, str) and not self.w3.isChecksumAddress(address):
            return self.w3.toChecksumAddress(address.lower())
        return address

    def connect(
        self,
        node_host: str,
        node_port: typing.Union[str, int] = 8545,
        node_connection_type: str = 'http',
        node_consensus: str = 'PoA',
    ):

        if node_connection_type == 'ipc':
            os.environ['WEB3_PROVIDER_URI'] = f'file://{node_host}'
        else:
            os.environ['WEB3_PROVIDER_URI'] = f'{node_connection_type}://{node_host}:{node_port}'

        self.w3 = Web3()
        
        if node_consensus.lower() == 'poa':
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        if not self.w3.isConnected():
            raise ConnectionError('Can not connected to ethereum node. Check your node firewall and make sure enable connection and try again.')

    @check_connection
    def create_account(
        self,
        password: str
    ) -> typing.Dict[str, typing.Any]:
        
        new_account = self.w3.eth.account.create()
        encrypted_key = new_account.encrypt(password)

        return {
            "account": new_account,
            "encrypted_key": encrypted_key
        }
    
    @check_connection
    def get_account(
        self,
        password: str,
        encrypted_key: typing.Dict[str, typing.Any]
    ) -> LocalAccount:

        account = self.w3.eth.account.from_key(
            self.w3.eth.account.decrypt(
                encrypted_key,
                password
            )
        )

        return account

    @check_connection
    def get_account_from_key(
        self,
        private_key: str
    ) -> LocalAccount:

        account = self.w3.eth.account.from_key(private_key)

        return account
    
    @check_connection
    def get_account_properties(
        self,
        address: str
    ) -> typing.Dict[str, typing.Any]:

        address = self.parse_address(address)

        return {
            "address": address,
            "balance": self.w3.eth.get_balance(address),
            "nonce": self.w3.eth.get_transaction_count(address)
        }

    @check_connection
    def change_account_password(
        self,
        old_password: str,
        new_password: str,
        encrypted_key: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:

        account = self.get_account(old_password, encrypted_key)

        new_encrypted_key = account.encrypt(new_password)

        return new_encrypted_key

    @check_connection
    def transfer(
        self,
        to: typing.Union[LocalAccount, str],
        value: int = -1,
        message: str = '',
        nonce: int = None,
        gas_price: int = None,
        account: LocalAccount = None,
        password: str = None,
        encrypted_key: typing.Dict[str, typing.Any] = None,
        private_key: str = None
    ) -> TxData:

        if not (isinstance(account, (LocalAccount, Account)) or \
            (isinstance(password, str) and isinstance(encrypted_key, dict)) or \
            isinstance(private_key, str)):
            raise TypeError('At least "account" parameter or "private_key" or "password" and "encrypted_key" parameter must be provided')

        if not isinstance(account,(LocalAccount, Account)):
            if isinstance(password, str) and isinstance(encrypted_key, dict):
                account = self.get_account(password, encrypted_key)
            else:
                account = self.get_account_from_key(private_key)

        if isinstance(to, (LocalAccount, Account)):
            to = to.address
        elif isinstance(to, str) and '0x' == to[:2]:
            to = self.parse_address(to)
        else:
            raise TypeError("to parameter must be address string or LocalAccount")
        
        current_nonce = nonce or self.w3.eth.get_transaction_count(account.address)

        message_gas = 0
        if message:
            message = self.w3.toHex(text=message)
            message_gas = (len(message)//2 - 1) * 68
        total_gas = 21000 + message_gas

        transaction = {
            "from": account.address,
            "to": to,
            "value": value,
            "data": message,
            "gas": total_gas,
            "nonce": current_nonce,
            "chainId": self.w3.eth.chain_id
        }

        if not isinstance(gas_price, int):
            gas_price = self.w3.eth.gas_price
        
        transaction['gasPrice'] = gas_price

        account_balance = self.w3.eth.get_balance(account.address)

        if value < 0:
            value = account_balance - total_gas * gas_price

        total_cost = value + total_gas * gas_price

        if account_balance < total_cost:
            raise ValueError(str(total_cost - account_balance)+' minimum needed to be added to do transaction. Ask admin to send it to you.')

        signed_transaction = account.sign_transaction(transaction)

        transaction_hash = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        return self.get_transaction(transaction_hash)
    
    @check_connection
    def estimate_transfer_price(
        self,
        value: int = 0,
        message: str = '',
        gas_price: int = None,
    ) -> typing.Dict[str, int]:

        message_gas = 0
        if message:
            message = self.w3.toHex(text=message)
            message_gas = (len(message)//2 - 1) * 68
        total_gas = 21000 + message_gas
        if not isinstance(gas_price, int):
            gas_price = self.w3.eth.gas_price

        return {'cost': total_gas*gas_price, 'value': value, 'total': total_gas*gas_price+value}
    
    def compile_contract(
        self,
        source_files: typing.Union[str, Path, typing.List[typing.Union[str, Path]]],
        solc_version: str = None,
    ) -> typing.Dict[str,typing.Dict[str, typing.Any]]:

        installed_version = [str(i) for i in solcx.get_installed_solc_versions()]

        if isinstance(solc_version, str):
            if str(solcx.get_solc_version()) != solc_version:
                if solc_version not in installed_version:
                    solcx.install_solc(solc_version)
                solcx.set_solc_version(solc_version, silent=True)
        elif installed_version == []:
            logging.info('Solc doesn\'t exist. Downloading and installing latest version')
            current_version = solcx.install_solc()
            solcx.set_solc_version(current_version, silent=True)
        
        return solcx.compile_files(source_files=source_files, output_values=['bin', 'abi'])

    @check_connection
    def deploy_contract(
        self,
        contract_bytecode: str,
        contract_abi: typing.List[typing.Dict[str, typing.Any]],
        *contract_args,
        value: int = 0,
        nonce: int = None,
        gas_price: int = None,
        account: LocalAccount = None,
        password: str = None,
        encrypted_key: typing.Dict[str, typing.Any] = None,
        private_key: str = None,
        **contract_kwargs
    ) -> typing.Dict[str, typing.Any]:
        global build_transaction

        if value < 0:
            raise ValueError('Value parameter must be non negative')

        if not (isinstance(account, (LocalAccount, Account)) or \
            (isinstance(password, str) and isinstance(encrypted_key, dict)) or \
            isinstance(private_key, str)):
            raise TypeError('At least "account" parameter or "private_key" or "password" and "encrypted_key" parameter must be provided')

        if not isinstance(account,(LocalAccount, Account)):
            if isinstance(password, str) and isinstance(encrypted_key, dict):
                account = self.get_account(password, encrypted_key)
            else:
                account = self.get_account_from_key(private_key)

        current_nonce = nonce or self.w3.eth.get_transaction_count(account.address)

        contract_args, contract_kwargs = self.parse_args(contract_args, contract_kwargs)
        constructor = self.w3.eth.contract(
            bytecode=contract_bytecode,
            abi=contract_abi
        ).constructor(
            *contract_args,
            **contract_kwargs
        )

        if not isinstance(gas_price, int):
            gas_price = self.w3.eth.gas_price

        try:
            transaction = getattr(constructor, build_transaction)({
                "from": account.address,
                "nonce": current_nonce,
                "value": value
            })
            gas_price = transaction['maxFeePerGas']
        except:
            transaction = getattr(constructor, build_transaction)({
                "from": account.address,
                "nonce": current_nonce,
                "value": value,
                "gasPrice": gas_price
            })

        total_gas = transaction['gas']

        account_balance = self.w3.eth.get_balance(account.address)

        total_cost = value + total_gas * gas_price

        if account_balance < total_cost:
            raise ValueError(str(total_cost - account_balance)+' minimum needed to be added to do transaction. Ask admin to send it to you.')

        signed_transaction = account.sign_transaction(transaction)

        transaction_hash = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        functions = self.parse_abi(contract_abi)

        payload = {
            'transaction_hash': transaction_hash.hex(),
            'methods': functions
        }

        return payload

    @check_connection
    def generate_deploy_contract_transaction(
        self,
        contract_bytecode: str,
        contract_abi: typing.List[typing.Dict[str, typing.Any]],
        *contract_args,
        value: int = 0,
        nonce: int = None,
        gas_price: int = None,
        account_address: str = None,
        **contract_kwargs
    ) -> typing.Dict[str, typing.Any]:
        global build_transaction

        if value < 0:
            raise ValueError('Value parameter must be non negative')

        if not isinstance(account_address, str):
            raise TypeError('"account_address" parameter must be provided')

        current_nonce = nonce or self.w3.eth.get_transaction_count(account_address)

        contract_args, contract_kwargs = self.parse_args(contract_args, contract_kwargs)
        constructor = self.w3.eth.contract(
            bytecode=contract_bytecode,
            abi=contract_abi
        ).constructor(
            *contract_args,
            **contract_kwargs
        )

        if not isinstance(gas_price, int):
            gas_price = self.w3.eth.gas_price

        try:
            transaction = getattr(constructor, build_transaction)({
                "from": account_address,
                "nonce": current_nonce,
                "value": value
            })
            gas_price = transaction['maxFeePerGas']
        except:
            transaction = getattr(constructor, build_transaction)({
                "from": account_address,
                "nonce": current_nonce,
                "value": value,
                "gasPrice": gas_price
            })

        total_gas = transaction['gas']

        account_balance = self.w3.eth.get_balance(account_address)

        total_cost = value + total_gas * gas_price

        if account_balance < total_cost:
            raise ValueError(str(total_cost - account_balance)+' minimum needed to be added to do transaction. Ask admin to send it to you.')

        return transaction

    @check_connection
    def estimate_deploy_contract_price(
        self,
        contract_bytecode: str,
        contract_abi: typing.List[typing.Dict[str, typing.Any]],
        *contract_args,
        value: int = 0,
        gas_price: int = None,
        account_address: str = None,
        **contract_kwargs
    ) -> typing.Dict[str, int]:
        global build_transaction

        if value < 0:
            raise ValueError('Value parameter must be non negative')
        
        if not isinstance(account_address, str):
            raise TypeError('"account_address" parameter must be provided')

        contract_args, contract_kwargs = self.parse_args(contract_args, contract_kwargs)
        constructor = self.w3.eth.contract(
            bytecode=contract_bytecode,
            abi=contract_abi
        ).constructor(
            *contract_args,
            **contract_kwargs
        )

        if not isinstance(gas_price, int):
            gas_price = self.w3.eth.gas_price

        try:
            transaction = getattr(constructor, build_transaction)({
                "from": account_address,
                "value": value
            })
            gas_price = transaction['maxFeePerGas']
        except:
            transaction = getattr(constructor, build_transaction)({
                "from": account_address,
                "value": value,
                "gasPrice": gas_price
            })

        total_gas = transaction['gas']

        return {'cost': total_gas*gas_price, 'value': value, 'total': total_gas*gas_price+value}

    @check_connection
    def get_contract_address(
        self,
        transaction_hash: str
    ) -> typing.Optional[str]:

        receipt = self.get_transaction_receipt(transaction_hash)

        return receipt.get('contractAddress', None)

    @check_connection
    def get_contract(
        self,
        contract_address: str,
        contract_abi: typing.List[typing.Dict[str, typing.Any]]
    ) -> Contract:

        if isinstance(contract_address, str) and isinstance(contract_abi, list):
            contract_address = self.parse_address(contract_address)
            return self.w3.eth.contract(address=contract_address, abi=contract_abi)
        raise TypeError('address parameter must be string and abi parameter must be list')
        
    @check_connection
    def contract_method(
        self,
        contract_method: str,
        *contract_args,
        contract: Contract = None,
        contract_address: str = None,
        contract_abi: typing.List[typing.Dict[str, typing.Any]] = None,
        value: int = 0,
        nonce: int = None,
        gas_price: int = None,
        account: LocalAccount = None,
        password: str = None,
        encrypted_key: typing.Dict[str, typing.Any] = None,
        private_key: str = None,
        **contract_kwargs
    ) -> TxData:
        global build_transaction

        if value < 0:
            raise ValueError('Value parameter must be non negative')
        
        if not (isinstance(contract, Contract) or (isinstance(contract_address, str) and isinstance(contract_abi, list))):
            raise TypeError('At least "contract" parameter or "contract_address" and "contract_abi" parameter must be provided')

        if not (isinstance(account, (LocalAccount, Account)) or \
            (isinstance(password, str) and isinstance(encrypted_key, dict)) or \
            isinstance(private_key, str)):
            raise TypeError('At least "account" parameter or "private_key" or "password" and "encrypted_key" parameter must be provided')

        if not isinstance(account,(LocalAccount, Account)):
            if isinstance(password, str) and isinstance(encrypted_key, dict):
                account = self.get_account(password, encrypted_key)
            else:
                account = self.get_account_from_key(private_key)

        current_nonce = nonce or self.w3.eth.get_transaction_count(account.address)

        if not isinstance(contract, Contract):
            contract = self.get_contract(contract_address, contract_abi)

        method = getattr(contract.functions, contract_method, False)
        if not method:
            raise MethodNotFound(contract_method+' method not found in contract')
        contract_args, contract_kwargs = self.parse_args(contract_args, contract_kwargs)
        constructor = method(*contract_args, **contract_kwargs)

        if not isinstance(gas_price, int):
            gas_price = self.w3.eth.gas_price

        try:
            transaction = getattr(constructor, build_transaction)({
                "from": account.address,
                "nonce": current_nonce,
                "value": value
            })
            gas_price = transaction['maxFeePerGas']
        except:
            transaction = getattr(constructor, build_transaction)({
                "from": account.address,
                "nonce": current_nonce,
                "value": value,
                "gasPrice": gas_price
            })

        total_gas = transaction['gas']

        account_balance = self.w3.eth.get_balance(account.address)

        total_cost = value + total_gas * gas_price

        if account_balance < total_cost:
            raise ValueError(str(total_cost - account_balance)+' minimum needed to be added to do transaction. Ask admin to send it to you.')

        signed_transaction = account.sign_transaction(transaction)

        transaction_hash = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        return self.get_transaction(transaction_hash)
    
    @check_connection
    def generate_contract_method_transaction(
        self,
        contract_method: str,
        *contract_args,
        contract: Contract = None,
        contract_address: str = None,
        contract_abi: typing.List[typing.Dict[str, typing.Any]] = None,
        value: int = 0,
        nonce: int = None,
        gas_price: int = None,
        account_address: str = None,
        **contract_kwargs
    ) -> typing.Dict[str, typing.Any]:
        global build_transaction

        if value < 0:
            raise ValueError('Value parameter must be non negative')
        
        if not (isinstance(contract, Contract) or (isinstance(contract_address, str) and isinstance(contract_abi, list))):
            raise TypeError('At least "contract" parameter or "contract_address" and "contract_abi" parameter must be provided')

        if not isinstance(account_address, str):
            raise TypeError('"account_address" parameter must be provided')

        current_nonce = nonce or self.w3.eth.get_transaction_count(account_address)

        if not isinstance(contract, Contract):
            contract = self.get_contract(contract_address, contract_abi)

        method = getattr(contract.functions, contract_method, False)
        if not method:
            raise MethodNotFound(contract_method+' method not found in contract')
        contract_args, contract_kwargs = self.parse_args(contract_args, contract_kwargs)
        constructor = method(*contract_args, **contract_kwargs)

        if not isinstance(gas_price, int):
            gas_price = self.w3.eth.gas_price

        try:
            transaction = getattr(constructor, build_transaction)({
                "from": account_address,
                "nonce": current_nonce,
                "value": value
            })
            gas_price = transaction['maxFeePerGas']
        except:
            transaction = getattr(constructor, build_transaction)({
                "from": account_address,
                "nonce": current_nonce,
                "value": value,
                "gasPrice": gas_price
            })

        total_gas = transaction['gas']

        account_balance = self.w3.eth.get_balance(account_address)

        total_cost = value + total_gas * gas_price

        if account_balance < total_cost:
            raise ValueError(str(total_cost - account_balance)+' minimum needed to be added to do transaction. Ask admin to send it to you.')

        return transaction

    @check_connection
    def contract_method_test(
        self,
        contract_method: str,
        *contract_args,
        contract: Contract = None,
        contract_address: str = None,
        contract_abi: typing.List[typing.Dict[str, typing.Any]] = None,
        value: int = 0,
        gas_price: int = None,
        account_address: str = None,
        **contract_kwargs
    ) -> typing.Literal[True]:

        if value < 0:
            raise ValueError('Value parameter must be non negative')

        if not (isinstance(contract, Contract) or (isinstance(contract_address, str) and isinstance(contract_abi, list))):
            raise TypeError('At least "contract" parameter or "contract_address" and "contract_abi" parameter must be provided')
        
        if not isinstance(account_address, str):
            raise TypeError('"account_address" parameter must be provided')

        if not isinstance(contract, Contract):
            contract = self.get_contract(contract_address, contract_abi)
        
        method = getattr(contract.functions, contract_method, False)
        if not method:
            raise MethodNotFound(contract_method+' method not found in contract')
        contract_args, contract_kwargs = self.parse_args(contract_args, contract_kwargs)
        constructor = method(*contract_args, **contract_kwargs)

        if not isinstance(gas_price, int):
            gas_price = self.w3.eth.gas_price
        
        try:
            gas = constructor.estimateGas({
                "from": account_address,
                "value": value
            })

            constructor.call({
                "from": account_address,
                "value": value,
                "gas": gas
            })
        except:
            gas = constructor.estimateGas({
                "from": account_address,
                "value": value,
                "gasPrice": gas_price
            })

            constructor.call({
                "from": account_address,
                "value": value,
                "gas": gas,
                "gasPrice": gas_price
            })

        return True

    @check_connection
    def estimate_contract_method_price(
        self,
        contract_method: str,
        *contract_args,
        contract: Contract = None,
        contract_address: str = None,
        contract_abi: typing.List[typing.Dict[str, typing.Any]] = None,
        value: int = 0,
        gas_price: int = None,
        account_address: str = None,
        **contract_kwargs
    ) -> typing.Dict[str, int]:
        global build_transaction

        if value < 0:
            raise ValueError('Value parameter must be non negative')

        if not (isinstance(contract, Contract) or (isinstance(contract_address, str) and isinstance(contract_abi, list))):
            raise TypeError('At least "contract" parameter or "contract_address" and "contract_abi" parameter must be provided')
        
        if not isinstance(account_address, str):
            raise TypeError('"account_address" parameter must be provided')

        if not isinstance(contract, Contract):
            contract = self.get_contract(contract_address, contract_abi)
        
        method = getattr(contract.functions, contract_method, False)
        if not method:
            raise MethodNotFound(contract_method+' method not found in contract')
        contract_args, contract_kwargs = self.parse_args(contract_args, contract_kwargs)
        constructor = method(*contract_args, **contract_kwargs)

        if not isinstance(gas_price, int):
            gas_price = self.w3.eth.gas_price
        
        try:
            transaction = getattr(constructor, build_transaction)({
                "from": account_address,
                "value": value
            })
            gas_price = transaction['maxFeePerGas']
        except:
            transaction = getattr(constructor, build_transaction)({
                "from": account_address,
                "value": value,
                "gasPrice": gas_price
            })

        total_gas = transaction['gas']

        return {'cost': total_gas*gas_price, 'value': value, 'total': total_gas*gas_price+value}

    @check_connection
    def contract_call(
        self,
        contract_method: str,
        *contract_args,
        contract: Contract = None,
        contract_address: str = None,
        contract_abi: typing.List[typing.Dict[str, typing.Any]] = None,
        **contract_kwargs
    ) -> typing.Any:

        if not (isinstance(contract, Contract) or (isinstance(contract_address, str) and isinstance(contract_abi, list))):
            raise TypeError('At least "contract" parameter or "contract_address" and "contract_abi" parameter must be provided')

        if not isinstance(contract, Contract):
            contract = self.get_contract(contract_address, contract_abi)

        method = getattr(contract.functions, contract_method, False)
        if not method:
            raise MethodNotFound(contract_method+' method not found in contract')
        contract_args, contract_kwargs = self.parse_args(contract_args, contract_kwargs)
        constructor = method(*contract_args, **contract_kwargs)

        return constructor.call()

    @check_connection
    def parse_contract_event_log(
        self,
        event_name: str,
        transaction_hash: str,
        *,
        contract: Contract = None,
        contract_address: str = None,
        contract_abi: typing.List[typing.Dict[str, typing.Any]] = None
    ) -> typing.List[AttributeDict]:

        if not (isinstance(contract, Contract) or (isinstance(contract_address, str) and isinstance(contract_abi, list))):
            raise TypeError('At least "contract" parameter or "contract_address" and "contract_abi" parameter must be provided')

        if not isinstance(contract, Contract):
            contract = self.get_contract(contract_address, contract_abi)

        event = getattr(contract.events, event_name, False)
        if not event:
            raise EventNotFound(event_name+' event not fount in contract')
        receipt = self.get_transaction_receipt(transaction_hash)
        event_log = event().processReceipt(receipt, errors=DISCARD)

        return list(event_log)

    @check_connection
    def cancel_transaction(
        self,
        transaction_hash: typing.Union[HexBytes, str],
        account: LocalAccount = None,
        password: str = None,
        encrypted_key: typing.Dict[str, typing.Any] = None,
        private_key: str = None
    ) -> TxData:

        try:
            self.w3.eth.get_transaction_receipt(transaction_hash)
            raise ValueError('Transaction status is already mined')
        except TransactionNotFound:
            pass
    
        if not (isinstance(account, (LocalAccount, Account)) or \
            (isinstance(password, str) and isinstance(encrypted_key, dict)) or \
            isinstance(private_key, str)):
            raise TypeError('At least "account" parameter or "private_key" or "password" and "encrypted_key" parameter must be provided')

        if not isinstance(account,(LocalAccount, Account)):
            if isinstance(password, str) and isinstance(encrypted_key, dict):
                account = self.get_account(password, encrypted_key)
            else:
                account = self.get_account_from_key(private_key)

        old_transaction = self.get_transaction(transaction_hash)

        if old_transaction['from'] != account.address:
            raise UserError('Transaction sender is not match with current sender')

        account_balance = self.w3.eth.get_balance(account.address)

        total_cost = 21000 * (old_transaction['gasPrice'] + 1)

        if account_balance < total_cost:
            raise ValueError(str(total_cost - account_balance)+' minimum needed to be added to do transaction. Ask admin to send it to you.')
        
        new_transaction = {
            'from': account.address,
            'to': account.address,
            'value': 0,
            'nonce': old_transaction['nonce'],
            'gas': 21000,
            'gasPrice': old_transaction['gasPrice'] + 1,
            'chainId': self.w3.eth.chain_id
        }

        signed_transaction = account.sign_transaction(new_transaction)

        transaction_hash = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        return self.get_transaction(transaction_hash)

    @check_connection
    def estimate_cancel_transaction_price(
        self,
        transaction_hash: typing.Union[HexBytes, str],
    ) -> typing.Dict[str, int]:

        try:
            self.w3.eth.get_transaction_receipt(transaction_hash)
            raise ValueError('Transaction status is already mined')
        except TransactionNotFound:
            pass

        old_transaction = self.get_transaction(transaction_hash)

        total_gas = 21000

        gas_price = old_transaction['gasPrice'] + 1

        return {'cost': total_gas*gas_price, 'value': 0, 'total': total_gas*gas_price}

    @check_connection
    def sign_transaction_as_typed_data(
        self,
        domain_name: str,
        domain_version: str,
        verifying_contract: str,
        transaction: typing.Dict[str, typing.Any],
        domain_chain_id: int = None,
        account: LocalAccount = None,
        password: str = None,
        encrypted_key: typing.Dict[str, typing.Any] = None,
        private_key: str = None,
    ) -> HexBytes:
        
        if any([i not in transaction for i in ['from', 'to', 'nonce', 'gas']]):
            raise TypeError('At least transaction must contains "from", "to", "nonce", and "gas" field')

        if not (isinstance(account, (LocalAccount, Account)) or \
            (isinstance(password, str) and isinstance(encrypted_key, dict)) or \
            isinstance(private_key, str)):
            raise TypeError('At least "account" parameter or "private_key" or "password" and "encrypted_key" parameter must be provided')

        if not isinstance(domain_chain_id, int):
            domain_chain_id = transaction.get('chainId', self.w3.eth.chain_id)

        if not isinstance(account,(LocalAccount, Account)):
            if isinstance(password, str) and isinstance(encrypted_key, dict):
                account = self.get_account(password, encrypted_key)
            else:
                account = self.get_account_from_key(private_key)

        data = {
            'types': {
                'EIP712Domain': [
                    { 'name': 'name', 'type': 'string' },
                    { 'name': 'version', 'type': 'string' },
                    { 'name': 'chainId', 'type': 'uint256' },
                    { 'name': 'verifyingContract', 'type': 'address' },
                ],
                'ForwardRequest': [
                    { 'name': 'from', 'type': 'address' },
                    { 'name': 'to', 'type': 'address' },
                    { 'name': 'value', 'type': 'uint256' },
                    { 'name': 'gas', 'type': 'uint256' },
                    { 'name': 'nonce', 'type': 'uint256' },
                    { 'name': 'data', 'type': 'bytes' }
                ]
            },
            'primaryType': 'ForwardRequest',
            'domain': {
                'name': domain_name,
                'version': domain_version,
                'chainId': domain_chain_id,
                'verifyingContract': verifying_contract,
            },
            'message': {
                'from': transaction['from'],
                'to': transaction['to'],
                'value': transaction.get('value', 0),
                'gas': transaction['gas'],
                'nonce': transaction['nonce'],
                'data': bytes.fromhex(transaction.get('data', '0x')[2:])
            }
        }

        signable_data = encode_structured_data(data)

        signed_data = account.sign_message(signable_data)

        return signed_data.signature
    
    @check_connection
    def forward_signed_transaction(
        self,
        transaction: typing.Dict[str, typing.Any],
        signature: typing.Union[str, HexBytes],
        contract: Contract = None,
        contract_address: str = None,
        contract_abi: typing.List[typing.Dict[str, typing.Any]] = None,
        forwarder_method: str = 'execute',
        nonce: int = None,
        gas_price: int = None,
        account: LocalAccount = None,
        password: str = None,
        encrypted_key: typing.Dict[str, typing.Any] = None,
        private_key: str = None,
    ) -> TxData:
        
        if any([i not in transaction for i in ['from', 'to', 'nonce', 'gas']]):
            raise TypeError('At least transaction must contains "from", "to", "nonce", and "gas" field')

        transaction['value'] = transaction.get('value', 0)
        transaction['data'] = transaction.get('data', '0x')
        
        if not (isinstance(contract, Contract) or (isinstance(contract_address, str) and isinstance(contract_abi, list))):
            raise TypeError('At least "contract" parameter or "contract_address" and "contract_abi" parameter must be provided')

        if not (isinstance(account, (LocalAccount, Account)) or \
            (isinstance(password, str) and isinstance(encrypted_key, dict)) or \
            isinstance(private_key, str)):
            raise TypeError('At least "account" parameter or "private_key" or "password" and "encrypted_key" parameter must be provided')

        if not isinstance(account,(LocalAccount, Account)):
            if isinstance(password, str) and isinstance(encrypted_key, dict):
                account = self.get_account(password, encrypted_key)
            else:
                account = self.get_account_from_key(private_key)
        
        current_nonce = nonce or self.w3.eth.get_transaction_count(account.address)

        if not isinstance(contract, Contract):
            contract = self.get_contract(contract_address, contract_abi)
        
        method = getattr(contract.functions, forwarder_method, False)
        if not method:
            raise MethodNotFound(forwarder_method+' method not found in forwarder contract')
        contract_args, contract_kwargs = self.parse_args(contract_args, contract_kwargs)
        constructor = method(
            req={k:transaction[k] for k in ['from', 'to', 'value', 'gas', 'nonce', 'data']},
            signature=signature
        )

        if not isinstance(gas_price, int):
            gas_price = self.w3.eth.gas_price

        try:
            forward_transaction = getattr(constructor, build_transaction)({
                "from": account.address,
                "nonce": current_nonce
            })
            gas_price = transaction['maxFeePerGas']
        except:
            forward_transaction = getattr(constructor, build_transaction)({
                "from": account.address,
                "nonce": current_nonce,
                "gasPrice": gas_price
            })
        
        forward_transaction['gas'] = forward_transaction['gas'] + transaction['gas']

        total_gas = forward_transaction['gas']

        account_balance = self.w3.eth.get_balance(account.address)

        total_cost = total_gas * gas_price

        if account_balance < total_cost:
            raise ValueError(str(total_cost - account_balance)+' minimum needed to be added to do transaction.')

        signed_transaction = account.sign_transaction(forward_transaction)

        transaction_hash = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        return self.get_transaction(transaction_hash)
    
    @check_connection
    def get_transaction(
        self,
        transaction_hash: typing.Union[HexBytes, str]
    ) -> TxData:

        return self.w3.eth.get_transaction(transaction_hash)

    @check_connection
    def get_transaction_receipt(
        self,
        transaction_hash: typing.Union[HexBytes, str],
        timeout: int = 5
    ) -> TxReceipt:

        return self.w3.eth.wait_for_transaction_receipt(transaction_hash, timeout)
    
    @check_connection
    def get_block(
        self,
        block_identifier: BlockIdentifier,
        full_transactions: bool = False
    ) -> BlockData:
    
        return self.w3.eth.get_block(block_identifier, full_transactions)