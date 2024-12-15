# Multi Keyword Spider

![image](https://github.com/user-attachments/assets/85692117-bca5-46eb-8869-a62a6b95f023)

## Overview
The **Multi_Keyword Spider** is a web scraping tool built using Scrapy. It is designed to crawl websites, identify specified keywords across pages, and categorize them. The results are saved in a structured Excel file, making it a versatile tool for keyword detection and web data analysis.

This tool is robust against interruptions, avoids redundant URL crawling, and ensures all crawled data is saved, even in case of unexpected script termination.

---

## Features
- Crawls websites from a CSV file containing administrator details.
- Detects and categorizes keywords such as "NIST," "ISO-27001," "SOC," "GDPR," etc.
- Saves results with details like raw keywords found, standardized keywords, and error comments (if any).
- Prevents redundant crawling by maintaining a record of visited URLs.
- Handles interruptions (e.g., `CTRL+C`) and saves crawled data before exiting.
- Skips non-text responses, optimizing the crawling process.
- Provides detailed logging of activities.

---

## Business Use Case
This tool can be utilized by organizations to:
- Audit and analyze the compliance status of websites.
- Identify specific compliance keywords for reporting and assessment.
- Automate manual website content review processes, reducing human effort and errors.

For example, a compliance team can use this tool to verify whether websites mention relevant regulations such as GDPR or SOC standards.

---

## Requirements
### Software
- Python 3.8+
- Scrapy library
- Pandas library
- Signal handling for graceful termination

### Hardware
- A machine capable of running Python and Scrapy (minimum 4 GB RAM recommended for optimal performance).

### Input Data
A CSV file containing the list of websites with the following columns:
- `Administrators`: Name of the administrator.
- `Admin Website`: URL of the website.

Example CSV content:
```csv
Administrators,Admin Website
Admin1,https://example.com
Admin2,https://example2.com
```

---

## Setup and Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/multi-admin-keyword-spider.git
    cd multi-admin-keyword-spider
    ```

2. Install the required libraries:
    ```bash
    pip install scrapy pandas
    ```

3. Place your input CSV file (e.g., `Admin List - 25.csv`) in the project directory.

4. Update the CSV path in the script if required:
    ```python
    df = pd.read_csv(r"C:\path\to\Admin List - 25.csv")
    ```

---

## Usage
1. Run the spider:
    ```bash
    scrapy runspider multi_admin_spider.py
    ```

2. During the execution, the spider will:
   - Crawl each website from the CSV.
   - Detect keywords and categorize them.
   - Save the results to an Excel file (`multi_admin_results.xlsx`).

3. If the script is interrupted (e.g., `CTRL+C`):
   - The results crawled so far are saved automatically.

### Output Example
An example of the saved Excel file:
| Admin Name | Base URL           | Crawled URL        | RAW Keyword        | Standard Keyword  | NIST | ISO-27001 | SOC | GDPR | ESG |
|------------|--------------------|--------------------|--------------------|-------------------|------|-----------|-----|------|-----|
| Admin1     | https://example.com| https://example.com/nist | nist-, gdpr       | NIST, GDPR       | 1    | 0         | 0   | 1    | 0   |

---

## Enhancements
The following enhancements have been implemented:
1. **Interrupt Handling**: Crawled data is saved when the script is interrupted, ensuring no data loss.
2. **Redundant URL Handling**: Prevents recurrent crawling of identical URLs.
3. **Error Handling**: Logs and skips non-text responses or pages causing errors during crawling.
4. **Logging**: Provides detailed debug-level logs for traceability.

---

## Logs
Logs provide insights into the crawling process. An example log entry:
```
2024-12-11 18:28:05 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://example.com> (referer: None)
```

---

## Future Improvements
- Add support for dynamic keyword categories through configuration files.
- Parallelize crawling for improved performance.
- Integrate with cloud storage to save results remotely.

---

## Contributing
Contributions are welcome! If you want to add a feature or fix a bug, feel free to fork the repository, make changes, and submit a pull request.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

