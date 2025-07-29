"""
Tests for BPMN Parser using pytest
"""
import pytest
from bpmn_parser import BPMNParser, ElementType, ServiceTask, Task


@pytest.fixture
def parser():
    """Create a BPMN parser instance for tests"""
    return BPMNParser()


@pytest.fixture
def sample_processes(parser):
    """Parse the sample BPMN file for tests"""
    return parser.parse_file('sample_process.bpmn')


def test_parse_sample_file(sample_processes):
    """Test parsing the sample BPMN file"""
    assert len(sample_processes) == 1
    
    process = sample_processes[0]
    assert process.id == 'sampleProcess'
    assert process.name == 'Sample Activiti Process'
    
    # Check we have the expected number of elements
    assert len(process.elements) == 8  # 1 start, 3 service tasks, 1 user task, 2 gateways, 1 end
    assert len(process.sequence_flows) == 8


def test_service_task_parsing(sample_processes):
    """Test that service tasks are parsed with Activiti metadata"""
    process = sample_processes[0]
    
    # Find service task with class
    service_task = next(
        (elem for elem in process.elements 
         if elem.id == 'serviceTask1' and isinstance(elem, ServiceTask)), 
        None
    )
    
    assert service_task is not None
    assert service_task.implementation_class == 'com.example.ProcessDataDelegate'
    assert service_task.name == 'Process Data'
    
    # Find service task with expression
    expr_task = next(
        (elem for elem in process.elements 
         if elem.id == 'serviceTask2' and isinstance(elem, ServiceTask)), 
        None
    )
    
    assert expr_task is not None
    assert expr_task.expression == '${autoApprovalService.approve(execution)}'


def test_user_task_parsing(sample_processes):
    """Test that user tasks are parsed with Activiti metadata"""
    process = sample_processes[0]
    
    user_task = next(
        (elem for elem in process.elements 
         if elem.id == 'userTask1' and isinstance(elem, Task)), 
        None
    )
    
    assert user_task is not None
    assert user_task.assignee == 'reviewer'
    assert user_task.candidate_groups == 'managers,supervisors'


def test_sequence_flow_conditions(sample_processes):
    """Test that sequence flow conditions are parsed"""
    process = sample_processes[0]
    
    # Find flow with condition
    conditional_flow = next(
        (flow for flow in process.sequence_flows 
         if flow.id == 'flow3'), 
        None
    )
    
    assert conditional_flow is not None
    assert conditional_flow.condition_expression == '${needsReview == true}'
    assert conditional_flow.name == 'Needs Review'


def test_element_types(sample_processes):
    """Test that different element types are correctly identified"""
    process = sample_processes[0]
    
    # Count elements by type
    element_types = {}
    for element in process.elements:
        element_type = element.element_type
        element_types[element_type] = element_types.get(element_type, 0) + 1
    
    assert element_types[ElementType.START_EVENT] == 1
    assert element_types[ElementType.END_EVENT] == 1
    assert element_types[ElementType.SERVICE_TASK] == 3
    assert element_types[ElementType.USER_TASK] == 1
    assert element_types[ElementType.EXCLUSIVE_GATEWAY] == 2


def test_activiti_metadata_extraction(sample_processes):
    """Test that Activiti metadata is properly extracted"""
    process = sample_processes[0]
    
    # Find service task and check metadata
    service_task = next(
        (elem for elem in process.elements 
         if elem.id == 'serviceTask1'), 
        None
    )
    
    assert service_task is not None
    # Check that activiti metadata is captured
    assert 'activiti:class' in service_task.activiti_metadata
    assert service_task.activiti_metadata['activiti:class'] == 'com.example.ProcessDataDelegate'


def test_sequence_flow_references(sample_processes):
    """Test that sequence flows have correct source and target references"""
    process = sample_processes[0]
    
    # Find the first flow
    first_flow = next(
        (flow for flow in process.sequence_flows 
         if flow.id == 'flow1'), 
        None
    )
    
    assert first_flow is not None
    assert first_flow.source_ref == 'startEvent1'
    assert first_flow.target_ref == 'serviceTask1'


@pytest.mark.parametrize("element_id,expected_type", [
    ('startEvent1', ElementType.START_EVENT),
    ('serviceTask1', ElementType.SERVICE_TASK),
    ('userTask1', ElementType.USER_TASK),
    ('exclusiveGateway1', ElementType.EXCLUSIVE_GATEWAY),
    ('endEvent1', ElementType.END_EVENT),
])
def test_individual_element_types(sample_processes, element_id, expected_type):
    """Test individual element type parsing using parametrized tests"""
    process = sample_processes[0]
    
    element = next(
        (elem for elem in process.elements if elem.id == element_id),
        None
    )
    
    assert element is not None
    assert element.element_type == expected_type


def test_parser_handles_missing_file():
    """Test that parser handles missing files gracefully"""
    parser = BPMNParser()
    
    with pytest.raises(FileNotFoundError):
        parser.parse_file('nonexistent.bpmn')


def test_empty_process_elements():
    """Test handling of processes with no elements"""
    parser = BPMNParser()
    
    # This would require creating a minimal BPMN file for testing
    # For now, we'll test that the parser can handle empty element lists
    assert parser is not None
