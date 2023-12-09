class ResData:
    def __init__(self, data):
        self.block_number = data.get("block_number")
        self.confirmed = data.get("confirmed")
        self.content_uri = self.process_content_uri(data.get("content_uri"))
        self.created_at = data.get("created_at")
        self.creator_address = data.get("creator_address")
        self.owner_address = data.get("owner_address")
        self.trx_hash = data.get("trx_hash")
        self.id = data.get("id")
        self.position = data.get("position")
        self.category = data.get("category")
        self.mtype = data.get("mtype")
        self.internal_trx_index = data.get("internal_trx_index")
        self.network_id = data.get("network_id")

        self.brc20_command_data = data.get("brc20_command", {})
        
        if self.brc20_command_data:
            self.brc20_reason = self.brc20_command_data.get("reason")
            self.brc20_is_valid = self.brc20_command_data.get("is_valid")
        else:
            self.brc20_reason = None
            self.brc20_is_valid = None

    def process_content_uri(self, content_uri):
        # 将 \\ 替换为 0
        return content_uri.replace("\\", "0")

    def __str__(self):
        return (f"Inscription(trx_hash={self.trx_hash}, "
               f"creator_address={self.creator_address}, "
               f"position={self.position}, "
               f"content_uri={self.content_uri}, "
               f"brc20_is_valid={self.brc20_is_valid}) "
               
               )

