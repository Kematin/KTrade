from config import Settings


def create_paths(config: Settings):
    config.image.directory.mkdir(parents=True, exist_ok=True)
