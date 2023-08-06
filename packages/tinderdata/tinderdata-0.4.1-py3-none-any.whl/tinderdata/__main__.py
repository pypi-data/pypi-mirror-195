"""
Running the tool from the commandline, if it is installed in your environment.
"""
import typer

from tinderdata.tinder import TinderData
from tinderdata.utils import set_logger_level

app = typer.Typer()


@app.command()
def analyze(
    data_path: str = typer.Argument(
        None, help="Location, relative or absolute, of the exported JSON file with your user data.",
    ),
    show_figures: bool = typer.Option(
        False, help="Whether or not to show figures when plotting insights."
    ),
    save_figures: bool = typer.Option(
        False, help="Whether or not to save figures when plotting insights."
    ),
    log_level: str = typer.Option(
        "info",
        help="The base console logging level. Can be 'debug', 'info', 'warning' and 'error'.",
    ),
) -> None:
    """Get insight on your Tinder usage."""
    set_logger_level(log_level)

    tinder = TinderData(data_path)
    tinder.check_plot_dir()

    logger.info("Plotting insights on messages")
    tinder.plot_messages_loyalty(showfig=show_figures, savefig=save_figures)
    tinder.plot_messages_monthly_stats(showfig=show_figures, savefig=save_figures)
    tinder.plot_messages_weekday_stats(showfig=show_figures, savefig=save_figures)

    logger.info("Plotting insights on swipes")
    tinder.plot_swipes_monthly_stats(showfig=show_figures, savefig=save_figures)
    tinder.plot_swipes_monthly_relative_stats(showfig=show_figures, savefig=save_figures)
    tinder.plot_swipes_weekday_stats(showfig=show_figures, savefig=save_figures)
    tinder.plot_swipes_weekday_relative_stats(showfig=show_figures, savefig=save_figures)

    logger.info("Displaying usage statistics")
    tinder.output_usage_statistics()
    tinder.output_swipes_statistics()
    tinder.output_success_statistics()
    tinder.output_message_statistics()
    tinder.output_sankey_string()


if __name__ == "__main__":
    app()
