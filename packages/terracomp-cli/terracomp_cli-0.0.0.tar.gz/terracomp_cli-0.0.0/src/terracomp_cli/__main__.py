from terracomp_typer import build_app_from_module


def main() -> None:
    app = build_app_from_module(
        module_name="terracomp_cli.commands", typer_options=dict(no_args_is_help=True, rich_markup_mode="rich")
    )
    app()


if __name__ == "__main__":
    main()
