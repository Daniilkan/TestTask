from app.clients.crm import CRMManager

class CRMTasks:
    def __init__(self):
        self.crm_manager = CRMManager()

    def send_premium(self, products):
        title = "Top 5 Premium Products"
        description = "\n".join([f"{p.art} - {p.name} - {p.price} - {p.url}" for p in products])
        return self.crm_manager.create_task(title, description)

    def send_budget(self, products):
        title = "Top 5 Budget Products"
        description = "\n".join([f"{p.art} - {p.name} - {p.price} - {p.url}" for p in products])
        return self.crm_manager.create_task(title, description)