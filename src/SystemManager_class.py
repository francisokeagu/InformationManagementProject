class SystemManager:

    def __init__(self, logfile="app.log"):
      """
      Initialize the SystemManager.

      Args:
          logfile (str): Path to the log file.
      """
      self.logfile = logfile
      # Set up the logger immediately
      self.setup_logger()


    def setup_logger(logfile="app.log"):
    """Configure and initialize logging for the application."""
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Logger initialized successfully.")


    def validate_input(data):
    """Ensure dataset structure and required columns are valid."""
    if data is None or data.empty:
        logging.error("Validation failed: Data is empty.")
        return False

    required_cols = ["user_id", "title", "checkout_date"]
    missing = [c for c in required_cols if c not in data.columns]
    if missing:
        logging.error(f"Missing required columns: {missing}")
        return False

    logging.info("Data validation passed.")

    return True


