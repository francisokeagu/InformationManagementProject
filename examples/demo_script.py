""" TO TEST CORE FUNCTIONS """

from src.library_name import setup_logger, load_library_data, validate_input, create_report

def main():
    setup_logger()
    data = load_library_data("data/sample_data.csv")

    if validate_input(data):
        report = create_report(data)
        print("\n📊 Library Report Summary:")
        for key, value in report.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()


""" TEST COMPLETE """ 
