from ..endpoints import GenericPluralEndpoint


class TicketsEndPoint(GenericPluralEndpoint):
    def __init__(self, request_service):
        super(TicketsEndPoint, self).__init__(request_service)
        self._endpoint = "/api/v2/tickets"
        self.plural_resource_key = "tickets"
        self.single_resource_key = "ticket"
