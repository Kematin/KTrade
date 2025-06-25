MODELS = ["models.table:Item"]


def register_models(base):
    for model_path in MODELS:
        module_path, class_name = model_path.split(":")
        module = __import__(module_path, fromlist=[class_name])
        model_class = getattr(module, class_name)
