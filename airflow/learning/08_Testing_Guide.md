# Testing Guide for Air flow DAGs

**Goal:** Write robust tests for your DAGs.

---

## 🧪 Testing Levels

### 1. DAG Integrity Tests
**What:** Ensure DAGs load without errors

```python
# tests/test_dag_integrity.py
from airflow.models import DagBag

def test_no_import_errors():
    dag_bag = DagBag(dag_folder='dags/', include_examples=False)
    assert len(dag_bag.import_errors) == 0, f"Errors: {dag_bag.import_errors}"

def test_dag_bag_size():
    dag_bag = DagBag(dag_folder='dags/', include_examples=False)
    assert len(dag_bag.dags) > 0, "No DAGs found"
```

### 2. DAG Structure Tests
**What:** Validate DAG configuration

```python
def test_dag_has_tags():
    dag_bag = DagBag(dag_folder='dags/')
    dag = dag_bag.get_dag('my_dag')
    assert len(dag.tags) > 0, "DAG should have tags"

def test_dag_has_correct_schedule():
    dag_bag = DagBag()
    dag = dag_bag.get_dag('my_dag')
    assert dag.schedule_interval == '@daily'

def test_dag_has_owner():
    dag_bag = DagBag()
    dag = dag_bag.get_dag('my_dag')
    assert dag.default_args.get('owner') == 'data_team'
```

### 3. Task Tests
**What:** Test individual tasks

```python
from airflow.models import DagBag
from datetime import datetime

def test_extract_task():
    dag_bag = DagBag()
    dag = dag_bag.get_dag('etl_pipeline')
    task = dag.get_task('extract')
    
    # Execute task
    execution_date = datetime(2025, 12, 20)
    task.execute(context={'ds': '2025-12-20'})
    
    # Add assertions based on expected behavior
```

### 4. Business Logic Tests
**What:** Test transformation logic

```python
# Assuming you have a function used by a task
from dags.etl_pipeline import transform_data
import pandas as pd

def test_transform_data():
    # Arrange
    raw_data = [
        {'id': 1, 'amount': 100},
        {'id': 2, 'amount': -50},  # Invalid
        {'id': 3, 'amount': 200},
    ]
    
    # Act
    result = transform_data(raw_data)
    
    # Assert
    assert len(result) == 2  # Invalid record filtered
    assert result[0]['tax'] == 8  # 100 * 0.08
```

---

## 🛠️ Test Framework Setup

### Install Test Dependencies

```bash
pip install pytest pytest-cov
```

### Project Structure

```
project/
├── dags/
│   ├── __init__.py
│   └── etl_pipeline.py
├── tests/
│   ├── __init__.py
│   ├── test_dag_integrity.py
│   ├── test_etl_pipeline.py
│   └── conftest.py
└── pytest.ini
```

### Configuration (pytest.ini)

```ini
[pytest]
pythonpath = .
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

---

## 🎯 Complete Test Suite Example

```python
# tests/test_sales_pipeline.py
import pytest
from airflow.models import DagBag
from datetime import datetime
from unittest.mock import Mock, patch

class TestSalesPipeline:
    
    @pytest.fixture
    def dag_bag(self):
        return DagBag(dag_folder='dags/', include_examples=False)
    
    def test_dag_loads(self, dag_bag):
        """Test DAG loads without import errors"""
        assert 'sales_pipeline' in dag_bag.dags
    
    def test_dag_has_correct_tasks(self, dag_bag):
        """Test DAG has expected tasks"""
        dag = dag_bag.get_dag('sales_pipeline')
        expected_tasks = ['extract', 'transform', 'load', 'validate']
        
        actual_tasks = [task.task_id for task in dag.tasks]
        assert set(expected_tasks) == set(actual_tasks)
    
    def test_task_dependencies(self, dag_bag):
        """Test tasks have correct dependencies"""
        dag = dag_bag.get_dag('sales_pipeline')
        
        extract = dag.get_task('extract')
        transform = dag.get_task('transform')
        
        # Transform should depend on extract
        assert extract in transform.upstream_list
    
    @patch('dags.sales_pipeline.HttpHook')
    def test_extract_task(self, mock_hook, dag_bag):
        """Test extract task with mocked API"""
        # Setup mock
        mock_response = Mock()
        mock_response.json.return_value = {'sales': [{'id': 1}]}
        mock_hook.return_value.run.return_value = mock_response
        
        # Execute task
        dag = dag_bag.get_dag('sales_pipeline')
        task = dag.get_task('extract')
        result = task.execute(context={'ds': '2025-12-20'})
        
        # Verify
        assert len(result) == 1
        assert result[0]['id'] == 1
```

---

## 🔄 CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test DAGs

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install apache-airflow pytest pytest-cov
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          pytest tests/ --cov=dags --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## 🎯 Best Practices

### 1. Mock External Dependencies

```python
@patch('airflow.providers.postgres.hooks.postgres.PostgresHook')
def test_with_mocked_db(mock_postgres):
    mock_postgres.return_value.get_records.return_value = [(100,)]
    # Test code here
```

### 2. Use Fixtures for Reusability

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_data():
    return [
        {'id': 1, 'value': 100},
        {'id': 2, 'value': 200},
    ]

def test_transform(sample_data):
    result = transform(sample_data)
    assert len(result) == 2
```

### 3. Test Edge Cases

```python
def test_handles_empty_data():
    result = transform([])
    assert result == []

def test_handles_null_values():
    data = [{'id': 1, 'value': None}]
    result = transform(data)
    assert len(result) == 0  # Should filter nulls
```

### 4. Test DAG Schedule

```python
def test_dag_schedule():
    dag = DagBag().get_dag('my_dag')
    assert dag.schedule_interval == '@daily'
    assert dag.catchup == False
```

---

## 📊 Coverage Goals

- **DAG Integrity:** 100% (all DAGs load)
- **Business Logic:** 80%+ coverage
- **Integration Tests:** Key workflows covered

---

## 🐛 Debugging Failed Tests

```bash
# Run specific test
pytest tests/test_sales_pipeline.py::test_extract_task -v

# Run with print statements
pytest tests/ -s

# Run with debugger
pytest tests/ --pdb
```

---

**Well-tested DAGs = reliable pipelines!** 🧪
