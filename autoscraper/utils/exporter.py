import csv
import json
from typing import List, Any

def export_results(data: List[Any], file_path: str = "output.csv", format: str = "csv") -> None:
    """
    Export scraped data to a specified format.
    
    Args:
        data (list): The list of items to export.
        file_path (str): The destination file path.
        format (str): The format to save the data in ('csv', 'json', 'txt').
        
    Raises:
        ValueError: If the format is not supported.
    """
    format = format.lower()
    
    if format == "csv":
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for item in data:
                if isinstance(item, (list, tuple)):
                    writer.writerow(item)
                else:
                    writer.writerow([item])
    elif format == "json":
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    elif format == "txt":
        with open(file_path, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(f"{item}\n")
    else:
        raise ValueError(f"Unsupported format '{format}'. Supported formats are: 'csv', 'json', 'txt'.")
