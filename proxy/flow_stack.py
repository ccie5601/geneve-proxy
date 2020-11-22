"""FlowStack module."""

class Flow:
    """Flow class."""

    DIR_INBOUND = 0
    DIR_OUTBOUND = 1

    def __init__(
        self,
        cookie,
        direction_allowed,
        transport_allowed,
        application_allowed,
        direction
    ):
        """Construct a new Flow."""
        self.cookie = cookie
        self.direction_allowed = direction_allowed
        self.transport_allowed = transport_allowed
        self.application_allowed = application_allowed
        self.direction = direction

    def is_allowed(self):
        """
        Return whether a Flow is allowed.

        None: undetermined
        False: not allowed
        True: allowed
        """
        if (
            self.direction_allowed and
            self.transport_allowed and
            self.application_allowed
        ):
            return True
        elif (
            self.direction_allowed is False or
            self.transport_allowed is False or
            self.application_allowed is False
        ):
            return False

        return None

    def dir_string(self):
        """Return a string representation of this flow's direction."""
        dir_string = 'Unknown'
        if self.direction == self.DIR_INBOUND:
            dir_string = 'Inbound'
        elif self.direction == self.DIR_OUTBOUND:
            dir_string = 'Outbound'
        return dir_string

    def __repr__(self):
        """Return a string representation of this Flow."""
        return (
            f'Flow with direction {self.dir_string()}. '
            f'Direction allowed: {self.direction_allowed}. '
            f'Transport allowed: {self.transport_allowed}, '
            f'Application port allowed: {self.application_allowed}'
        )

class FlowStack:
    """FlowStack class."""

    stack = {}

    def __init__(self, max_size = 1024):
        """Construct a new FlowStack."""
        self.max_size = max_size

    def set_flow(
        self,
        cookie,
        direction_allowed = None,
        transport_allowed = None,
        application_allowed = None,
        direction = None,
    ):
        """Push a new flow onto the stack or update an existing flow."""
        flow = self.get_flow(cookie)
        if flow is None:
            flow = Flow(
                cookie, direction_allowed, transport_allowed, application_allowed, direction
            )
        else:
            if direction_allowed is not None:
                flow.direction_allowed = direction_allowed
            if transport_allowed is not None:
                flow.transport_allowed = transport_allowed
            if application_allowed is not None:
                flow.application_allowed = application_allowed
            if direction is not None:
                flow.direction = direction

        self.stack[cookie] = flow
        self.trim_stack()
        return flow

    def get_flow(self, cookie):
        """Return the flow's status if it exists, None if it doesn't."""
        try:
            return self.stack[cookie]
        except KeyError:
            return None

    def trim_stack(self):
        """Drop the oldest flows to resize the stack to max size."""
        if len(self.stack) > self.max_size:
            self.stack = self.stack[-self.max_size:]
