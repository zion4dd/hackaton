from pyfcm import FCMNotification

from config import settings


class FireBase:
    def __init__(self) -> None:
        self.push_service = FCMNotification(api_key=settings.FBTOKEN)

    def push(self, registration_id=None, body="empty message"):
        try:
            result = self.push_service.notify_single_device(
                registration_id=registration_id,
                message_body=body,
                sound="default",
            )
            print(result)

        except Exception:
            print("ERR: push failed")
