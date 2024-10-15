class Comment:
    def __init__(self, Id, ThreadId, ThreadType, DateTimeCreated, DateTimeUtc, RequestId, BodyText, AgentId, AgentName, FromEmail, FromName, SystemTriggered, TimeTrackingSeconds, LocalRequestId):
        self.id = Id
        self.requestid = RequestId
        self.threadid = ThreadId
        self.threadtype = ThreadType
        self.agentname = AgentName
        self.bodytext = BodyText
        self.datetime_created = DateTimeCreated
        self.fromemail= FromEmail
        self.fromname= FromName
        self.localrequestid = LocalRequestId