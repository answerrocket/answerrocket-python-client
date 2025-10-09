"""
Test workflow for dataset CRUD operations.

This script tests the full lifecycle of a dataset including:
1. Creating a dataset with metrics and dimensions
2. Retrieving the dataset
3. Updating metrics and dimensions
4. Deleting metrics and dimensions
5. Deleting the dataset
"""

from answer_rocket import AnswerRocketClient
import uuid

# =============================================================================
# Configuration - Update these values for your environment
# =============================================================================

# Your Answer Rocket API endpoint
API_URL = "http://localhost:8080"

# Your bearer token (get this from the Answer Rocket UI or API)
# Format: "arc--<your-token-here>"
BEARER_TOKEN = "arc--xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# An existing database ID from your Answer Rocket instance
# You can get this from the UI or by calling client.data.get_databases()
DATABASE_ID = "00000000-0000-0000-0000-000000000000"

# =============================================================================

# Initialize client
client = AnswerRocketClient(API_URL, BEARER_TOKEN)

# Parse the database ID
database_id = uuid.UUID(DATABASE_ID)

# Generate a unique dataset ID
dataset_id = uuid.uuid4()

print(f"=== Creating Dataset with ID: {dataset_id} ===\n")

# Step 1: Create an empty dataset (no dimensions or metrics)
dataset = {
    "datasetId": str(dataset_id),
    "name": "test_crud_workflow",
    "databaseId": str(database_id),
    "description": "Test dataset for CRUD workflow",
    "sourceTable": "fact_distributor_sales",
    "dataInterval": "date",
    "miscInfo": None,
    "datasetMinDate": None,
    "datasetMaxDate": None,
    "queryRowLimit": 100,
    "useDatabaseCasing": False,
    "kShotLimit": 3,
    "dimensions": [],
    "metrics": []
}

response = client.data.create_dataset(dataset)
print(f"Create Dataset Response: {response}\n")

if not response.success:
    print(f"Failed to create dataset: {response.error}")
    exit(1)

# Step 1a: Add dimensions to the dataset
print(f"=== Adding Dimensions ===\n")

# Create 'date' dimension using a dictionary
print("Creating 'date' dimension from DICTIONARY...")
dimension_date = {
    "id": "date",
    "name": "date",
    "description": "Transaction date",
    "outputLabel": "Date",
    "isActive": True,
    "miscInfo": None,
    "dataType": "DATE",  # Uppercase to test normalization
    "sqlExpression": "date",
    "sqlSortExpression": None,
    "sampleLimit": 10
}

date_response = client.data.create_dimension(dataset_id, dimension_date)
print(f"Create 'date' Dimension Response: {date_response}\n")

# Create 'department' dimension using a dictionary (uppercase enums)
print("Creating 'department' dimension from DICTIONARY (uppercase enums)...")
dimension_department = {
    "id": "department",
    "name": "department",
    "description": "Department name",
    "outputLabel": "Department",
    "isActive": True,
    "miscInfo": None,
    "dataType": "STRING",  # Uppercase to test normalization
    "sqlExpression": "department",
    "sqlSortExpression": None,
    "sampleLimit": 10
}

dept_response = client.data.create_dimension(dataset_id, dimension_department)
print(f"Create 'department' Dimension Response: {dept_response}\n")

# Create 'region' dimension using a dictionary
print("Creating 'region' dimension from DICTIONARY...")
dimension_region = {
    "id": "region",
    "name": "region",
    "description": "Sales region",
    "outputLabel": "Region",
    "isActive": True,
    "miscInfo": None,
    "dataType": "string",  # lowercase
    "sqlExpression": "region",
    "sqlSortExpression": None,
    "sampleLimit": 10
}

region_response = client.data.create_dimension(dataset_id, dimension_region)
print(f"Create 'region' Dimension Response: {region_response}\n")

# Step 1b: Add metrics to the dataset
print(f"=== Adding Metrics ===\n")

# Create 'sales' metric using a dictionary (uppercase enums)
print("Creating 'sales' metric from DICTIONARY (uppercase enums)...")
metric_sales = {
    "id": "sales_amt",
    "name": "sales",
    "description": "Total sales amount",
    "outputLabel": "Sales",
    "isActive": True,
    "miscInfo": None,
    "dataType": "NUMBER",  # Uppercase to test normalization
    "metricType": "BASIC",  # Uppercase to test normalization
    "displayFormat": "$,.2f",
    "sqlAggExpression": "SUM(sales_amt)",
    "sqlRowExpression": "sales_amt",
    "growthType": "PERCENT_CHANGE",  # Uppercase to test normalization
    "growthFormat": ",.2%"
}

sales_response = client.data.create_metric(dataset_id, metric_sales)
print(f"Create 'sales' Metric Response: {sales_response}\n")

# Create 'tax' metric using a dictionary
print("Creating 'tax' metric from DICTIONARY...")
metric_tax = {
    "id": "tax_amt",
    "name": "tax",
    "description": "Total tax amount",
    "outputLabel": "Tax",
    "isActive": True,
    "miscInfo": None,
    "dataType": "NUMBER",  # Uppercase to test normalization
    "metricType": "BASIC",  # Uppercase to test normalization
    "displayFormat": "$,.2f",
    "sqlAggExpression": "SUM(tax_amt)",
    "sqlRowExpression": "tax_amt",
    "growthType": "percent_change",  # lowercase
    "growthFormat": ",.2%"
}

tax_response = client.data.create_metric(dataset_id, metric_tax)
print(f"Create 'tax' Metric Response: {tax_response}\n")

# Create 'quantity' metric using a dictionary with mixed case
print("Creating 'quantity' metric from DICTIONARY (mixed case)...")
metric_quantity = {
    "id": "quantity",
    "name": "quantity",
    "description": "Total quantity sold",
    "outputLabel": "Quantity",
    "isActive": True,
    "miscInfo": None,
    "dataType": "number",  # lowercase
    "metricType": "Basic",  # Mixed case to test normalization
    "displayFormat": ",.0f",
    "sqlAggExpression": "SUM(quantity)",
    "sqlRowExpression": "quantity",
    "growthType": "Percent_Change",  # Mixed case to test normalization
    "growthFormat": ",.2%"
}

quantity_response = client.data.create_metric(dataset_id, metric_quantity)
print(f"Create 'quantity' Metric Response: {quantity_response}\n")

# Step 2: Retrieve the dataset using get_dataset2()
print(f"=== Retrieving Dataset ===\n")
retrieved_dataset = client.data.get_dataset2(dataset_id)

if retrieved_dataset is None:
    print("Failed to retrieve dataset")
    exit(1)

print(f"Dataset Name: {retrieved_dataset.name}")
print(f"Number of Dimensions: {len(retrieved_dataset.dimensions)}")
print(f"Number of Metrics: {len(retrieved_dataset.metrics)}")
print(f"Dimensions: {[d.name for d in retrieved_dataset.dimensions]}")
print(f"Metrics: {[m.name for m in retrieved_dataset.metrics]}\n")

# Step 3: Update a metric
print(f"=== Updating 'sales' Metric ===\n")

# Find the sales metric
sales_metric = next((m for m in retrieved_dataset.metrics if m.name == "sales"), None)

if sales_metric:
    print(f"Original SQL: {sales_metric.sql_agg_expression}")

    # Update the metric
    sales_metric.sql_agg_expression = "SUM(sales_amt * 1.1)"
    sales_metric.description = "Total sales amount with 10% markup"

    update_response = client.data.update_metric(dataset_id, sales_metric)
    print(f"Update Metric Response: {update_response}")

    if update_response.success:
        print(f"Updated SQL: {sales_metric.sql_agg_expression}\n")
    else:
        print(f"Failed to update metric: {update_response.error}\n")

# Step 4: Update a dimension
print(f"=== Updating 'department' Dimension ===\n")

# Find the department dimension
dept_dimension = next((d for d in retrieved_dataset.dimensions if d.name == "department"), None)

if dept_dimension:
    print(f"Original Description: {dept_dimension.description}")

    # Update the dimension
    dept_dimension.description = "Department name (updated)"
    dept_dimension.output_label = "Department Name"

    update_response = client.data.update_dimension(dataset_id, dept_dimension)
    print(f"Update Dimension Response: {update_response}")

    if update_response.success:
        print(f"Updated Description: {dept_dimension.description}\n")
    else:
        print(f"Failed to update dimension: {update_response.error}\n")

# Step 5: Create a new metric
print(f"=== Creating New Metric 'average_sale' ===\n")

new_metric = {
    "id": "average_sale",
    "name": "average_sale",
    "description": "Average sale amount",
    "outputLabel": "Avg Sale",
    "isActive": True,
    "miscInfo": None,
    "dataType": "number",
    "metricType": "ratio",
    "displayFormat": "$,.2f",
    "sqlAggExpression": "AVG(sales_amt)",
    "sqlRowExpression": "sales_amt",
    "growthType": "percent_change",
    "growthFormat": ",.2%"
}

create_metric_response = client.data.create_metric(dataset_id, new_metric)
print(f"Create Metric Response: {create_metric_response}\n")

# Step 6: Create a new dimension
print(f"=== Creating New Dimension 'product' ===\n")

new_dimension = {
    "id": "product",
    "name": "product",
    "description": "Product name",
    "outputLabel": "Product",
    "isActive": True,
    "miscInfo": None,
    "dataType": "string",
    "sqlExpression": "product",
    "sqlSortExpression": None,
    "sampleLimit": 10
}

create_dimension_response = client.data.create_dimension(dataset_id, new_dimension)
print(f"Create Dimension Response: {create_dimension_response}\n")

# Step 7: Retrieve the dataset again to see all changes
print(f"=== Retrieving Updated Dataset ===\n")
updated_dataset = client.data.get_dataset2(dataset_id)

if updated_dataset:
    print(f"Dataset Name: {updated_dataset.name}")
    print(f"Number of Dimensions: {len(updated_dataset.dimensions)}")
    print(f"Number of Metrics: {len(updated_dataset.metrics)}")
    print(f"Dimensions: {[d.name for d in updated_dataset.dimensions]}")
    print(f"Metrics: {[m.name for m in updated_dataset.metrics]}\n")

# Step 8: Delete a metric
print(f"=== Deleting 'quantity' Metric ===\n")

delete_metric_response = client.data.delete_metric(dataset_id, "quantity")
print(f"Delete Metric Response: {delete_metric_response}\n")

# Step 9: Delete a dimension
print(f"=== Deleting 'region' Dimension ===\n")

delete_dimension_response = client.data.delete_dimension(dataset_id, "region")
print(f"Delete Dimension Response: {delete_dimension_response}\n")

# Step 10: Retrieve the dataset one more time to verify deletions
print(f"=== Retrieving Dataset After Deletions ===\n")
final_dataset = client.data.get_dataset2(dataset_id)

if final_dataset:
    print(f"Dataset Name: {final_dataset.name}")
    print(f"Number of Dimensions: {len(final_dataset.dimensions)}")
    print(f"Number of Metrics: {len(final_dataset.metrics)}")
    print(f"Dimensions: {[d.name for d in final_dataset.dimensions]}")
    print(f"Metrics: {[m.name for m in final_dataset.metrics]}\n")

# Step 11: Clean up - Delete the dataset
print(f"=== Cleaning Up: Deleting Dataset ===\n")

# Note: You'll need to implement delete_dataset() in the SDK if it doesn't exist yet
# For now, we'll just print a message
print(f"Dataset {dataset_id} should be manually deleted or implement delete_dataset() method\n")

print("=== Workflow Complete ===")
