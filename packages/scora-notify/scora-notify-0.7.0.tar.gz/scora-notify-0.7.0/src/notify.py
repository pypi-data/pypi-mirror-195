from slack_sdk import WebClient

import logging


USER_ICON = ':fire:'
UPDATE_ICON = ':recycle:'
SUCCESS_ICON = ':white_check_mark:'
ERROR_ICON = ':x:'
SKIP_ICON = ':fast_forward:'
ENV_ICON = ':hocho:'


HEADER_MSGS = {
    'start': f'{UPDATE_ICON} Executando...',
    'success': f'{SUCCESS_ICON} Sucesso',
    'error': f'{ERROR_ICON} Erro'
}

class Notify():
    def __init__(self, slack_token, slack_channel, step, tenant="", project="", enable_slack_notifications=True):
        """Initializes the slack notifier

        Args:
            slack_token (str): Slack API token.
            slack_channel (str): Name of the slack channel to be used.
            step (str): Step name.
            tenant (str): Tenant name.
            project (str): Project name.
            enable_slack_notifications (bool, optional): Whether to enable notifications \
                or not. Defaults to True.
        """
        self.SLACK_TOKEN = slack_token
        self.ENABLE_SLACK_NOTIFICATIONS = enable_slack_notifications
        self.SLACK_CHANNEL = slack_channel
        self.STEP = step
        self.PROJECT = project
        self.TENANT = tenant
        self.SLACK_THREAD_TS = None
        self.SLACK_CHANNEL_ID = None
        
    def is_slack_enabled(self):
        return (
            self.SLACK_TOKEN and self.SLACK_TOKEN!='' and self.ENABLE_SLACK_NOTIFICATIONS
        )
        
    def get_title(self, step, tenant, project, msg_type):
        tenant_string = f'[{tenant}]' if tenant else ""
        project_string = f'[{project}]' if project else ""
        return [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f'{tenant_string} {project_string} {step} - {HEADER_MSGS[msg_type]}',
                    "emoji": True
                }
            }
        ]

    def start(self):
        logging.info(f"[Notify:start] Start of [{self.STEP}]")
        
        if self.is_slack_enabled():
            
            client = WebClient(token=self.SLACK_TOKEN)
            title = self.get_title(self.STEP,self.TENANT,self.PROJECT, 'start')
            response = client.chat_postMessage(
                channel= self.SLACK_CHANNEL,
                blocks= title,
                icon_emoji= USER_ICON,
                text=title[0]["text"]["text"]
            )
            
            self.SLACK_THREAD_TS = response.get("ts")
            self.SLACK_CHANNEL_ID = response.get("channel")



    def add_env_config(self, logging_config):
        self.add_update(logging_config, ENV_ICON)


    def add_update(self,message, icon=UPDATE_ICON):
        logging.info(f"[Notify:update]: {message}")

        if self.is_slack_enabled() and self.SLACK_THREAD_TS:
            client = WebClient(token=self.SLACK_TOKEN)
            client.chat_postMessage(
                channel= self.SLACK_CHANNEL,
                text= message,
                icon_emoji= icon,
                thread_ts= self.SLACK_THREAD_TS
            )


    def finish(self,success=False):
        logging.info(f"[Notify:finish] Finish of [{self.STEP}]")

        if self.is_slack_enabled():
            msg_type = 'success' if success else 'error'
            title=self.get_title(self.STEP, self.TENANT, self.PROJECT, msg_type)
            client = WebClient(token=self.SLACK_TOKEN)
            client.chat_update(
                channel= self.SLACK_CHANNEL_ID,
                ts= self.SLACK_THREAD_TS,
                blocks= title,
                icon_emoji= USER_ICON,
                text=title[0]["text"]["text"]
            )

