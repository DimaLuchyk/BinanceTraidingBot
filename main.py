import BinanceDataReceiver
import ConfigurationReader
import logging

def main():
    # Configure the logging settings
    logging.basicConfig(
        level=logging.DEBUG,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Set the log format
        datefmt='%Y-%m-%d %H:%M:%S',  # Set the date format
        handlers=[
            logging.FileHandler("my_log_file.log"),  # Log to a file
            #logging.StreamHandler()  # Optionally log to the console as well
        ]
    )

    ConfigurationReader.loadConfig("configuration.json")

    dataReceiver = BinanceDataReceiver.BinanceDataReceiver()
    dataReceiver.start()

if __name__ == "__main__":
    main()