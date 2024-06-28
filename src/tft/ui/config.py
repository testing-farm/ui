from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="TF_UI",
    settings_files=["settings.yaml"],
    environments=True,
)
