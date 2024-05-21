import BinanceDataReceiver
import ConfigurationReader

def main():
    ConfigurationReader.loadConfig("configuration.json")
    print(ConfigurationReader.get("interval"))
    dataReceiver = BinanceDataReceiver.BinanceDataReceiver()
    dataReceiver.start()

if __name__ == "__main__":
    main()