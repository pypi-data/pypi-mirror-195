import json
import base64
from pathlib import Path
from typing import Optional

from ._base import BaseAsyncAPI, sync_bind
from ..wallet import Wallet
from .tx import CreateTxOptions
from terra_proto.cosmwasm.wasm.v1 import AccessType
from paloma_sdk.core.wasm.data import AccessConfig
from paloma_sdk.core.wasm import MsgInstantiateContract, MsgExecuteContract, MsgStoreCode
from paloma_sdk.core.scheduler import MsgCreateJob, MsgExecuteJob
from paloma_sdk.core.coins import Coins
from paloma_sdk.core.broadcast import BlockTxBroadcastResult
from paloma_sdk.util.contract import read_file_as_b64

__all__ = ["AsyncJobSchedulerAPI", "JobSchedulerAPI"]


class AsyncJobSchedulerAPI(BaseAsyncAPI):
    async def create_job(
        self,
        wallet: Wallet,
        job_id: str,
        contract_address: str,
        abi: dict,
        payload: str,
        chain_type: str,
        chain_reference_id: str
    ) -> BlockTxBroadcastResult:
        """create job
        """
        definition = {"abi":json.dumps(abi, separators=[",", ":"]),"address":contract_address}
        definition_bytes = json.dumps(definition, separators=[",", ":"])
        payload_bytes = json.dumps({"hexPayload": payload}, separators=[",", ":"])
        create_tx = await wallet.create_and_sign_tx(
            CreateTxOptions(
                msgs=[
                    MsgCreateJob(wallet.key.acc_address, {
                        "id": job_id,
                        "owner": "",
                        "routing": {
                            "chain_type": chain_type,
                            "chain_reference_id": chain_reference_id
                        },
                        "definition": definition_bytes,
                        "payload": payload_bytes,
                        "is_payload_modifiable": True,
                        "permissions": {
                            "whitelist": [],
                            "blacklist": []
                        },
                        "triggers": [],
                        "address": ""
                    })
                ]
            )
        )
        create_tx_result = await self._c.tx.broadcast(create_tx)
        return create_tx_result

    async def execute_job(
        self,
        wallet: Wallet,
        job_id: str,
        payload: str,
    ) -> BlockTxBroadcastResult:
        """execute job
        """
        execute_tx = await wallet.create_and_sign_tx(
            CreateTxOptions(
                msgs=[
                    MsgExecuteJob(wallet.key.acc_address, job_id, json.dumps({"hexPayload": payload}, separators=[",", ":"]))
                ]
            )
        )
        create_tx_result = await self._c.tx.broadcast(execute_tx)
        return create_tx_result


class JobSchedulerAPI(AsyncJobSchedulerAPI):
    @sync_bind(AsyncJobSchedulerAPI.create_job)
    def create_job(
        self,
        wallet: Wallet,
        job_id: str,
        contract_address: str,
        abi: dict,
        payload: str,
        chain_type: str,
        chain_reference_id: str
    ) -> BlockTxBroadcastResult:
        pass

    @sync_bind(AsyncJobSchedulerAPI.execute_job)
    def execute_job(
        self,
        wallet: Wallet,
        job_id: str,
        payload: str,
    ) -> BlockTxBroadcastResult:
        pass

    create_job.__doc__ = AsyncJobSchedulerAPI.create_job.__doc__
    execute_job.__doc__ = AsyncJobSchedulerAPI.execute_job.__doc__
