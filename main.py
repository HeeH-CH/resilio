import truststore


class Entrypoint:
    """CLI entrypoint for the Resilio app."""

    def run(self) -> None:
        truststore.inject_into_ssl()
        from resilio.app import ResilioApp

        app = ResilioApp()
        app.run()


if __name__ == "__main__":
    Entrypoint().run()
