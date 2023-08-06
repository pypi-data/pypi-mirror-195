#   -*- coding: utf-8 -*-
#
#   This file is part of config-controller
#
#   Copyright (C) 2021-Present SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

from os.path import dirname, join
from typing import Dict

from predeployed_generator.contract_generator import ContractGenerator


class ContextGenerator(ContractGenerator):
    '''Generates Context
    '''

    ARTIFACT_FILENAME = 'Context.json'
    META_FILENAME = 'Context.meta.json'

    def __init__(self):
        generator = ContextGenerator.from_hardhat_artifact(
            join(dirname(__file__), 'artifacts', self.ARTIFACT_FILENAME),
            join(dirname(__file__), 'artifacts', self.META_FILENAME))
        deprecated_bytecode = "0x608060405234801561001057600080fd5b506004361061005e576000357c01000000000000000000000000000000000000000000000000000000009004806315cd7a2d1461006357806367091a01146100e657806383e781fe1461012a575b600080fd5b61006b610174565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156100ab578082015181840152602081019050610090565b50505050905090810190601f1680156100d85780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b610128600480360360208110156100fc57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610216565b005b6101326102b2565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b606060018054600181600116156101000203166002900480601f01602080910402602001604051908101604052809291908181526020018280546001816001161561010002031660029004801561020c5780601f106101e15761010080835404028352916020019161020c565b820191906000526020600020905b8154815290600101906020018083116101ef57829003601f168201915b5050505050905090565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161461026f57600080fd5b806000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1690509056fea165627a7a723058203d58598dee9113d96d02a8821205cf2af6e04d52d4d3b52f4563f77936acb5490029"
        super().__init__(bytecode=deprecated_bytecode, abi=generator.abi, meta=generator.meta)

    @classmethod
    def generate_storage(cls, **kwargs) -> Dict[str, str]:
        schain_owner = kwargs['schain_owner']
        schain_name = kwargs['schain_name']
        storage: Dict[str, str] = {}
        cls._write_address(storage, 0, schain_owner)
        cls._write_string(storage, 1, schain_name)
        return storage
