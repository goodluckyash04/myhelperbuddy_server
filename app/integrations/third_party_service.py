from app.utils.api_client import APIClient

# Example: Using API client for a third-party service
class ThirdPartyService:
    def __init__(self):
        self.client = APIClient(base_url="https://api.example.com")

    async def fetch_users(self):
        """Get user data from external API."""
        return await self.client.get("/users")

    async def create_user(self, user_data):
        """Create a new user in external API."""
        return await self.client.post("/users", data=user_data)

'''
service = ThirdPartyService()
return await service.fetch_users()
'''
