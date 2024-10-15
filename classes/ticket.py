class Ticket:
    def __init__(self, Id, LocalRequestId, DateTimeLastRead, Subject, Priority, Status, Requester, Agent, DateTimeCreated, DateTimeUpdated, SlaResponseOverdue, SlaResolutionOverdue, RequestTypeName, NextSlaDueDateTime, NextSlaOverdue, NextSlaPaused):
        self.id = Id
        self.local_request_id = LocalRequestId
        # self.datetime_last_read = DateTimeLastRead
        self.subject = Subject
        self.priority = Priority
        self.status = Status
        self.requester = Requester
        # self.agent = Agent
        self.datetime_created = DateTimeCreated
        self.datetime_updated = DateTimeUpdated
        # self.sla_response_overdue = SlaResponseOverdue
        # self.sla_resolution_overdue = SlaResolutionOverdue
        # self.request_type_name = RequestTypeName
        # self.next_sla_due_datetime = NextSlaDueDateTime
        # self.next_sla_overdue = NextSlaOverdue
        # self.next_sla_paused = NextSlaPaused