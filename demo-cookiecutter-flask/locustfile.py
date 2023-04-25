from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        headers = {
            "user-agent": "my-app/0.0.1",
            "sentry-trace": "1234567890abcdef1234567890abcdef-1234567890abcdef-1",
        }

        self.client.get("/")
        self.client.get("/about/", headers=headers)
        self.client.get("/users/", headers=headers)
        self.client.get("/register/", headers=headers)
