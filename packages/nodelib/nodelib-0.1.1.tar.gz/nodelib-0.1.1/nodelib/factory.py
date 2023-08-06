import logging
from .bsc import BscNode
from .ether import EtherNode
from .tron import TronNode
from .exceptions import UnknownApi
from .interface import INode

logger = logging.getLogger('nodes.factory')


class NodeFactory(object):
    def build_node(self, node_id: str, api: str, uri: str, provider: str, **kwargs) -> INode:
        logger.info('[%s] Building node %s from %s', api, node_id, provider)

        if api == 'web3.eth':
            return EtherNode(uri=uri, chain_id=kwargs['chain_id'])
        elif api == 'web3.bsc':
            return BscNode(uri=uri, chain_id=kwargs['chain_id'])
        elif api == 'tronpy':
            return TronNode(uri=uri)
        else:
            raise UnknownApi(api)
