import csv

def query_sales_data(start_date, end_date):
    total = 0
    records = []

    with open("resources/datasets/sales.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if start_date <= row["date"] <= end_date:
                amount = float(row["amount"])
                total += amount
                records.append(row)

    return {
        "total_sales": total,
        "records_count": len(records)
    }


