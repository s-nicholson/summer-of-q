"""
Tests for BPMN Visualizer using pytest
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from bpmn_visualizer import BPMNVisualizer
from bpmn_parser import BPMNParser, Process, BPMNElement, SequenceFlow, ServiceTask, ElementType


@pytest.fixture
def visualizer():
    """Create a BPMN visualizer instance for tests"""
    return BPMNVisualizer(show_metadata=False)


@pytest.fixture
def visualizer_with_metadata():
    """Create a BPMN visualizer instance with metadata display enabled"""
    return BPMNVisualizer(show_metadata=True)


@pytest.fixture
def sample_process():
    """Create a sample process for testing"""
    # Create a simple process with a few elements
    service_task = ServiceTask(
        id='task1',
        name='Test Task',
        element_type=ElementType.SERVICE_TASK,
        activiti_metadata={'activiti:class': 'com.example.TestClass'},
        implementation_class='com.example.TestClass'
    )
    
    start_event = BPMNElement(
        id='start1',
        name='Start',
        element_type=ElementType.START_EVENT,
        activiti_metadata={}
    )
    
    sequence_flow = SequenceFlow(
        id='flow1',
        name='Test Flow',
        element_type=ElementType.SEQUENCE_FLOW,
        activiti_metadata={},
        source_ref='start1',
        target_ref='task1',
        condition_expression='${test == true}'
    )
    
    return Process(
        id='testProcess',
        name='Test Process',
        elements=[start_event, service_task],
        sequence_flows=[sequence_flow]
    )


def test_visualizer_initialization(visualizer):
    """Test that visualizer initializes correctly"""
    assert visualizer.show_metadata is False
    assert ElementType.START_EVENT in visualizer.element_shapes
    assert ElementType.START_EVENT in visualizer.element_colors


def test_visualizer_with_metadata_initialization(visualizer_with_metadata):
    """Test that visualizer with metadata initializes correctly"""
    assert visualizer_with_metadata.show_metadata is True


@patch('bpmn_visualizer.graphviz.Digraph')
def test_create_diagram(mock_digraph, visualizer, sample_process):
    """Test diagram creation"""
    # Create a mock graph with proper context manager support
    mock_graph = MagicMock()
    mock_subgraph = MagicMock()
    mock_graph.subgraph.return_value.__enter__.return_value = mock_subgraph
    mock_digraph.return_value = mock_graph
    
    result = visualizer.create_diagram([sample_process])
    
    # Verify Digraph was created with correct parameters
    mock_digraph.assert_called_once_with(comment='BPMN Process Diagram')
    
    # Verify graph attributes were set
    assert mock_graph.attr.call_count >= 3  # rankdir, size, node, edge attrs
    
    assert result == mock_graph


def test_build_element_label_without_metadata(visualizer):
    """Test element label building without metadata"""
    service_task = ServiceTask(
        id='task1',
        name='Test Task',
        element_type=ElementType.SERVICE_TASK,
        activiti_metadata={'activiti:class': 'com.example.TestClass'},
        implementation_class='com.example.TestClass'
    )
    
    label = visualizer._build_element_label(service_task)
    assert label == 'Test Task'


def test_build_element_label_with_metadata(visualizer_with_metadata):
    """Test element label building with metadata"""
    service_task = ServiceTask(
        id='task1',
        name='Test Task',
        element_type=ElementType.SERVICE_TASK,
        activiti_metadata={'activiti:class': 'com.example.TestClass'},
        implementation_class='com.example.TestClass'
    )
    
    label = visualizer_with_metadata._build_element_label(service_task)
    assert 'Test Task' in label
    assert 'Class: com.example.TestClass' in label


def test_build_element_label_no_name(visualizer):
    """Test element label building when element has no name"""
    element = BPMNElement(
        id='element1',
        name=None,
        element_type=ElementType.START_EVENT,
        activiti_metadata={}
    )
    
    label = visualizer._build_element_label(element)
    assert label == 'element1'


def test_add_sequence_flow_without_metadata(visualizer):
    """Test adding sequence flow without metadata"""
    mock_graph = Mock()
    
    flow = SequenceFlow(
        id='flow1',
        name='Test Flow',
        element_type=ElementType.SEQUENCE_FLOW,
        activiti_metadata={},
        source_ref='start1',
        target_ref='task1',
        condition_expression='${test == true}'
    )
    
    visualizer._add_sequence_flow_to_diagram(mock_graph, flow)
    
    # Should add edge with just the name
    mock_graph.edge.assert_called_once_with('start1', 'task1', label='Test Flow')


def test_add_sequence_flow_with_metadata(visualizer_with_metadata):
    """Test adding sequence flow with metadata"""
    mock_graph = Mock()
    
    flow = SequenceFlow(
        id='flow1',
        name='Test Flow',
        element_type=ElementType.SEQUENCE_FLOW,
        activiti_metadata={},
        source_ref='start1',
        target_ref='task1',
        condition_expression='${test == true}'
    )
    
    visualizer_with_metadata._add_sequence_flow_to_diagram(mock_graph, flow)
    
    # Should add edge with name and condition
    mock_graph.edge.assert_called_once_with(
        'start1', 
        'task1', 
        label='Test Flow\\n[${test == true}]'
    )


def test_element_shapes_mapping(visualizer):
    """Test that all element types have shape mappings"""
    expected_types = [
        ElementType.START_EVENT,
        ElementType.END_EVENT,
        ElementType.SERVICE_TASK,
        ElementType.USER_TASK,
        ElementType.EXCLUSIVE_GATEWAY,
        ElementType.PARALLEL_GATEWAY
    ]
    
    for element_type in expected_types:
        assert element_type in visualizer.element_shapes
        assert element_type in visualizer.element_colors


def test_save_diagram(visualizer):
    """Test diagram saving functionality"""
    mock_diagram = Mock()
    
    visualizer.save_diagram(mock_diagram, 'test_output', 'svg')
    
    assert mock_diagram.format == 'svg'
    mock_diagram.render.assert_called_once_with('test_output', cleanup=True)
